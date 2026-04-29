#!/usr/bin/env python
"""
Debug API response
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
            'page_size': 10,
            'target_currency': 'USD',
            'target_language': 'EN',
            'tracking_id': aliexpress_api.tracking_id,
            'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title,discount',
        })
        
        print("\n" + "="*60)
        print("RAW API RESPONSE:")
        print("="*60)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
        
        # Navigate through structure
        if 'resp_result' in result:
            resp = result['resp_result']
            print(f"\n✅ resp_result found!")
            print(f"   resp_code: {resp.get('resp_code')}")
            print(f"   resp_msg: {resp.get('resp_msg')}")
            
            if 'result' in resp:
                data = resp['result']
                print(f"\n✅ result found!")
                print(f"   Keys: {list(data.keys())}")
                
                if 'products' in data:
                    products = data['products']
                    print(f"\n✅ products found!")
                    print(f"   Keys: {list(products.keys())}")
                    
                    if 'product' in products:
                        product_list = products['product']
                        print(f"\n✅ product array found! Count: {len(product_list)}")
                    else:
                        print("\n❌ No 'product' key in products")
                        print(f"   Full products: {products}")
                else:
                    print("\n❌ No 'products' key in result")
            else:
                print("\n❌ No 'result' key in resp_result")
        else:
            print("\n❌ No 'resp_result' in result")

if __name__ == '__main__':
    debug_api()
