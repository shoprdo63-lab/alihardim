#!/usr/bin/env python
"""
Seed products into database - for Vercel deployment
"""
import random
import urllib.parse
from app import db
from app.models.database import Product
from config import Config

# Base product templates - will generate 1000 products
BASE_PRODUCTS = [
    # Electronics (100 products x 10 variations = 1000)
    ("אוזניות Bluetooth", "bluetooth earbuds", "electronic", (15, 80)),
    ("מטען נייד", "power bank", "electronic", (20, 90)),
    ("רמקול Bluetooth", "bluetooth speaker", "electronic", (25, 120)),
    ("מצלמת אבטחה WiFi", "wifi security camera", "electronic", (30, 150)),
    ("שעון חכם", "smart watch", "electronic", (35, 180)),
    ("מטען רכב USB", "car usb charger", "electronic", (8, 35)),
    ("כבל USB-C", "usb c cable", "electronic", (6, 25)),
    ("מיקרופון USB", "usb microphone", "electronic", (20, 80)),
    ("עכבר אלחוטי", "wireless mouse", "electronic", (15, 60)),
    ("מקלדת Bluetooth", "bluetooth keyboard", "electronic", (25, 100)),
    
    # Toys
    ("לגו קלאסי", "classic lego", "toys", (30, 150)),
    ("מכונית על שלט", "rc car", "toys", (35, 180)),
    ("רובוט לילדים", "kids robot", "toys", (25, 120)),
    ("בובת פרווה", "plush doll", "toys", (15, 100)),
    ("ערכת יצירה", "craft kit", "toys", (10, 80)),
    ("פאזל 1000 חלקים", "1000 piece puzzle", "toys", (12, 60)),
    ("דינוזאור צעצוע", "toy dinosaur", "toys", (20, 120)),
    ("צעצוע חינוכי", "educational toy", "toys", (15, 100)),
    ("קוביות מגנטיות", "magnetic blocks", "toys", (25, 150)),
    ("נשק מים", "water gun", "toys", (10, 50)),
    
    # Home & Garden
    ("מכונת קפה", "coffee machine", "home_garden", (60, 300)),
    ("מסחטת מיצים", "juicer", "home_garden", (50, 250)),
    ("מטחנת בשר", "meat grinder", "home_garden", (45, 220)),
    ("מכונת לחם", "bread maker", "home_garden", (70, 350)),
    ("מטהר אוויר", "air purifier", "home_garden", (80, 400)),
    ("שואב אבק רובוטי", "robot vacuum", "home_garden", (120, 600)),
    ("סיר לחץ חשמלי", "electric pressure cooker", "home_garden", (60, 320)),
    ("מיקסר מקצועי", "stand mixer", "home_garden", (80, 400)),
    ("מכונת גלידה", "ice cream maker", "home_garden", (40, 200)),
    ("מסנן מים", "water filter", "home_garden", (30, 150)),
    
    # Tools
    ("מקדחה חשמלית", "electric drill", "tools", (60, 300)),
    ("סט מברגים", "screwdriver set", "tools", (15, 100)),
    ("משחזת זווית", "angle grinder", "tools", (50, 250)),
    ("מד טווח לייזר", "laser measure", "tools", (25, 130)),
    ("מצלמה בורסקופית", "borescope camera", "tools", (30, 150)),
    ("מדחס אוויר", "air compressor", "tools", (80, 400)),
    ("מסור שולחני", "table saw", "tools", (100, 500)),
    ("מלחם חשמלי", "soldering iron", "tools", (20, 100)),
    ("סט כלי יד", "hand tool set", "tools", (30, 200)),
    ("משקל תליה דיגיטלי", "digital scale", "tools", (15, 80)),
    
    # Jewish
    ("תפילין מהודרות", "tefillin", "jewish", (200, 900)),
    ("טלית גדולה", "tallit", "jewish", (80, 400)),
    ("מזוזה", "mezuzah", "jewish", (30, 200)),
    ("חנוכיה", "menorah", "jewish", (40, 250)),
    ("סט פמוטים", "candlesticks", "jewish", (30, 180)),
    ("גביע קידוש", "kiddush cup", "jewish", (50, 250)),
    ("קרש חלה", "challah board", "jewish", (30, 150)),
    ("מחזור", "machzor", "jewish", (25, 120)),
    ("תיק תפילין", "tefillin bag", "jewish", (40, 180)),
    ("זוג פמוטים", "candlestick pair", "jewish", (35, 200)),
    
    # Sports
    ("אופניים חשמליים", "electric bike", "sports", (300, 1500)),
    ("קורקינט חשמלי", "electric scooter", "sports", (250, 1200)),
    ("גלשן גלים", "surfboard", "sports", (80, 400)),
    ("חליפת צלילה", "wetsuit", "sports", (40, 200)),
    ("מערכת שנירקול", "snorkeling set", "sports", (50, 250)),
    ("מקלות טיולים", "trekking poles", "sports", (25, 120)),
    ("תרמיל 65 ליטר", "backpack 65l", "sports", (45, 220)),
    ("אוהל משפחתי", "family tent", "sports", (100, 500)),
    ("מזרן שטח", "camping mattress", "sports", (40, 180)),
    ("פנס ראש", "headlamp", "sports", (15, 80)),
    
    # Car
    ("מצלמת דרך", "dash cam", "car", (60, 300)),
    ("מערכת התנעה", "remote starter", "car", (50, 250)),
    ("חיישני חנייה", "parking sensors", "car", (25, 120)),
    ("מעקב GPS", "gps tracker", "car", (40, 200)),
    ("מערכת שמע", "car audio", "car", (80, 400)),
    ("מטען קפיצה", "jump starter", "car", (50, 250)),
    ("כיסוי מושבים", "seat covers", "car", (40, 200)),
    ("מערכת TPMS", "tire pressure", "car", (35, 180)),
    ("מצלמת רוורס", "backup camera", "car", (20, 100)),
    ("מברשת ניקוי", "car brush", "car", (15, 70)),
    
    # Pet
    ("מיטה מחוממת", "heated pet bed", "pet", (30, 150)),
    ("מכונת מזון", "auto feeder", "pet", (40, 200)),
    ("מערכת מים", "water fountain", "pet", (25, 130)),
    ("בית חתולים", "cat tree", "pet", (35, 180)),
    ("ציוד טיפוח", "grooming kit", "pet", (30, 150)),
    ("קערת איטית", "slow bowl", "pet", (10, 50)),
    ("מיטה אורטופדית", "orthopedic bed", "pet", (40, 200)),
    ("צעצוע אינטראקטיבי", "interactive toy", "pet", (15, 80)),
    ("קולר GPS", "gps collar", "pet", (40, 200)),
    ("מזרקת מים", "water fountain", "pet", (30, 150)),
    
    # Office
    ("מדפסת תרמית", "thermal printer", "office", (50, 250)),
    ("לוח מחיק", "whiteboard", "office", (120, 600)),
    ("מצלמת וידאו", "webcam", "office", (60, 300)),
    ("מיקרופון", "microphone", "office", (25, 130)),
    ("סט משרדי", "office set", "office", (30, 150)),
    ("מעמד מסך", "monitor arm", "office", (40, 200)),
    ("שולחן מתכוונן", "standing desk", "office", (200, 1000)),
    ("כיסא משרדי", "office chair", "office", (120, 600)),
    ("מערכת NAS", "nas system", "office", (180, 900)),
    ("מקרן נייד", "projector", "office", (150, 750)),
    
    # Art
    ("מכונת לייזר", "laser engraver", "art", (250, 1200)),
    ("מדפסת תלת מימד", "3d printer", "art", (200, 1000)),
    ("סט ציור", "paint set", "art", (30, 150)),
    ("מסך ציור", "drawing tablet", "art", (120, 600)),
    ("עט דיגיטלי", "digital pen", "art", (50, 250)),
    ("מכונת רקמה", "embroidery machine", "art", (250, 1200)),
    ("סט פיסול", "sculpting set", "art", (40, 200)),
    ("ציוד תכשיטים", "jewelry kit", "art", (30, 150)),
    ("מכונת ויניל", "vinyl cutter", "art", (120, 600)),
    ("סט צילום", "photo kit", "art", (70, 350)),
]

# Colors per category
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


def generate_product_id():
    """Generate unique product ID"""
    return f"100500{random.randint(100000000, 999999999)}"


def seed_products():
    """Seed the database with REAL AliExpress products with REAL images."""
    from app.api.aliexpress import aliexpress_api
    
    print("🌱 Importing REAL AliExpress products with REAL images...")
    
    with current_app.app_context():
        # Import keywords that give good results
        keywords = ['smartphone', 'headphones', 'smart watch', 'laptop', 'tablet', 
                    'charger', 'case', 'cable', 'speaker', 'camera']
        
        added_count = Product.query.count()
        if added_count > 1000:
            print(f"✅ Already have {added_count:,} real products, skipping.")
            return 0
        
        print(f"Importing real products from AliExpress API...")
        
        for keyword in keywords[:5]:  # Get 5 categories to start
            try:
                print(f"\n🔍 Searching: {keyword}")
                
                result = aliexpress_api._make_request('GET', {
                    'method': 'aliexpress.affiliate.product.query',
                    'keywords': keyword,
                    'page_no': 1,
                    'page_size': 50,
                    'target_currency': 'USD',
                    'target_language': 'EN',
                    'tracking_id': aliexpress_api.tracking_id,
                    'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title',
                })
                
                if not result or 'resp_result' not in result:
                    continue
                
                data = result['resp_result'].get('result', {})
                products_data = data.get('products', {}).get('product', [])
                
                print(f"   Found {len(products_data)} products")
                
                for product in products_data:
                    pid = product.get('product_id', '')
                    
                    # Skip if exists
                    if Product.query.filter_by(product_id=pid).first():
                        continue
                    
                    # Parse price
                    price_str = product.get('target_sale_price', product.get('sale_price', '0'))
                    try:
                        price = float(str(price_str).replace('$', '').replace(',', ''))
                    except:
                        price = 0.0
                    
                    # Get REAL image URL
                    image_url = product.get('product_main_image', '')
                    
                    new_product = Product(
                        product_id=pid,
                        title=product.get('product_title', ''),
                        title_hebrew=product.get('product_title', ''),
                        description_hebrew='מוצר איכותי מאלי אקספרס. משלוח חינם.',
                        price=price,
                        original_price=price * 1.2 if price > 0 else 0,
                        currency='USD',
                        category='electronic',
                        image_url=image_url,  # REAL IMAGE!
                        product_url=product.get('product_detail_url', ''),
                        affiliate_url=product.get('product_detail_url', ''),
                        rating=float(str(product.get('evaluate_rate', '4.5')).split()[0]) if product.get('evaluate_rate') else 4.5,
                        reviews_count=0,
                        orders_count=0,
                        store_name=product.get('shop_title', 'AliExpress'),
                        is_modest=True
                    )
                    
                    db.session.add(new_product)
                    added_count += 1
                
                db.session.commit()
                print(f"   ✅ Added products (Total: {added_count})")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        print(f"\n🎉 Successfully imported {added_count} REAL products with REAL images!")
        return added_count


if __name__ == '__main__':
    seed_products()
