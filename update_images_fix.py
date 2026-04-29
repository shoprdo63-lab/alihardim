#!/usr/bin/env python
"""
Fix image URLs for all products - use English instead of Hebrew
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product

# Category colors
CATEGORY_COLORS = {
    'electronic': ('0f3460', 'e94560'),
    'toys': ('16213e', 'f9a825'),
    'home_garden': ('1a5f7a', 'f9844a'),
    'tools': ('533483', 'e94560'),
    'jewish': ('14274e', 'd4af37'),
    'sports': ('1e5128', '4e9f3d'),
    'car': ('232931', 'eeeeee'),
    'pet': ('4a1c40', 'd4a5a5'),
    'office': ('1a1a2e', '4cc9f0'),
    'art': ('432818', '9c6644'),
}


def fix_images():
    app = create_app()
    
    with app.app_context():
        print("Fixing product images...")
        
        products = Product.query.all()
        print(f"Total products: {len(products)}")
        
        updated = 0
        for p in products:
            # Generate new image URL with English text
            bg, text = CATEGORY_COLORS.get(p.category, ('1a1a2e', 'e94560'))
            
            # Use English title for image
            if p.title:
                short_title = p.title[:20].replace(' ', '+')
            else:
                short_title = 'Product'
            
            p.image_url = f"https://placehold.co/400x400/{bg}/{text}?text={short_title}"
            updated += 1
            
            if updated % 1000 == 0:
                db.session.commit()
                print(f"  Updated {updated} products...")
        
        db.session.commit()
        print(f"✅ Fixed {updated} products with new images!")


if __name__ == '__main__':
    fix_images()
