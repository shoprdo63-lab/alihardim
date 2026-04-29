#!/usr/bin/env python
"""
Fix all AliExpress product links to use proper search URLs
"""
import os
import urllib.parse
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product

def fix_all_links():
    app = create_app()
    
    with app.app_context():
        print("Fixing AliExpress product links...")
        
        products = Product.query.all()
        print(f"Total products: {len(products)}")
        
        updated = 0
        for p in products:
            # Create proper search URL using English title
            if p.title:
                search_term_en = urllib.parse.quote(p.title.replace(' ', '-'))
                search_term_he = urllib.parse.quote(p.title_hebrew or p.title)
                
                # New affiliate URL format
                p.affiliate_url = f"https://www.aliexpress.com/w/wholesale-{search_term_en}.html?sortType=bestmatch"
                
                # Fallback search URL
                p.product_url = f"https://www.aliexpress.com/wholesale?SearchText={search_term_he}"
                
                updated += 1
                
                if updated % 5000 == 0:
                    db.session.commit()
                    print(f"  Updated {updated} products...")
        
        db.session.commit()
        print(f"✅ Fixed {updated} products with new AliExpress links!")
        
        # Show sample
        sample = Product.query.first()
        if sample:
            print(f"\nSample product:")
            print(f"  Title: {sample.title_hebrew or sample.title}")
            print(f"  Product URL: {sample.product_url}")
            print(f"  Affiliate URL: {sample.affiliate_url}")

if __name__ == '__main__':
    fix_all_links()
