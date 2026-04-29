#!/usr/bin/env python
"""
Test AliExpress API with real credentials
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.api.aliexpress import aliexpress_api

def test_api():
    app = create_app()
    
    with app.app_context():
        print("Testing AliExpress API...")
        print(f"App Key: {aliexpress_api.app_key}")
        print(f"Tracking ID: {aliexpress_api.tracking_id}")
        
        # Test search
        try:
            results = aliexpress_api.search_products("bluetooth headphones", 10)
            print(f"\n✅ API Working! Found {len(results)} products")
            
            if results:
                print("\nSample product:")
                p = results[0]
                print(f"  ID: {p.get('product_id')}")
                print(f"  Title: {p.get('title')}")
                print(f"  Price: ${p.get('price')}")
                print(f"  URL: {p.get('affiliate_url')}")
            
            return True
        except Exception as e:
            print(f"\n❌ API Error: {e}")
            return False

if __name__ == '__main__':
    test_api()
