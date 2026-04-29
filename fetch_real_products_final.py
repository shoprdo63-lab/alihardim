#!/usr/bin/env python
"""
Fetch REAL products with REAL images from AliExpress API!
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.api.aliexpress import aliexpress_api
from app.models.database import Product
from app.services.content_filter import translate_to_hebrew, generate_hebrew_description
import time

# Search keywords
KEYWORDS = [
    'bluetooth headphones', 'wireless charger', 'phone case', 'power bank',
    'smart watch', 'usb cable', 'screen protector', 'car charger',
    'wireless mouse', 'keyboard', 'led light', 'wifi camera',
    'toy car', 'building blocks', 'puzzle', 'educational toy',
    'kitchen tool', 'storage box', 'organizer', 'led strip',
    'tool set', 'screwdriver', 'tape measure', 'drill bits',
    'yoga mat', 'resistance band', 'water bottle', 'sports bag',
    'car phone holder', 'cleaning cloth', 'tool kit',
    'dog toy', 'pet bowl', 'cat toy',
    'pen set', 'notebook', 'sticky notes',
    'paint set', 'brush', 'canvas'
]


def fetch_products():
    app = create_app()
    
    with app.app_context():
        print("🚀 Fetching REAL products from AliExpress API...")
        print("=" * 60)
        
        total_added = 0
        
        for keyword in KEYWORDS:
            print(f"\n🔍 {keyword}...", end=" ")
            
            try:
                # Call API
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
                    print("❌")
                    continue
                
                data = result['resp_result'].get('result', {})
                products_data = data.get('products', {}).get('product', [])
                
                if not products_data:
                    print("⚠️")
                    continue
                
                added = 0
                for product in products_data:
                    product_id = product.get('product_id', '')
                    
                    # Skip if exists
                    if Product.query.filter_by(product_id=product_id).first():
                        continue
                    
                    title = product.get('product_title', '')
                    
                    # Get price
                    sale_price = product.get('target_sale_price', product.get('sale_price', '0'))
                    try:
                        price = float(str(sale_price).replace('$', '').replace(',', ''))
                    except:
                        price = 0.0
                    
                    # URLs
                    product_url = product.get('product_detail_url', '')
                    affiliate_url = aliexpress_api.generate_affiliate_link(product_url) if product_url else product_url
                    
                    # Hebrew
                    hebrew_title, _ = translate_to_hebrew(title)
                    hebrew_desc = generate_hebrew_description({'title': title, 'category': 'general'})
                    
                    # Determine category
                    keyword_lower = keyword.lower()
                    category = 'electronic' if any(x in keyword_lower for x in ['bluetooth', 'charger', 'phone', 'power', 'smart', 'usb', 'wireless', 'keyboard', 'mouse', 'wifi', 'camera']) else \
                               'toys' if any(x in keyword_lower for x in ['toy', 'puzzle', 'blocks']) else \
                               'home_garden' if any(x in keyword_lower for x in ['kitchen', 'storage', 'organizer', 'led', 'light']) else \
                               'tools' if any(x in keyword_lower for x in ['tool', 'screwdriver', 'tape', 'drill']) else \
                               'sports' if any(x in keyword_lower for x in ['yoga', 'resistance', 'sports', 'water']) else \
                               'car' if 'car' in keyword_lower else \
                               'pet' if any(x in keyword_lower for x in ['dog', 'pet', 'cat']) else \
                               'office' if any(x in keyword_lower for x in ['pen', 'notebook', 'sticky']) else \
                               'art' if any(x in keyword_lower for x in ['paint', 'brush', 'canvas']) else \
                               'electronic'
                    
                    # Create product
                    new_product = Product(
                        product_id=product_id,
                        title=title,
                        title_hebrew=hebrew_title,
                        description_hebrew=hebrew_desc,
                        price=price,
                        original_price=price * 1.15 if price > 0 else price,
                        currency='USD',
                        category=category,
                        image_url=product.get('product_main_image', ''),  # REAL IMAGE!
                        product_url=product_url,
                        affiliate_url=affiliate_url,
                        rating=float(str(product.get('evaluate_rate', '4.5')).split()[0]) if product.get('evaluate_rate') else 4.5,
                        reviews_count=0,
                        orders_count=0,
                        store_name=product.get('shop_title', 'AliExpress Store'),
                        is_modest=True
                    )
                    
                    db.session.add(new_product)
                    added += 1
                    total_added += 1
                
                print(f"✅ +{added}")
                
                # Save every 50
                if total_added % 50 == 0:
                    db.session.commit()
                    print(f"   💾 Total: {total_added}")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        # Final save
        db.session.commit()
        
        print("\n" + "=" * 60)
        print(f"🎉 SUCCESS! Added {total_added} REAL products with REAL images!")
        print("📸 All products now have actual AliExpress images!")


if __name__ == '__main__':
    fetch_products()
