#!/usr/bin/env python
"""
Test AliExpress API - Raw response without filtering
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.api.aliexpress import aliexpress_api

def test_api_raw():
    app = create_app()
    
    with app.app_context():
        print("Testing AliExpress API (raw)...")
        print(f"App Key: {aliexpress_api.app_key}")
        print(f"Tracking ID: {aliexpress_api.tracking_id}")
        
        # Make raw API call
        params = {
            'method': 'aliexpress.affiliate.product.query',
            'keywords': 'headphones',
            'page_no': 1,
            'page_size': 10,
            'target_currency': 'USD',
            'target_language': 'EN',
            'tracking_id': aliexpress_api.tracking_id,
            'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title,discount',
        }
        
        result = aliexpress_api._make_request('GET', params)
        
        print(f"\nRaw API Result:")
        print(f"Keys: {result.keys() if result else 'No result'}")
        
        if result and 'resp_result' in result:
            resp = result['resp_result']
            print(f"Response result keys: {resp.keys() if resp else 'No resp_result'}")
            
            if 'result' in resp:
                data = resp['result']
                print(f"Data keys: {data.keys() if data else 'No data'}")
                
                if 'products' in data:
                    products = data['products']
                    print(f"Products keys: {products.keys() if products else 'No products'}")
                    
                    if 'product' in products:
                        product_list = products['product']
                        print(f"\n✅ Found {len(product_list)} products!")
                        
                        for i, p in enumerate(product_list[:3]):
                            print(f"\nProduct {i+1}:")
                            print(f"  ID: {p.get('product_id')}")
                            print(f"  Title: {p.get('product_title', '')[:50]}")
                            print(f"  Price: {p.get('target_sale_price', p.get('sale_price', 'N/A'))}")
                            print(f"  URL: {p.get('product_detail_url', '')[:60]}")
                    else:
                        print("\n❌ No 'product' key in products")
                else:
                    print("\n❌ No 'products' key in data")
            else:
                print("\n❌ No 'result' in resp_result")
        else:
            print("\n❌ No 'resp_result' in result")
            print(f"Full result: {result}")

if __name__ == '__main__':
    test_api_raw()
