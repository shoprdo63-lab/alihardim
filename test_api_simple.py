#!/usr/bin/env python
"""
Test API with disabled content filter
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from app.api.aliexpress import aliexpress_api
from app.services.content_filter import is_modest_product

def test_api():
    app = create_app()
    
    with app.app_context():
        print("Testing API without content filter...")
        print(f"App Key: {aliexpress_api.app_key}")
        print(f"Tracking ID: {aliexpress_api.tracking_id}")
        
        # Test modest filter
        print(f"\nModest filter test: {is_modest_product('sexy lingerie')} (should be True now)")
        
        # Call API
        result = aliexpress_api._make_request('GET', {
            'method': 'aliexpress.affiliate.product.query',
            'keywords': 'bluetooth headphones',
            'page_no': 1,
            'page_size': 10,
            'target_currency': 'USD',
            'target_language': 'EN',
            'tracking_id': aliexpress_api.tracking_id,
            'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title,discount',
        })
        
        if not result or 'resp_result' not in result:
            print(f"\n❌ No API response")
            print(f"Result: {result}")
            return
        
        data = result['resp_result'].get('result', {})
        products_data = data.get('products', {}).get('product', [])
        
        print(f"\n✅ API returned {len(products_data)} products!")
        
        if products_data:
            print("\nFirst 3 products:")
            for i, p in enumerate(products_data[:3]):
                print(f"\n{i+1}. {p.get('product_title', 'N/A')[:50]}")
                print(f"   ID: {p.get('product_id', 'N/A')}")
                print(f"   Price: {p.get('target_sale_price', 'N/A')}")
                print(f"   Image: {p.get('product_main_image', 'N/A')[:60]}...")

if __name__ == '__main__':
    test_api()
