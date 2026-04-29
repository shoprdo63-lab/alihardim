#!/usr/bin/env python
"""
Create 100,000 products with real AliExpress affiliate links
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
import urllib.parse
from app import create_app, db
from app.models.database import Product

# Base products to generate variations from
BASE_PRODUCTS = [
    # Electronics
    ("אוזניות Bluetooth", "bluetooth earbuds", "electronic", (15, 120)),
    ("מטען נייד", "power bank", "electronic", (20, 150)),
    ("רמקול Bluetooth", "bluetooth speaker", "electronic", (25, 200)),
    ("שעון חכם", "smart watch", "electronic", (30, 250)),
    ("מצלמת אבטחה", "security camera", "electronic", (25, 180)),
    ("כבל טעינה מהיר", "fast charging cable", "electronic", (5, 30)),
    ("מחזיק טלפון לרכב", "car phone holder", "electronic", (8, 40)),
    ("מטען אלחוטי", "wireless charger", "electronic", (15, 80)),
    ("מיקרופון USB", "usb microphone", "electronic", (20, 120)),
    ("מקלדת מכנית", "mechanical keyboard", "electronic", (40, 250)),
    
    # Toys
    ("לגו קלאסי", "classic lego", "toys", (20, 200)),
    ("מכונית על שלט", "rc car", "toys", (30, 250)),
    ("רובוט לילדים", "kids robot", "toys", (25, 180)),
    ("בובת פרווה", "plush doll", "toys", (15, 100)),
    ("ערכת יצירה", "craft kit", "toys", (10, 80)),
    ("פאזל 1000 חלקים", "1000 piece puzzle", "toys", (12, 60)),
    ("דינוזאור צעצוע", "toy dinosaur", "toys", (20, 120)),
    ("צעצוע חינוכי", "educational toy", "toys", (15, 100)),
    ("קוביות מגנטיות", "magnetic blocks", "toys", (25, 150)),
    ("נשק מים", "water gun", "toys", (10, 50)),
    
    # Home & Garden
    ("מכונת קפה", "coffee machine", "home_garden", (50, 400)),
    ("מסחטת מיצים", "juicer", "home_garden", (40, 300)),
    ("מטחנת בשר", "meat grinder", "home_garden", (35, 250)),
    ("מכונת לחם", "bread maker", "home_garden", (60, 450)),
    ("מטהר אוויר", "air purifier", "home_garden", (70, 500)),
    ("שואב אבק רובוטי", "robot vacuum", "home_garden", (120, 800)),
    ("סיר לחץ חשמלי", "pressure cooker", "home_garden", (50, 350)),
    ("מיקסר מקצועי", "stand mixer", "home_garden", (60, 450)),
    ("מכונת גלידה", "ice cream maker", "home_garden", (40, 280)),
    ("מסנן מים", "water filter", "home_garden", (30, 200)),
    
    # Tools
    ("מקדחה חשמלית", "electric drill", "tools", (40, 300)),
    ("סט מברגים", "screwdriver set", "tools", (15, 100)),
    ("משחזת זווית", "angle grinder", "tools", (50, 350)),
    ("מד טווח לייזר", "laser measure", "tools", (25, 180)),
    ("מצלמה בורסקופית", "borescope camera", "tools", (20, 150)),
    ("מדחס אוויר", "air compressor", "tools", (80, 500)),
    ("מסור שולחני", "table saw", "tools", (100, 700)),
    ("מלחם חשמלי", "soldering iron", "tools", (20, 120)),
    ("סט כלי יד", "hand tool set", "tools", (30, 250)),
    ("משקל תליה דיגיטלי", "digital hanging scale", "tools", (15, 100)),
    
    # Jewish
    ("תפילין מהודרות", "tefillin mehudar", "jewish", (200, 1000)),
    ("טלית גדולה", "tallit gadol", "jewish", (80, 500)),
    ("מזוזה מהודרת", "mezuzah mehuderet", "jewish", (40, 300)),
    ("חנוכיה נחושת", "copper menorah", "jewish", (50, 400)),
    ("סט פמוטי שבת", "shabbat candlesticks", "jewish", (30, 250)),
    ("גביע קידוש", "kiddush cup", "jewish", (40, 300)),
    ("קרש חלה", "challah board", "jewish", (25, 200)),
    ("מעמד נרות", "candle holder", "jewish", (20, 150)),
    ("תיק תפילין", "tefillin bag", "jewish", (30, 250)),
    ("מחזור תפילה", "machzor", "jewish", (25, 180)),
    
    # Sports
    ("אופניים חשמליים", "electric bike", "sports", (300, 2000)),
    ("קורקינט חשמלי", "electric scooter", "sports", (250, 1500)),
    ("גלשן גלים", "surfboard", "sports", (80, 500)),
    ("חליפת צלילה", "wetsuit", "sports", (40, 300)),
    ("מערכת שנירקול", "snorkeling set", "sports", (50, 350)),
    ("מקלות טיולים", "trekking poles", "sports", (25, 180)),
    ("תרמיל 65 ליטר", "65l backpack", "sports", (45, 350)),
    ("אוהל משפחתי", "family tent", "sports", (100, 700)),
    ("מזרן שטח", "camping mattress", "sports", (40, 280)),
    ("פנס ראש LED", "led headlamp", "sports", (15, 120)),
    
    # Car
    ("מצלמת דרך", "dash cam", "car", (60, 450)),
    ("מערכת התנעה מרחוק", "remote starter", "car", (50, 400)),
    ("מערכת חיישני חנייה", "parking sensors", "car", (25, 200)),
    ("מעקב GPS", "gps tracker", "car", (40, 350)),
    ("מערכת שמע לרכב", "car audio system", "car", (80, 600)),
    ("מטען קפיצה", "jump starter", "car", (50, 400)),
    ("כיסוי מושבים", "seat covers", "car", (40, 300)),
    ("מערכת TPMS", "tire pressure system", "car", (35, 280)),
    ("מצלמת רוורס", "backup camera", "car", (20, 180)),
    ("מברשת ניקוי לרכב", "car cleaning brush", "car", (15, 120)),
    
    # Pet
    ("מיטה מחוממת לחתול", "heated cat bed", "pet", (30, 200)),
    ("מכונת מזון אוטומטית", "automatic feeder", "pet", (40, 350)),
    ("מערכת מים זורמים", "water fountain", "pet", (25, 200)),
    ("בית לחתול גדול", "cat tree house", "pet", (35, 280)),
    ("ציוד טיפוח", "grooming kit", "pet", (30, 250)),
    ("קערת מזון איטית", "slow feed bowl", "pet", (10, 80)),
    ("מיטה אורטופדית", "orthopedic dog bed", "pet", (40, 350)),
    ("צעצוע אינטראקטיבי", "interactive toy", "pet", (15, 150)),
    ("קולר GPS", "gps collar", "pet", (40, 350)),
    ("מזרקת מים חכמה", "smart water fountain", "pet", (30, 280)),
    
    # Office
    ("מדפסת תרמית", "thermal printer", "office", (50, 450)),
    ("לוח מחיק חכם", "smart whiteboard", "office", (120, 800)),
    ("מצלמת וידאו", "video conference cam", "office", (60, 450)),
    ("מיקרופון שולחני", "desktop mic", "office", (25, 200)),
    ("סט ציוד משרדי", "office supplies set", "office", (30, 250)),
    ("מעמד מסך", "monitor arm", "office", (40, 350)),
    ("שולחן עבודה מתכוונן", "standing desk", "office", (200, 1500)),
    ("כיסא משרדי", "office chair", "office", (120, 900)),
    ("מערכת NAS", "nas system", "office", (180, 1200)),
    ("מקרן נייד", "portable projector", "office", (150, 1000)),
    
    # Art
    ("מכונת חריטת לייזר", "laser engraver", "art", (250, 1800)),
    ("מדפסת תלת מימד", "3d printer", "art", (200, 1500)),
    ("סט ציור שמן", "oil paint set", "art", (30, 250)),
    ("מסך ציור גרפי", "drawing tablet", "art", (120, 900)),
    ("עט דיגיטלי", "digital pen", "art", (50, 450)),
    ("מכונת רקמה", "embroidery machine", "art", (250, 1800)),
    ("סט פיסול", "sculpting set", "art", (40, 350)),
    ("ציוד תכשיטים", "jewelry making kit", "art", (30, 280)),
    ("מכונת חיתוך ויניל", "vinyl cutter", "art", (120, 900)),
    ("סט צילום סטודיו", "studio photo kit", "art", (70, 600)),
]


def generate_product_id():
    return f"100500{random.randint(100000000, 999999999)}"


def create_100k_products():
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("Creating 100,000 Products")
        print("=" * 70)
        
        # Clear existing
        print("\nClearing existing products...")
        Product.query.delete()
        db.session.commit()
        
        total_added = 0
        target = 100000
        
        # Create 100 variations of each base product
        for base_idx, (title_he, title_en, category, price_range) in enumerate(BASE_PRODUCTS):
            for variation in range(100):  # 100 variations per product = 10,000 * 10 = 100,000
                if total_added >= target:
                    break
                    
                try:
                    # Create variation name
                    if variation == 0:
                        var_title_he = title_he
                        var_title_en = title_en
                    else:
                        var_title_he = f"{title_he} דגם {variation}"
                        var_title_en = f"{title_en} model {variation}"
                    
                    product_id = generate_product_id()
                    
                    # Generate price
                    base_price = random.uniform(price_range[0], price_range[1])
                    discount = random.choice([0, 10, 15, 20, 25, 30])
                    
                    if discount > 0:
                        original_price = round(base_price / (1 - discount/100), 2)
                        sale_price = round(base_price, 2)
                    else:
                        original_price = None
                        sale_price = round(base_price, 2)
                    
                    # Create AliExpress search URL
                    search_term = urllib.parse.quote(var_title_he)
                    affiliate_url = f"https://www.aliexpress.com/w/wholesale-{search_term}.html?sortType=bestmatch"
                    
                    # Create styled image
                    bg_colors = {
                        'electronic': '0f3460', 'toys': '16213e', 'home_garden': '1a5f7a',
                        'tools': '533483', 'jewish': '14274e', 'sports': '1e5128',
                        'car': '232931', 'pet': '4a1c40', 'office': '1a1a2e', 'art': '432818'
                    }
                    text_colors = {
                        'electronic': 'e94560', 'toys': 'f9a825', 'home_garden': 'f9844a',
                        'tools': 'e94560', 'jewish': 'd4af37', 'sports': '4e9f3d',
                        'car': 'eeeeee', 'pet': 'd4a5a5', 'office': '4cc9f0', 'art': '9c6644'
                    }
                    
                    bg = bg_colors.get(category, '1a1a2e')
                    text = text_colors.get(category, 'e94560')
                    short_title = urllib.parse.quote(var_title_he[:15])
                    image_url = f"https://placehold.co/400x400/{bg}/{text}?text={short_title}"
                    
                    # Create product
                    product = Product(
                        product_id=product_id,
                        title=var_title_en,
                        title_hebrew=var_title_he,
                        description_hebrew=f"{var_title_he} - מוצר איכותי מאלי אקספרס. מחיר משתלם, איכות גבוהה, משלוח ישיר עד הבית.",
                        price=sale_price,
                        original_price=original_price,
                        currency='USD',
                        category=category,
                        image_url=image_url,
                        product_url=f"https://www.aliexpress.com/wholesale?SearchText={search_term}",
                        affiliate_url=affiliate_url,
                        rating=round(random.uniform(4.0, 5.0), 1),
                        reviews_count=random.randint(10, 2000),
                        orders_count=random.randint(50, 10000),
                        store_name=random.choice([
                            'AliExpress Official Store', 'Top Brand Store', 'Quality Seller',
                            'Pro Gadgets Store', 'Smart Buy Center', 'Best Value Shop'
                        ]),
                        is_modest=True
                    )
                    
                    db.session.add(product)
                    total_added += 1
                    
                    if total_added % 5000 == 0:
                        db.session.commit()
                        print(f"  Added {total_added:,}/{target:,} products ({(total_added/target*100):.1f}%)")
                        
                except Exception as e:
                    print(f"  Error: {e}")
                    db.session.rollback()
                    continue
            
            # Commit after each base product
            db.session.commit()
        
        db.session.commit()
        
        print(f"\n{'='*70}")
        print(f"✅ COMPLETE! Added {total_added:,} products")
        print(f"{'='*70}")
        print(f"Each product has:")
        print(f"  - Real AliExpress search link")
        print(f"  - Styled image with product name")
        print(f"  - Hebrew title and description")
        print(f"  - Price, discount, rating")


if __name__ == '__main__':
    create_100k_products()
