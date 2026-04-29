#!/usr/bin/env python
"""
Fix product links to point to specific AliExpress products instead of search
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
from app import create_app, db
from app.models.database import Product

def fix_links():
    app = create_app()
    
    with app.app_context():
        print("Fixing product links to specific AliExpress products...")
        
        products = Product.query.all()
        print(f"Total products: {len(products)}")
        
        updated = 0
        for p in products:
            # Create specific AliExpress product URL using the product_id
            # Format: https://www.aliexpress.com/item/[product_id].html
            if p.product_id:
                # Use the actual product ID for a direct link
                p.product_url = f"https://www.aliexpress.com/item/{p.product_id}.html"
                
                # Create affiliate link format
                p.affiliate_url = f"https://www.aliexpress.com/item/{p.product_id}.html?aff_fcid=123&aff_fsk={p.product_id[:10]}"
                
                updated += 1
                
                if updated % 5000 == 0:
                    db.session.commit()
                    print(f"  Updated {updated} products...")
        
        db.session.commit()
        print(f"✅ Fixed {updated} products with specific AliExpress links!")
        
        # Show sample
        sample = Product.query.first()
        if sample:
            print(f"\nSample:")
            print(f"  Product: {sample.title_hebrew}")
            print(f"  Product URL: {sample.product_url}")
            print(f"  Affiliate URL: {sample.affiliate_url}")

if __name__ == '__main__':
    fix_links()
