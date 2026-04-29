#!/usr/bin/env python
"""
Initialize database with tables and default categories.
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Category
from config import Config

def init_database():
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if categories already exist
        existing = Category.query.first()
        if existing:
            print("Categories already initialized.")
            return
        
        print("Initializing categories...")
        
        # Add categories with icons
        categories_data = [
            {'key': 'electronic', 'name_hebrew': "גאדג'טים ואלקטרוניקה", 'name_english': 'Electronics & Gadgets', 'icon': 'laptop', 'sort_order': 1},
            {'key': 'toys', 'name_hebrew': 'צעצועים לילדים', 'name_english': 'Toys for Kids', 'icon': 'toy-brick', 'sort_order': 2},
            {'key': 'home_garden', 'name_hebrew': 'בית וגן', 'name_english': 'Home & Garden', 'icon': 'house-door', 'sort_order': 3},
            {'key': 'tools', 'name_hebrew': 'כלי עבודה וDIY', 'name_english': 'Tools & DIY', 'icon': 'tools', 'sort_order': 4},
            {'key': 'jewish', 'name_hebrew': 'אביזרי יהדות', 'name_english': 'Jewish Items', 'icon': 'star-fill', 'sort_order': 5},
            {'key': 'sports', 'name_hebrew': 'ספורט וקמפינג', 'name_english': 'Sports & Camping', 'icon': 'bicycle', 'sort_order': 6},
            {'key': 'car', 'name_hebrew': 'רכב ואביזרים', 'name_english': 'Car Accessories', 'icon': 'car-front', 'sort_order': 7},
            {'key': 'pet', 'name_hebrew': 'חיות מחמד', 'name_english': 'Pet Supplies', 'icon': 'heart', 'sort_order': 8},
            {'key': 'office', 'name_hebrew': 'כלי כתיבה ומשרד', 'name_english': 'Office Supplies', 'icon': 'pencil', 'sort_order': 9},
            {'key': 'art', 'name_hebrew': 'אמנות ויצירה', 'name_english': 'Art & Crafts', 'icon': 'palette', 'sort_order': 10},
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data, is_active=True)
            db.session.add(category)
            print(f"  Added: {cat_data['name_hebrew']}")
        
        db.session.commit()
        print(f"\nSuccessfully added {len(categories_data)} categories!")
        print("\nDatabase initialized successfully!")
        print("Next step: Run 'python sync_products.py' to load products from AliExpress.")

if __name__ == '__main__':
    init_database()
