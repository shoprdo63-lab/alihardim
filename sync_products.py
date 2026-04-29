#!/usr/bin/env python
"""
Sync products from AliExpress API to local database.
Fetches thousands of products across multiple categories and keywords.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import time
from app import create_app, db
from app.models.database import Product
from app.api.aliexpress import aliexpress_api
from app.services.content_filter import is_modest_product, translate_to_hebrew, generate_hebrew_description
from config import Config

def sync_products():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("AliExpress Product Sync Tool")
        print("=" * 60)
        
        # Keywords for each category (extensive list for thousands of products)
        category_keywords = {
            'electronic': [
                'smartphone', 'tablet', 'laptop', 'headphones', 'wireless earbuds', 'charger', 
                'usb cable', 'power bank', 'bluetooth speaker', 'smart watch', 'mouse', 
                'keyboard', 'webcam', 'memory card', 'phone case', 'screen protector',
                'gaming controller', 'wifi router', 'security camera', 'led strip'
            ],
            'toys': [
                'lego', 'building blocks', 'educational toy', 'puzzle', 'board game',
                'remote control car', 'toy robot', 'dinosaur toy', 'stuffed animal',
                'action figure', 'toy train', 'craft kit', 'slime kit', 'magic set'
            ],
            'home_garden': [
                'kitchen organizer', 'storage box', 'food container', 'led lamp', 'desk lamp',
                'wall shelf', 'coat hook', 'trash bin', 'laundry basket', 'garden tools',
                'plant pot', 'watering can', 'bbq grill', 'camping chair', 'cooler box'
            ],
            'tools': [
                'cordless drill', 'screwdriver set', 'tool box', 'wrench set', 'pliers',
                'hammer', 'tape measure', 'level tool', 'utility knife', 'soldering iron',
                'multimeter', 'work light', 'tool belt', 'saw', 'electric grinder'
            ],
            'jewish': [
                'kippah', 'tzitzit', 'tallit', 'menorah', 'hanukkah', 'dreidel', 'mezuzah',
                'siddur', 'jewish calendar', 'shabbat candlesticks', 'kiddush cup', ' challah board'
            ],
            'sports': [
                'camping tent', 'sleeping bag', 'backpack', 'water bottle', 'bicycle light',
                'fishing rod', 'basketball', 'soccer ball', 'resistance bands', 'yoga mat',
                'dumbbell set', 'jump rope', 'frisbee', 'camping stove', 'hiking boots'
            ],
            'car': [
                'car phone holder', 'car charger', 'car vacuum', 'car organizer', 'car cover',
                'steering wheel cover', 'car cleaning kit', 'tire inflator', 'dash cam',
                'car seat cover', 'car air freshener', 'car tool kit', 'emergency kit'
            ],
            'pet': [
                'dog toy', 'cat toy', 'pet bed', 'pet bowl', 'dog leash', 'cat scratcher',
                'pet carrier', 'grooming kit', 'pet brush', 'training treats', 'pet collar'
            ],
            'office': [
                'notebook', 'pen set', 'pencil case', 'stapler', 'desk organizer', 'file folder',
                'whiteboard', 'marker set', 'calculator', 'document tray', 'tape dispenser'
            ],
            'art': [
                'acrylic paint', 'watercolor set', 'canvas board', 'paint brush set', 'sketchbook',
                'colored pencils', 'oil pastels', 'craft glue', 'scissors', 'beads kit'
            ],
        }
        
        total_added = 0
        total_skipped = 0
        
        for category_key, keywords in category_keywords.items():
            print(f"\n{'='*60}")
            print(f"Category: {Config.SAFE_CATEGORIES.get(category_key, category_key)}")
            print(f"{'='*60}")
            
            category_added = 0
            
            for keyword in keywords:
                print(f"\n  Searching: '{keyword}'...")
                
                try:
                    # Fetch products from API
                    api_products = aliexpress_api.search_products(
                        keywords=keyword,
                        page_size=20,
                        max_price=100  # Focus on affordable products
                    )
                    
                    if not api_products:
                        print(f"    No products found for '{keyword}'")
                        continue
                    
                    print(f"    Found {len(api_products)} products")
                    
                    added_for_keyword = 0
                    skipped_for_keyword = 0
                    
                    for api_product in api_products:
                        # Check if product already exists
                        existing = Product.query.filter_by(
                            product_id=api_product['product_id']
                        ).first()
                        
                        if existing:
                            skipped_for_keyword += 1
                            total_skipped += 1
                            continue
                        
                        # Double-check modesty filter
                        if not is_modest_product(api_product['title']):
                            skipped_for_keyword += 1
                            total_skipped += 1
                            continue
                        
                        try:
                            # Generate Hebrew content
                            hebrew_title, _ = translate_to_hebrew(api_product['title'])
                            hebrew_desc = generate_hebrew_description({
                                'title': api_product['title'],
                                'category': category_key
                            })
                            
                            # Create product
                            product = Product(
                                product_id=api_product['product_id'],
                                title=api_product['title'],
                                title_hebrew=hebrew_title,
                                description_hebrew=hebrew_desc,
                                price=api_product['price'],
                                original_price=api_product.get('original_price'),
                                currency='USD',
                                category=category_key,
                                image_url=api_product['image_url'],
                                product_url=api_product['product_url'],
                                affiliate_url=api_product.get('affiliate_url', api_product['product_url']),
                                rating=api_product.get('rating'),
                                store_name=api_product.get('store_name', ''),
                                is_modest=True
                            )
                            
                            db.session.add(product)
                            added_for_keyword += 1
                            category_added += 1
                            total_added += 1
                            
                        except Exception as e:
                            print(f"    Error adding product: {e}")
                            db.session.rollback()
                            continue
                    
                    # Commit after each keyword
                    db.session.commit()
                    print(f"    Added: {added_for_keyword}, Skipped: {skipped_for_keyword}")
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"    API Error for '{keyword}': {e}")
                    db.session.rollback()
                    continue
            
            print(f"\n  Category total added: {category_added}")
        
        print(f"\n{'='*60}")
        print("SYNC COMPLETE!")
        print(f"{'='*60}")
        print(f"Total products added: {total_added}")
        print(f"Total products skipped: {total_skipped}")
        print(f"{'='*60}")
        
        # Show breakdown by category
        print("\nProducts by category:")
        for key, name in Config.SAFE_CATEGORIES.items():
            count = Product.query.filter_by(category=key).count()
            print(f"  {name}: {count}")

if __name__ == '__main__':
    sync_products()
