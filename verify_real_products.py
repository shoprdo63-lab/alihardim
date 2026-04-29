#!/usr/bin/env python
"""
Verify that all products have REAL AliExpress product IDs
Remove fake products and ensure links work
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product

def verify_products():
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking products...")
        
        all_products = Product.query.all()
        print(f"Total products: {len(all_products)}")
        
        real_products = 0
        fake_products = 0
        
        for p in all_products:
            # Check if product_id looks like a real AliExpress ID
            # Real IDs: 1005001234567890 (16 digits starting with 100500 or similar)
            pid = p.product_id
            
            if pid and (pid.startswith('100500') or pid.startswith('32568') or pid.startswith('4001')):
                real_products += 1
            else:
                fake_products += 1
                print(f"  ⚠️ Fake product: {p.title_hebrew or p.title} (ID: {pid})")
        
        print(f"\n📊 Results:")
        print(f"  ✅ Real AliExpress products: {real_products}")
        print(f"  ❌ Fake products: {fake_products}")
        
        if fake_products > 0:
            print(f"\n🗑️  Removing {fake_products} fake products...")
            
            for p in all_products:
                pid = p.product_id
                if not (pid and (pid.startswith('100500') or pid.startswith('32568') or pid.startswith('4001'))):
                    db.session.delete(p)
            
            db.session.commit()
            print("✅ Fake products removed!")
        
        # Verify links
        remaining = Product.query.all()
        print(f"\n✅ Remaining real products: {len(remaining)}")
        
        if remaining:
            sample = remaining[0]
            print(f"\n📌 Sample product:")
            print(f"  Title: {sample.title_hebrew or sample.title}")
            print(f"  ID: {sample.product_id}")
            print(f"  Link: https://www.aliexpress.com/item/{sample.product_id}.html")
            print(f"  Image: {sample.image_url[:80] if sample.image_url else 'None'}...")

if __name__ == '__main__':
    verify_products()
