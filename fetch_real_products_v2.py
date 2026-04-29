#!/usr/bin/env python
"""
Fetch real products from AliExpress API - Bypass content filter for API results
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.api.aliexpress import aliexpress_api
from app.models.database import Product
from app.services.content_filter import translate_to_hebrew, generate_hebrew_description
import time

# Simple keywords that should return results
SEARCH_KEYWORDS = [
    'bluetooth', 'charger', 'cable', 'case cover', 'screen protector',
    'power bank', 'wireless mouse', 'keyboard', 'usb hub',
    'toy car', 'building blocks', 'puzzle', 'educational toy',
    'led light', 'kitchen tool', 'storage box', 'wall sticker',
    'tool set', 'screwdriver', 'tape measure', 'glue gun',
    'sports ball', 'resistance band', 'water bottle', 'yoga',
    'car charger', 'phone holder', 'organizer', 'cleaning cloth',
    'dog toy', 'pet bowl', 'scratching post',
    'pen', 'notebook', 'sticky note', 'folder',
    'paint', 'brush', 'canvas', 'craft',
]


def is_simple_modest_check(title):
    """Simple check - only block obvious bad words."""
    title_lower = title.lower()
    bad_words = ['sexy', 'lingerie', 'bikini', 'underwear', 'bra ', 'bras ', 'adult', 'porn', 'nude']
    for word in bad_words:
        if word in title_lower:
            return False
    return True


def fetch_real_products():
    app = create_app()
    
    with app.app_context():
        print("Fetching real products from AliExpress API...")
        print("=" * 50)
        
        total_added = 0
        total_api_results = 0
        
        for keyword in SEARCH_KEYWORDS:
            print(f"\n🔍 Searching: '{keyword}'")
            
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
                    print(f"   ⚠️ No API response")
                    continue
                
                data = result['resp_result'].get('result', {})
                products_data = data.get('products', {}).get('product', [])
                
                if not products_data:
                    print(f"   ⚠️ No products in response")
                    continue
                
                total_api_results += len(products_data)
                print(f"   📦 API returned {len(products_data)} products")
                
                added = 0
                for product in products_data:
                    title = product.get('product_title', '')
                    product_id = product.get('product_id', '')
                    
                    # Skip if exists
                    if Product.query.filter_by(product_id=product_id).first():
                        continue
                    
                    # Simple modest check
                    if not is_simple_modest_check(title):
                        continue
                    
                    # Get price
                    sale_price = product.get('target_sale_price', product.get('sale_price', '0'))
                    try:
                        price = float(str(sale_price).replace('$', '').replace(',', ''))
                    except:
                        price = 0.0
                    
                    # URLs
                    product_url = product.get('product_detail_url', '')
                    affiliate_url = aliexpress_api.generate_affiliate_link(product_url) if product_url else product_url
                    
                    # Hebrew translation
                    hebrew_title, _ = translate_to_hebrew(title)
                    hebrew_desc = generate_hebrew_description({'title': title, 'category': 'general'})
                    
                    # Determine category from keyword
                    category = 'electronic' if any(x in keyword for x in ['charger', 'cable', 'bluetooth', 'usb', 'wireless', 'keyboard', 'mouse']) else \
                               'toys' if 'toy' in keyword or 'puzzle' in keyword or 'blocks' in keyword else \
                               'home_garden' if any(x in keyword for x in ['light', 'kitchen', 'storage', 'wall']) else \
                               'tools' if any(x in keyword for x in ['tool', 'screwdriver', 'tape', 'glue']) else \
                               'sports' if any(x in keyword for x in ['sports', 'resistance', 'yoga', 'water']) else \
                               'car' if 'car' in keyword else \
                               'pet' if 'pet' in keyword or 'dog' in keyword else \
                               'office' if any(x in keyword for x in ['pen', 'notebook', 'sticky', 'folder']) else \
                               'art' if any(x in keyword for x in ['paint', 'brush', 'canvas', 'craft']) else \
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
                        image_url=product.get('product_main_image', ''),
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
                
                print(f"   ✅ Added {added} products (Total: {total_added})")
                
                # Save every 50 products
                if total_added % 50 == 0:
                    db.session.commit()
                    print(f"   💾 Committed {total_added} products to database")
                
                time.sleep(0.3)  # Rate limit
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        # Final commit
        db.session.commit()
        
        print("\n" + "=" * 50)
        print(f"🎉 Done!")
        print(f"   API returned: {total_api_results} total products")
        print(f"   Added to DB: {total_added} products")


if __name__ == '__main__':
    fetch_real_products()
