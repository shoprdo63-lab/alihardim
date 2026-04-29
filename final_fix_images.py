#!/usr/bin/env python
"""FINAL FIX: Delete all products and import REAL ones with REAL images"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product
from app.api.aliexpress import aliexpress_api

app = create_app()

with app.app_context():
    print("=" * 70)
    print("🗑️  STEP 1: DELETING ALL FAKE PRODUCTS...")
    print("=" * 70)
    
    count_before = Product.query.count()
    if count_before > 0:
        Product.query.delete()
        db.session.commit()
        print(f"✅ Deleted {count_before} fake products with placeholder images")
    else:
        print("ℹ️  No products to delete")
    
    print("\n" + "=" * 70)
    print("🚀 STEP 2: IMPORTING REAL PRODUCTS FROM ALIEXPRESS API...")
    print("=" * 70)
    
    # Keywords that return good results
    keywords = [
        'smartphone', 'headphones', 'smart watch', 'laptop', 'tablet',
        'charger', 'case', 'cable', 'speaker', 'camera',
        'power bank', 'bluetooth', 'wireless', 'adapter'
    ]
    
    total_added = 0
    
    for keyword in keywords:
        try:
            print(f"\n🔍 Searching: '{keyword}'...", end=" ")
            
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
                print("❌ No API response")
                continue
            
            data = result['resp_result'].get('result', {})
            products_data = data.get('products', {}).get('product', [])
            
            if not products_data:
                print("⚠️  No products found")
                continue
            
            added = 0
            for i, product in enumerate(products_data):
                pid = product.get('product_id', '')
                
                # Skip if already exists
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
                
                # Debug first product
                if added == 0 and i == 0:
                    print(f"\n   🖼️  Sample image: {image_url[:70]}...")
                
                new_product = Product(
                    product_id=pid,
                    title=product.get('product_title', ''),
                    title_hebrew=product.get('product_title', ''),
                    description_hebrew='מוצר איכותי מאלי אקספרס עם משלוח חינם',
                    price=price,
                    original_price=price * 1.2 if price > 0 else 0,
                    currency='USD',
                    category='electronic',
                    image_url=image_url,  # REAL IMAGE from AliExpress!
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
            print(f"✅ +{added} (Total: {total_added})")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:60]}")
    
    print("\n" + "=" * 70)
    print(f"🎉 COMPLETE! Imported {total_added} REAL products with REAL images")
    print("=" * 70)
    
    # Verify
    if total_added > 0:
        sample = Product.query.first()
        print(f"\n📌 Sample product:")
        print(f"   Title: {sample.title[:50]}")
        print(f"   Image URL: {sample.image_url[:70]}...")
        print(f"   Is real AliExpress image: {'alicdn' in sample.image_url or 'aliexpress' in sample.image_url if sample.image_url else False}")
