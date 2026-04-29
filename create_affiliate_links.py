#!/usr/bin/env python
"""
Create proper AliExpress affiliate links for existing products
Using the tracking ID provided by user
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models.database import Product

# The user's tracking ID
TRACKING_ID = "ali_smart_finder_v1"


def create_affiliate_links():
    app = create_app()
    
    with app.app_context():
        print("Creating AliExpress affiliate links...")
        print(f"Tracking ID: {TRACKING_ID}")
        
        products = Product.query.all()
        print(f"Total products: {len(products)}")
        
        updated = 0
        for p in products:
            # Create affiliate link using tracking ID
            # Format: https://s.click.aliexpress.com/e/_d[tracking_params]
            
            # Option 1: Use product ID if we have real one
            if p.product_id and len(p.product_id) > 10:
                # Real AliExpress product ID format
                p.affiliate_url = f"https://s.click.aliexpress.com/e/_d{TRACKING_ID}_{p.product_id[:10]}"
            else:
                # Search-based link
                search_term = p.title.replace(' ', '-')[:30] if p.title else 'product'
                p.affiliate_url = f"https://s.click.aliexpress.com/e/_d{TRACKING_ID}?search={search_term}"
            
            # Also update product URL to be proper search
            if p.title:
                search_term = p.title.replace(' ', '+')
                p.product_url = f"https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20240101000000&SearchText={search_term}"
            
            updated += 1
            
            if updated % 5000 == 0:
                db.session.commit()
                print(f"  Updated {updated} products...")
        
        db.session.commit()
        print(f"✅ Updated {updated} products with affiliate links!")
        
        # Show sample
        sample = Product.query.first()
        if sample:
            print(f"\nSample:")
            print(f"  Title: {sample.title_hebrew or sample.title}")
            print(f"  Product URL: {sample.product_url}")
            print(f"  Affiliate URL: {sample.affiliate_url}")


if __name__ == '__main__':
    create_affiliate_links()
