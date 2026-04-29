#!/usr/bin/env python
"""
Fetch real products from AliExpress API and save to database
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.api.aliexpress import aliexpress_api
from app.models.database import Product
from app.services.content_filter import is_modest_product, translate_to_hebrew, generate_hebrew_description
import time

# Search keywords for different categories
CATEGORY_KEYWORDS = {
    'electronic': ['bluetooth headphones', 'wireless charger', 'power bank', 'usb cable', 'phone case'],
    'toys': ['educational toys', 'building blocks', 'puzzle games', 'kids drone', 'robot toy'],
    'home_garden': ['led light strip', 'kitchen organizer', 'wall stickers', 'plant pots', 'storage box'],
    'tools': ['screwdriver set', 'tool kit', 'multimeter', 'soldering iron', 'drill bits'],
    'jewish': ['menorah', 'dreidel', 'kippah clips', 'shabbat candle', 'mezuzah case'],
    'sports': ['resistance bands', 'yoga mat', 'dumbbell set', 'jump rope', 'sports bottle'],
    'car': ['car phone holder', 'car charger', 'dash cam', 'tire pressure', 'car organizer'],
    'pet': ['pet toys', 'dog bed', 'cat scratcher', 'pet feeder', 'pet grooming'],
    'office': ['pen set', 'notebook', 'desk organizer', 'sticky notes', 'calculator'],
    'art': ['paint set', 'drawing pencils', 'craft supplies', 'sewing kit', 'scrapbook'],
}


def fetch_and_save_products():
    app = create_app()
    
    with app.app_context():
        print("Fetching real products from AliExpress API...")
        
        total_added = 0
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            print(f"\n📂 Category: {category}")
            
            for keyword in keywords:
                print(f"  🔍 Searching: {keyword}")
                
                try:
                    # Fetch products from API
                    result = aliexpress_api._make_request('GET', {
                        'method': 'aliexpress.affiliate.product.query',
                        'keywords': keyword,
                        'page_no': 1,
                        'page_size': 20,
                        'target_currency': 'USD',
                        'target_language': 'EN',
                        'tracking_id': aliexpress_api.tracking_id,
                        'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title,discount',
                    })
                    
                    if not result or 'resp_result' not in result:
                        print(f"    ❌ No results for {keyword}")
                        continue
                    
                    data = result['resp_result'].get('result', {})
                    products_data = data.get('products', {}).get('product', [])
                    
                    print(f"    ✅ Found {len(products_data)} products")
                    
                    added_for_keyword = 0
                    
                    for product in products_data:
                        title = product.get('product_title', '')
                        product_id = product.get('product_id', '')
                        
                        # Check if already exists
                        if Product.query.filter_by(product_id=product_id).first():
                            continue
                        
                        # Filter non-modest (skip if not modest)
                        if not is_modest_product(title):
                            continue
                        
                        # Get prices
                        sale_price = product.get('target_sale_price', product.get('sale_price', '0'))
                        try:
                            price = float(str(sale_price).replace('$', '').replace(',', ''))
                        except:
                            price = 0.0
                        
                        # Generate affiliate link
                        product_url = product.get('product_detail_url', '')
                        affiliate_url = aliexpress_api.generate_affiliate_link(product_url) if product_url else product_url
                        
                        # Translate to Hebrew
                        hebrew_title, _ = translate_to_hebrew(title)
                        hebrew_desc = generate_hebrew_description({'title': title, 'category': category})
                        
                        # Create product
                        new_product = Product(
                            product_id=product_id,
                            title=title,
                            title_hebrew=hebrew_title,
                            description_hebrew=hebrew_desc,
                            price=price,
                            original_price=price * 1.2 if price > 0 else price,
                            currency='USD',
                            category=category,
                            image_url=product.get('product_main_image', ''),
                            product_url=product_url,
                            affiliate_url=affiliate_url,
                            rating=float(product.get('evaluate_rate', '4.5').split()[0]) if product.get('evaluate_rate') else 4.5,
                            reviews_count=0,
                            orders_count=0,
                            store_name=product.get('shop_title', ''),
                            is_modest=True
                        )
                        
                        db.session.add(new_product)
                        added_for_keyword += 1
                        total_added += 1
                        
                        if total_added % 100 == 0:
                            db.session.commit()
                            print(f"    💾 Saved {total_added} products so far...")
                    
                    print(f"    ✅ Added {added_for_keyword} products for '{keyword}'")
                    
                    # Small delay to not hit rate limits
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ❌ Error: {e}")
                    continue
            
            # Commit after each category
            db.session.commit()
        
        print(f"\n🎉 Done! Added {total_added} real products from AliExpress!")


if __name__ == '__main__':
    fetch_and_save_products()
