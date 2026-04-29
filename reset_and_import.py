#!/usr/bin/env python
"""Reset database and import REAL products with REAL images"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product
from app.utils.seed_products import seed_products

app = create_app()

with app.app_context():
    print("=" * 60)
    print("🗑️  Clearing all old products...")
    print("=" * 60)
    
    # Delete all existing products
    count = Product.query.count()
    Product.query.delete()
    db.session.commit()
    
    print(f"✅ Deleted {count} old products with fake images")
    print()
    
    # Import real products
    print("=" * 60)
    print("🚀 Importing REAL products with REAL images...")
    print("=" * 60)
    
    seed_products()
    
    # Verify
    total = Product.query.count()
    print(f"\n📊 Total products now: {total}")
    
    # Show sample
    sample = Product.query.first()
    if sample:
        print(f"\n📌 Sample product:")
        print(f"   Title: {sample.title[:50]}")
        print(f"   Image: {sample.image_url[:70]}...")
