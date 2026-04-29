#!/usr/bin/env python
"""
Test real AliExpress API with your credentials
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.api.aliexpress import AliExpressAPI

app = create_app()

with app.app_context():
    print("=" * 70)
    print("Testing Real AliExpress API")
    print("=" * 70)
    
    api = AliExpressAPI()
    
    print(f"\nAPI Key: {api.app_key}")
    print(f"Tracking ID: {api.tracking_id}")
    print(f"Base URL: {api.base_url}")
    
    # Test search
    print("\nTesting search for 'wireless earbuds'...")
    try:
        products = api.search_products("wireless earbuds", page_size=5)
        if products:
            print(f"✅ SUCCESS! Found {len(products)} products")
            print("\nFirst product:")
            p = products[0]
            print(f"  Title: {p['title']}")
            print(f"  Price: ${p['price']}")
            print(f"  Image: {p['image_url'][:60]}...")
            print(f"  Affiliate: {p['affiliate_url'][:60]}...")
        else:
            print("❌ No products found")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
