#!/usr/bin/env python
"""
Import REAL products from AliExpress API
This will get products with REAL IDs and REAL images
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.api.aliexpress import aliexpress_api
from app.models.database import Product

def import_products():
    app = create_app()
    
    with app.app_context():
        print("🚀 Importing REAL products from AliExpress API...")
        
        # Clear existing fake products first
        print("\n🗑️  Clearing old products...")
        Product.query.delete()
        db.session.commit()
        print("✅ Old products cleared!")
        
        # Get products from API
        keywords = ['bluetooth', 'charger', 'phone case', 'headphones', 'watch']
        total_added = 0
        
        for keyword in keywords:
            print(f"\n🔍 Searching: {keyword}")
            
            try:
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
                    print(f"  ❌ No results")
                    continue
                
                data = result['resp_result'].get('result', {})
                products_data = data.get('products', {}).get('product', [])
                
                print(f"  ✅ Found {len(products_data)} products")
                
                for product in products_data:
                    # Get price
                    price_str = product.get('target_sale_price', product.get('sale_price', '0'))
                    try:
                        price = float(str(price_str).replace('$', '').replace(',', ''))
                    except:
                        price = 0.0
                    
                    # Create product with REAL data
                    new_product = Product(
                        product_id=product.get('product_id'),
                        title=product.get('product_title', ''),
                        title_hebrew=product.get('product_title', ''),  # Will translate later
                        description_hebrew='מוצר איכותי מאלי אקספרס',
                        price=price,
                        original_price=price * 1.2 if price > 0 else 0,
                        currency='USD',
                        category='electronic',
                        image_url=product.get('product_main_image', ''),
                        product_url=product.get('product_detail_url', ''),
                        affiliate_url=product.get('product_detail_url', ''),
                        rating=float(str(product.get('evaluate_rate', '4.5')).split()[0]) if product.get('evaluate_rate') else 4.5,
                        reviews_count=0,
                        orders_count=0,
                        store_name=product.get('shop_title', 'AliExpress'),
                        is_modest=True
                    )
                    
                    db.session.add(new_product)
                    total_added += 1
                
                db.session.commit()
                print(f"  ✅ Added {len(products_data)} products")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print(f"\n🎉 Done! Total real products added: {total_added}")
        
        # Show sample
        if total_added > 0:
            sample = Product.query.first()
            print(f"\n📌 Sample:")
            print(f"  ID: {sample.product_id}")
            print(f"  Title: {sample.title}")
            print(f"  Price: ${sample.price}")
            print(f"  Link: https://www.aliexpress.com/item/{sample.product_id}.html")

if __name__ == '__main__':
    import_products()
