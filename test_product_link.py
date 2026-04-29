#!/usr/bin/env python
"""Test if product links are correct"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.models.database import Product

app = create_app()

with app.app_context():
    # Get first 5 products
    products = Product.query.limit(5).all()
    
    print("Testing product links:\n")
    
    for i, p in enumerate(products, 1):
        print(f"{i}. {p.title[:50]}...")
        print(f"   Product ID: {p.product_id}")
        print(f"   Product URL: {p.product_url}")
        print(f"   Affiliate URL: {p.affiliate_url}")
        
        # Build direct link
        direct_link = f"https://www.aliexpress.com/item/{p.product_id}.html"
        print(f"   Direct Link: {direct_link}")
        
        # Check if ID looks valid (should be numeric or start with specific patterns)
        if p.product_id and p.product_id.isdigit():
            print(f"   ✅ ID is numeric")
        elif p.product_id and (p.product_id.startswith('100500') or p.product_id.startswith('32568')):
            print(f"   ✅ ID looks like AliExpress format")
        else:
            print(f"   ⚠️  ID format unclear: {p.product_id}")
        
        print()
