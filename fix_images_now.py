#!/usr/bin/env python
"""DELETE all products and import REAL ones with REAL images"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product
from app.api.aliexpress import aliexpress_api

app = create_app()

with app.app_context():
    print("=" * 60)
    print("🗑️  DELETING ALL PRODUCTS with fake images...")
    print("=" * 60)
    
    # Delete ALL products
    count_before = Product.query.count()
    Product.query.delete()
    db.session.commit()
    
    print(f"✅ Deleted {count_before} fake products")
    print()
    
    # Now import REAL products
    print("=" * 60)
    print("🚀 Importing REAL products with REAL images...")
    print("=" * 60)
    
    keywords = ['smartphone', 'headphones', 'smart watch', 'laptop', 'tablet', 
                'charger', 'case', 'cable', 'speaker', 'camera']
    
    total_added = 0
    
    for keyword in keywords:
        try:
            print(f"\n🔍 Searching: {keyword}")
            
            result = aliexpress_api._make_request('GET', {
                'method': 'aliexpress.affiliate.product.query',
                'keywords': keyword,
                'page_no': 1,
                'page_size': 50,
                'target_currency': 'USD',
                'target_language': 'EN',
                'tracking_id': aliexpress_api.tracking_id,
                'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title',
            })
            
            if not result or 'resp_result' not in result:
                print("   ❌ No response from API")
                continue
            
            data = result['resp_result'].get('result', {})
            products_data = data.get('products', {}).get('product', [])
            
            print(f"   📦 Found {len(products_data)} products")
            
            added = 0
            for product in products_data:
                pid = product.get('product_id', '')
                
                # Skip if exists
                if Product.query.filter_by(product_id=pid).first():
                    continue
                
                # Parse price
                price_str = product.get('target_sale_price', product.get('sale_price', '0'))
                try:
                    price = float(str(price_str).replace('$', '').replace(',', ''))
                except:
                    price = 0.0
                
                # Get REAL image URL from API
                image_url = product.get('product_main_image', '')
                
                # Debug - print first image URL
                if added == 0:
                    print(f"   🖼️  Sample image URL: {image_url[:80]}...")
                
                new_product = Product(
                    product_id=pid,
                    title=product.get('product_title', ''),
                    title_hebrew=product.get('product_title', ''),
                    description_hebrew='מוצר איכותי מאלי אקספרס',
                    price=price,
                    original_price=price * 1.2 if price > 0 else 0,
                    currency='USD',
                    category='electronic',
                    image_url=image_url,  # REAL IMAGE from API!
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
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎉 DONE! Total real products: {total_added}")
    print("=" * 60)
    
    # Verify
    if total_added > 0:
        sample = Product.query.first()
        print(f"\n📌 Sample product:")
        print(f"   Title: {sample.title[:50]}")
        print(f"   Image: {sample.image_url[:70]}...")
        print(f"   Has real image: {'alicdn' in sample.image_url if sample.image_url else False}")
