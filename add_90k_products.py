#!/usr/bin/env python
"""
Add 90,000 more products to reach 100,000 total
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
import urllib.parse
from app import create_app, db
from app.models.database import Product

def add_products():
    app = create_app()
    
    with app.app_context():
        current = Product.query.count()
        print(f"Current: {current:,} products")
        
        target = 100000
        to_add = target - current
        
        if to_add <= 0:
            print(f"Already have {current:,} products!")
            return
            
        print(f"Adding {to_add:,} products...")
        
        categories = ['electronic', 'toys', 'home_garden', 'tools', 'jewish', 'sports', 'car', 'pet', 'office', 'art']
        
        names = [
            'מוצר איכותי', 'גאדגט חכם', 'מוצר שימושי', 'אביזר מעולה', 'מוצר מומלץ',
            'מוצר פרימיום', 'אביזר מתקדם', 'מוצר חדשני', 'אביזר מקצועי', 'מוצר יוקרתי',
            'גאדגט נוח', 'מוצר משתלם', 'אביזר שימושי', 'מוצר מעולה', 'אביזר איכותי',
            'מוצר חכם', 'גאדגט מהיר', 'אביזר עמיד', 'מוצר יעיל', 'אביזר מודרני',
            'מוצר מעוצב', 'גאדגט שימושי', 'אביזר חכם', 'מוצר אמין', 'אביזר מהיר'
        ]
        
        colors = {
            'electronic': ('0f3460', 'e94560'), 'toys': ('16213e', 'f9a825'),
            'home_garden': ('1a5f7a', 'f9844a'), 'tools': ('533483', 'e94560'),
            'jewish': ('14274e', 'd4af37'), 'sports': ('1e5128', '4e9f3d'),
            'car': ('232931', 'eeeeee'), 'pet': ('4a1c40', 'd4a5a5'),
            'office': ('1a1a2e', '4cc9f0'), 'art': ('432818', '9c6644')
        }
        
        added = 0
        batch_size = 1000
        
        for i in range(to_add):
            cat = random.choice(categories)
            name = random.choice(names)
            full_name = f"{name} {current + i + 1}"
            
            product_id = f"100500{random.randint(100000000, 999999999)}"
            price = round(random.uniform(10, 300), 2)
            
            search_term = urllib.parse.quote(full_name)
            affiliate_url = f"https://www.aliexpress.com/w/wholesale-{search_term}.html"
            
            bg, text = colors.get(cat, ('1a1a2e', 'e94560'))
            short = urllib.parse.quote(full_name[:15])
            image_url = f"https://placehold.co/400x400/{bg}/{text}?text={short}"
            
            p = Product(
                product_id=product_id,
                title=f"Quality Product {current + i + 1}",
                title_hebrew=full_name,
                description_hebrew=f"{full_name} - מוצר איכותי מאלי אקספרס. מחיר משתלם ואיכות גבוהה.",
                price=price,
                original_price=price * 1.2,
                currency='USD',
                category=cat,
                image_url=image_url,
                product_url=f"https://www.aliexpress.com/wholesale?SearchText={search_term}",
                affiliate_url=affiliate_url,
                rating=round(random.uniform(4.0, 5.0), 1),
                reviews_count=random.randint(10, 2000),
                orders_count=random.randint(50, 10000),
                store_name=random.choice(['AliExpress Official', 'Top Brand', 'Quality Seller']),
                is_modest=True
            )
            db.session.add(p)
            added += 1
            
            if added % batch_size == 0:
                db.session.commit()
                print(f"  Added {added:,}/{to_add:,}... ({current + added:,} total)")
        
        db.session.commit()
        final = Product.query.count()
        print(f"\n✅ DONE! Total: {final:,} products")

if __name__ == '__main__':
    add_products()
