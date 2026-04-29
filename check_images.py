#!/usr/bin/env python
"""Check if products have real images"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product

app = create_app()

with app.app_context():
    total = Product.query.count()
    print(f"Total products: {total}\n")
    
    # Check first 5 products
    products = Product.query.limit(5).all()
    
    for i, p in enumerate(products, 1):
        print(f"{i}. {p.title[:40]}...")
        print(f"   ID: {p.product_id}")
        
        # Check if image is real
        if p.image_url and 'placehold' in p.image_url:
            print(f"   ❌ FAKE IMAGE: {p.image_url[:60]}...")
        elif p.image_url and ('ae01.alicdn' in p.image_url or 'alicdn' in p.image_url):
            print(f"   ✅ REAL ALIEXPRESS IMAGE: {p.image_url[:60]}...")
        else:
            print(f"   ⚠️  OTHER: {p.image_url[:60] if p.image_url else 'NO IMAGE'}...")
        print()
    
    # Count real vs fake
    all_products = Product.query.all()
    real = sum(1 for p in all_products if p.image_url and 'alicdn' in p.image_url)
    fake = sum(1 for p in all_products if p.image_url and 'placehold' in p.image_url)
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Real AliExpress images: {real}")
    print(f"   ❌ Fake/Placeholder images: {fake}")
    print(f"   📦 Total: {total}")
