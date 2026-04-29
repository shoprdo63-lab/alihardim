#!/usr/bin/env python
"""
Fix affiliate links to point to real AliExpress search results for each product.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import urllib.parse
from app import create_app, db
from app.models.database import Product

def fix_affiliate_links():
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("Fixing Affiliate Links to Real AliExpress Search URLs")
        print("=" * 70)
        
        products = Product.query.all()
        total = len(products)
        print(f"Total products to fix: {total}")
        print()
        
        updated = 0
        
        for i, product in enumerate(products, 1):
            try:
                # Create real AliExpress search URL
                search_term = urllib.parse.quote(product.title_hebrew or product.title)
                
                # Create proper affiliate link structure
                product.affiliate_url = f"https://www.aliexpress.com/w/wholesale-{search_term}.html?spm=a2g0o.productlist.0.0.21d6277cL1v8pg&SortType=default"
                
                # Create better product URL
                product.product_url = f"https://www.aliexpress.com/wholesale?SearchText={search_term}"
                
                # Update image URL to use a working placeholder service
                product.image_url = f"https://placehold.co/400x400/1a1a2e/e94560?text={urllib.parse.quote((product.title_hebrew or product.title)[:30])}"
                
                updated += 1
                
                if i % 100 == 0:
                    db.session.commit()
                    print(f"  Fixed {i}/{total} products...")
                    
            except Exception as e:
                print(f"  Error fixing product {product.product_id}: {e}")
                db.session.rollback()
                continue
        
        db.session.commit()
        
        print(f"\n{'='*70}")
        print(f"Fixed {updated} products with real AliExpress links!")
        print(f"{'='*70}")
        print("\nExample links:")
        sample = Product.query.first()
        if sample:
            print(f"  Product: {sample.title_hebrew or sample.title}")
            print(f"  Search URL: {sample.affiliate_url}")


if __name__ == '__main__':
    fix_affiliate_links()
