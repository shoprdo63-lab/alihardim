#!/usr/bin/env python
"""
Debug API - Save full response to file
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.api.aliexpress import aliexpress_api
import json

def debug_api():
    app = create_app()
    
    with app.app_context():
        print("🔍 Debugging API...")
        
        # Call API
        result = aliexpress_api._make_request('GET', {
            'method': 'aliexpress.affiliate.product.query',
            'keywords': 'bluetooth',
            'page_no': 1,
            'page_size': 5,
            'target_currency': 'USD',
            'target_language': 'EN',
            'tracking_id': aliexpress_api.tracking_id,
            'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url',
        })
        
        # Save to file
        with open('api_response.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("✅ Response saved to api_response.json")
        
        # Print summary
        if result:
            print(f"\nKeys in result: {list(result.keys())}")
            if 'resp_result' in result:
                resp = result['resp_result']
                print(f"resp_result keys: {list(resp.keys())}")
                if 'result' in resp:
                    data = resp['result']
                    print(f"result keys: {list(data.keys())}")

if __name__ == '__main__':
    debug_api()
