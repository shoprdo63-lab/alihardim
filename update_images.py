#!/usr/bin/env python
"""
Update all product images to use styled placeholders with product names.
This creates beautiful product cards even without real AliExpress images.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import urllib.parse
from app import create_app, db
from app.models.database import Product

# Color schemes for different categories
CATEGORY_COLORS = {
    'electronic': ('0f3460', 'e94560'),      # Dark blue + Red
    'toys': ('16213e', 'f9a825'),              # Navy + Gold
    'home_garden': ('1a5f7a', 'f9844a'),     # Teal + Orange
    'tools': ('533483', 'e94560'),             # Purple + Red
    'jewish': ('14274e', 'd4af37'),            # Dark blue + Gold
    'sports': ('1e5128', '4e9f3d'),            # Green tones
    'car': ('232931', '393e46'),                # Gray tones
    'pet': ('4a1c40', 'd4a5a5'),               # Purple-pink
    'office': ('1a1a2e', '4cc9f0'),            # Dark + Light blue
    'art': ('432818', '9c6644'),               # Brown tones
}


def update_images():
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("Updating Product Images to Styled Placeholders")
        print("=" * 70)
        
        products = Product.query.all()
        total = len(products)
        print(f"Total products: {total}")
        print()
        
        updated = 0
        
        for i, product in enumerate(products, 1):
            try:
                category = product.category
                if category in CATEGORY_COLORS:
                    bg_color, text_color = CATEGORY_COLORS[category]
                else:
                    bg_color, text_color = ('1a1a2e', 'e94560')
                
                # Create styled placeholder image URL
                # Using placehold.co for beautiful styled images
                title_short = (product.title_hebrew or product.title)[:25]
                encoded_title = urllib.parse.quote(title_short)
                
                # Create image with category colors and product name
                product.image_url = f"https://placehold.co/400x400/{bg_color}/{text_color}?text={encoded_title}"
                
                # Also ensure affiliate URL is proper AliExpress search
                search_term = urllib.parse.quote(product.title_hebrew or product.title)
                product.affiliate_url = f"https://www.aliexpress.com/w/wholesale-{search_term}.html?sortType=bestmatch"
                product.product_url = f"https://www.aliexpress.com/wholesale?SearchText={search_term}"
                
                updated += 1
                
                if i % 500 == 0:
                    db.session.commit()
                    print(f"  Updated {i}/{total} products...")
                    
            except Exception as e:
                print(f"  Error: {e}")
                db.session.rollback()
                continue
        
        db.session.commit()
        
        print(f"\n{'='*70}")
        print(f"Updated {updated} products with styled images!")
        print(f"{'='*70}")
        
        # Show examples
        print("\nExample products:")
        for cat in ['electronic', 'toys', 'home_garden']:
            p = Product.query.filter_by(category=cat).first()
            if p:
                print(f"\n  Category: {cat}")
                print(f"  Title: {p.title_hebrew or p.title}")
                print(f"  Image: {p.image_url}")
                print(f"  Link: {p.affiliate_url[:60]}...")


if __name__ == '__main__':
    update_images()
