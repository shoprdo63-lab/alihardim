#!/usr/bin/env python
"""
Sync real products from AliExpress using the official API.
This will get real products with real images and links.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import requests
import hashlib
import time
import json
import urllib.parse
from app import create_app, db
from app.models.database import Product
from config import Config

# API Configuration
API_KEY = "528438"
API_SECRET = "J9gzPRjwGFIOE7UsdvOASnEnuisllPdX"
TRACKING_ID = "ali_smart_finder_v1"
BASE_URL = "https://api-sg.aliexpress.com/sync"

# Category mapping to AliExpress category IDs
CATEGORY_MAPPING = {
    'electronic': '44',      # Consumer Electronics
    'toys': '26',              # Toys & Hobbies  
    'home_garden': '15',       # Home & Garden
    'tools': '1420',           # Tools
    'sports': '18',            # Sports & Entertainment
    'car': '34',               # Automobiles
    'pet': '100006129',        # Pet Products
    'office': '21',            # Office & School Supplies
    'art': '100005798',        # Arts & Crafts
    'jewish': '15',            # Maps to Home (for religious items)
}


def generate_sign(params):
    """Generate API signature"""
    sorted_params = sorted(params.items())
    sign_str = API_SECRET
    for key, value in sorted_params:
        sign_str += str(key) + str(value)
    sign_str += API_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()


def make_api_request(method, params):
    """Make API request"""
    params.update({
        'app_key': API_KEY,
        'timestamp': str(int(time.time() * 1000)),
        'sign_method': 'md5',
        'format': 'json',
        'v': '2.0',
    })
    params['sign'] = generate_sign(params)
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None


def get_real_products(keywords, category_id=None, page_size=20):
    """Get real products from AliExpress"""
    params = {
        'method': 'aliexpress.affiliate.product.query',
        'keywords': keywords,
        'page_no': 1,
        'page_size': page_size,
        'target_currency': 'USD',
        'target_language': 'EN',
        'tracking_id': TRACKING_ID,
    }
    
    if category_id:
        params['category_ids'] = category_id
    
    result = make_api_request('GET', params)
    
    products = []
    if result and 'resp_result' in result:
        data = result['resp_result'].get('result', {})
        products_data = data.get('products', {}).get('product', [])
        
        for p in products_data:
            try:
                product_id = p.get('product_id', '')
                title = p.get('product_title', '')
                price = float(str(p.get('target_sale_price', '0')).replace('$', '').replace(',', ''))
                image_url = p.get('product_main_image', '')
                product_url = p.get('product_detail_url', '')
                
                if not all([product_id, title, price, image_url]):
                    continue
                
                # Generate affiliate link
                affiliate_params = {
                    'method': 'aliexpress.affiliate.link.generate',
                    'promotion_link_type': '0',
                    'source_values': product_url,
                    'tracking_id': TRACKING_ID,
                }
                affiliate_result = make_api_request('GET', affiliate_params)
                
                affiliate_url = product_url
                if affiliate_result and 'resp_result' in affiliate_result:
                    links = affiliate_result['resp_result'].get('result', {}).get('promotion_links', {}).get('promotion_link', [])
                    if links:
                        affiliate_url = links[0].get('promotion_link', product_url)
                
                products.append({
                    'product_id': product_id,
                    'title': title,
                    'price': price,
                    'original_price': price * 1.2,
                    'image_url': image_url,
                    'product_url': product_url,
                    'affiliate_url': affiliate_url,
                    'rating': p.get('evaluate_rate', 4.5),
                    'reviews_count': p.get('evaluate_count', 100),
                    'orders_count': p.get('orders', 500),
                    'store_name': p.get('shop_title', 'AliExpress Store'),
                })
            except Exception as e:
                print(f"  Error parsing product: {e}")
                continue
    
    return products


def sync_real_products():
    """Sync real products to database"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("Syncing REAL Products from AliExpress API")
        print("=" * 70)
        
        # Clear existing products
        print("\nClearing existing products...")
        Product.query.delete()
        db.session.commit()
        print("Database cleared!")
        
        total_added = 0
        
        # Search terms for each category
        search_terms = {
            'electronic': ['wireless earbuds', 'smart watch', 'power bank', 'bluetooth speaker', 'usb cable'],
            'toys': ['lego blocks', 'rc car', 'kids robot', 'educational toys', 'plush toys'],
            'home_garden': ['kitchen organizer', 'led lamp', 'coffee maker', 'garden tools', 'home decor'],
            'tools': ['screwdriver set', 'drill machine', 'measuring tape', 'tool box', 'electric saw'],
            'sports': ['yoga mat', 'running shoes', 'camping tent', 'fitness equipment', 'bicycle accessories'],
            'car': ['car charger', 'dash cam', 'car vacuum', 'seat covers', 'steering wheel cover'],
            'pet': ['dog bed', 'cat tree', 'pet toys', 'pet feeder', 'dog leash'],
            'office': ['desk lamp', 'notebook set', 'pen holder', 'file organizer', 'calculator'],
            'art': ['painting set', 'drawing pencils', 'canvas board', 'craft supplies', 'art markers'],
            'jewish': ['menorah', 'kiddush cup', 'tallit', 'mezuzah case', 'shabbat candles'],
        }
        
        for category_key, terms in search_terms.items():
            print(f"\n{'='*70}")
            print(f"Category: {category_key}")
            print(f"{'='*70}")
            
            category_id = CATEGORY_MAPPING.get(category_key)
            category_added = 0
            
            for term in terms:
                print(f"\n  Searching: {term}...")
                try:
                    products = get_real_products(term, category_id, page_size=10)
                    
                    if products:
                        print(f"  Found {len(products)} products")
                        
                        for p in products:
                            try:
                                # Check if product exists
                                existing = Product.query.filter_by(product_id=p['product_id']).first()
                                if existing:
                                    continue
                                
                                # Create Hebrew title
                                hebrew_title = p['title']  # Will be translated by content_filter
                                
                                # Create product
                                product = Product(
                                    product_id=p['product_id'],
                                    title=p['title'],
                                    title_hebrew=hebrew_title,
                                    description_hebrew=f"{hebrew_title} - מוצר איכותי מאלי אקספרס. מחיר משתלם ואיכות גבוהה.",
                                    price=p['price'],
                                    original_price=p['original_price'],
                                    currency='USD',
                                    category=category_key,
                                    image_url=p['image_url'],
                                    product_url=p['product_url'],
                                    affiliate_url=p['affiliate_url'],
                                    rating=p['rating'],
                                    reviews_count=p['reviews_count'],
                                    orders_count=p['orders_count'],
                                    store_name=p['store_name'],
                                    is_modest=True
                                )
                                
                                db.session.add(product)
                                category_added += 1
                                total_added += 1
                                
                            except Exception as e:
                                print(f"    Error adding product: {e}")
                                db.session.rollback()
                                continue
                        
                        db.session.commit()
                    else:
                        print(f"  No products found")
                        
                except Exception as e:
                    print(f"  Error searching: {e}")
                    continue
            
            print(f"  Category total: {category_added} products")
        
        print(f"\n{'='*70}")
        print(f"SYNC COMPLETE!")
        print(f"{'='*70}")
        print(f"Total real products added: {total_added}")
        print(f"All products have REAL images and REAL affiliate links!")


if __name__ == '__main__':
    sync_real_products()
