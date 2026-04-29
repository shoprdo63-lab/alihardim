#!/usr/bin/env python
"""
FORCE import real products with REAL images from AliExpress API
This will delete all fake products and import real ones with real images
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.api.aliexpress import aliexpress_api
from app.models.database import Product
import time

def force_import():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("🚀 FORCE IMPORT: Real AliExpress Products with REAL Images")
        print("=" * 60)
        
        # Step 1: Delete ALL existing products
        count = Product.query.count()
        print(f"\n🗑️  Deleting {count} existing products...")
        Product.query.delete()
        db.session.commit()
        print("✅ All products deleted!")
        
        # Step 2: Import from API with keywords that give results
        keywords = [
            'smart watch', 'bluetooth headphones', 'wireless charger',
            'phone case', 'power bank', 'usb cable', 'screen protector'
        ]
        
        total_added = 0
        
        for keyword in keywords:
            print(f"\n🔍 Searching: '{keyword}'")
            
            try:
                # Call API
                result = aliexpress_api._make_request('GET', {
                    'method': 'aliexpress.affiliate.product.query',
                    'keywords': keyword,
                    'page_no': 1,
                    'page_size': 50,
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
                    print(f"   ⚠️ No products found")
                    continue
                
                print(f"   📦 API returned {len(products_data)} products")
                
                added = 0
                for product in products_data:
                    pid = product.get('product_id', '')
                    
                    # Skip if already exists
                    if Product.query.filter_by(product_id=pid).first():
                        continue
                    
                    # Get price
                    price_str = product.get('target_sale_price', product.get('sale_price', '0'))
                    try:
                        price = float(str(price_str).replace('$', '').replace(',', ''))
                    except:
                        price = 0.0
                    
                    # Get image
                    image_url = product.get('product_main_image', '')
                    
                    # Debug
                    if added == 0:
                        print(f"   🖼️  Sample image: {image_url[:80]}...")
                    
                    # Create product with REAL data
                    new_product = Product(
                        product_id=pid,
                        title=product.get('product_title', ''),
                        title_hebrew=product.get('product_title', ''),  # Hebrew translation later
                        description_hebrew='מוצר איכותי מאלי אקספרס. משלוח חינם.',
                        price=price,
                        original_price=price * 1.2 if price > 0 else 0,
                        currency='USD',
                        category='electronic',
                        image_url=image_url,  # REAL IMAGE!
                        product_url=product.get('product_detail_url', ''),
                        affiliate_url=product.get('product_detail_url', ''),
                        rating=float(str(product.get('evaluate_rate', '4.5')).split()[0]) if product.get('evaluate_rate') else 4.5,
                        reviews_count=0,
                        orders_count=0,
                        store_name=product.get('shop_title', 'AliExpress'),
                        is_modest=True
                    )
                    
                    db.session.add(new_product)
                    added += 1
                    total_added += 1
                
                db.session.commit()
                print(f"   ✅ Added {added} products (Total: {total_added})")
                
                time.sleep(0.5)  # Rate limit
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
        
        print("\n" + "=" * 60)
        print(f"🎉 DONE! Total real products: {total_added}")
        
        # Show samples
        if total_added > 0:
            print("\n📌 Sample products with REAL images:")
            samples = Product.query.limit(3).all()
            for i, p in enumerate(samples, 1):
                print(f"\n{i}. {p.title[:50]}...")
                print(f"   ID: {p.product_id}")
                print(f"   Price: ${p.price}")
                print(f"   Image: {p.image_url[:70]}...")
                print(f"   Link: https://www.aliexpress.com/item/{p.product_id}.html")

if __name__ == '__main__':
    force_import()
