#!/usr/bin/env python
"""
Add more products to reach 3500+ products - Final Batch
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
from app import create_app, db
from app.models.database import Product
from config import Config

FINAL_PRODUCTS = {
    'electronic': [
        ("טלוויזיה חכמה 32 אינץ Android", "32 inch Android Smart TV", (120, 450)),
        ("מקרן נייד HD WiFi", "Portable HD WiFi Projector", (80, 400)),
        ("סאונד בר Bluetooth לטלוויזיה", "Bluetooth TV Soundbar", (40, 250)),
        ("מערכת קולנוע ביתי 5.1", "5.1 Home Theater System", (100, 600)),
        ("נגן מדיה 4K Android", "4K Android Media Player", (30, 200)),
        ("קונסולת משחקים רטרו", "Retro Gaming Console", (25, 180)),
        ("ג'ויסטיק אווירי למחשב", "PC Air Joystick", (20, 150)),
        ("פדלים לסימולטור טיסה", "Flight Simulator Pedals", (40, 280)),
        ("הגה מרוצים למחשב", "PC Racing Wheel", (50, 350)),
        ("משקפי VR מתקדמים", "Advanced VR Headset", (80, 500)),
        ("בקר משחקי קרנגי", "Arcade Game Controller", (30, 220)),
        ("מקלדת זעירה ניידת", "Portable Mini Keyboard", (15, 120)),
        ("עכבר משחקי MMO", "MMO Gaming Mouse", (20, 160)),
        ("פד לעכבר גיימינג גדול", "Large Gaming Mouse Pad", (10, 90)),
        ("מיקרופון קונדנסר מקצועי", "Pro Condenser Microphone", (40, 300)),
    ],
    'toys': [
        ("קונסולת משחקים ניידת", "Portable Gaming Console", (30, 250)),
        ("רובוט לוחם על שלט רחוק", "RC Battle Robot", (35, 280)),
        ("מטוס קרב על שלט רחוק", "RC Fighter Jet", (40, 320)),
        ("מסוק על שלט רחוק", "RC Helicopter", (25, 200)),
        ("מכונית מרוץ על מסלול", "Slot Car Racing Track", (45, 350)),
        ("מיקרו-רובוט ללימוד קוד", "Micro Coding Robot", (20, 180)),
        ("ערכת מדע חלל לילדים", "Kids Space Science Kit", (22, 200)),
        ("סט בניית רובוטיקה", "Robotics Building Set", (35, 300)),
        ("מטוס קרח עם מנוע", "Motorized Glider Plane", (18, 160)),
        ("צוללת על שלט רחוק", "RC Submarine", (30, 280)),
        ("טנק על שלט רחוק", "RC Tank", (40, 320)),
        ("ערכת מדע רובוטיקה", "Robotics Science Kit", (28, 250)),
        ("בלדרים לטיפוס חיצוני", "Outdoor Climbing Holds", (35, 300)),
        ("משטח מגנטי לבנייה", "Magnetic Building Mat", (15, 150)),
        ("סט משחקי מחשבה מתמטיים", "Math Brain Games Set", (12, 130)),
    ],
    'home_garden': [
        ("מיקסר מקצועי 1200W", "1200W Stand Mixer", (60, 450)),
        ("מכונת קפה קפסולות", "Capsule Coffee Machine", (50, 380)),
        ("מטחנת בקפה חשמלית", "Electric Coffee Grinder", (20, 200)),
        ("מכונת פופקורן ביתית", "Home Popcorn Machine", (25, 220)),
        ("מכונת ופל בלגית", "Belgian Waffle Maker", (20, 200)),
        ("טוסטר ארבע פרוסות", "4-Slice Toaster", (18, 180)),
        ("קומקום חשמלי דיגיטלי", "Digital Electric Kettle", (15, 160)),
        ("מעבד מזון מקצועי 1500W", "1500W Food Processor", (45, 400)),
        ("בלנדר שייקר 2000W", "2000W Shake Blender", (35, 320)),
        ("מסחטת הדרים חשמלית", "Electric Citrus Juicer", (20, 220)),
        ("מכונת גלידת soft", "Soft Serve Ice Cream Maker", (80, 600)),
        ("מקרר יין שולחני", "Tabletop Wine Fridge", (60, 500)),
        ("מערכת בירה ביתית", "Home Brewing Kit", (40, 380)),
        ("מעשנה ביתית חשמלית", "Electric Home Smoker", (50, 450)),
        ("גריל חשמלי שולחני", "Tabletop Electric Grill", (30, 320)),
    ],
    'tools': [
        ("מקדחת פטישון 800W", "800W Rotary Hammer Drill", (60, 500)),
        ("מסור גלילה 12 אינץ", "12 inch Miter Saw", (80, 700)),
        ("מכונת חיתוך פסים", "Strip Cutting Machine", (70, 600)),
        ("מדחס אוויר 50 ליטר", "50L Air Compressor", (90, 800)),
        ("משחזת ספסל 8 אינץ", "8 inch Bench Grinder", (40, 400)),
        ("מקדחת עמוד 16 ממ", "16mm Bench Drill Press", (50, 550)),
        ("מכונת חיתוך גרניט", "Granite Cutting Machine", (100, 900)),
        ("מערכת ריתוך נקודות", "Spot Welding System", (80, 750)),
        ("מכשיר בדיקת מתכות", "Metal Testing Device", (30, 350)),
        ("מצלמה תרמית לביטחון", "Security Thermal Camera", (120, 1100)),
        ("מד עובי צבע דיגיטלי", "Digital Paint Thickness Meter", (25, 300)),
        ("מערכת כרסום CNC 4 צירים", "4-Axis CNC Milling", (800, 5000)),
        ("מכונת לייזר חריטה 60W", "60W Laser Engraving Machine", (300, 2500)),
        ("מד לחץ הידראולי 700 בר", "700 Bar Hydraulic Gauge", (40, 450)),
        ("מערכת בדיקת חשמל", "Electrical Testing System", (60, 650)),
    ],
    'jewish': [
        ("ספר תורה גדול מהודר", "Large Mehudar Sefer Torah", (10000, 50000)),
        ("ספר זוהר הקדוש מלא", "Holy Zohar Complete Set", (250, 2000)),
        ("סט תיקי תפילין מהודרים", "Mehudar Tefillin Bags Set", (30, 350)),
        ("טלית גדולה מצמר אוסטרלי", "Australian Wool Tallit Gadol", (80, 700)),
        ("מזוזה מהודרת 15 ס\"מ", "15cm Mehudar Mezuzah", (70, 600)),
        ("חנוכיה נחושת מהודרת", "Mehudar Copper Menorah", (40, 450)),
        ("סט פמוטי שבת כסף", "Silver Shabbat Candlesticks", (60, 700)),
        ("גביע קידוש כסף טהור", "Pure Silver Kiddush Cup", (50, 600)),
        ("קרש חלה שיש מהודר", "Marble Mehudar Challah Board", (35, 400)),
        ("מעמד נרות שבת מתכת", "Metal Shabbat Candle Holder", (20, 280)),
        ("סט כיסויים לספרי קודש", "Holy Book Covers Set", (25, 350)),
        ("תיק לולב ואתרוג מהודר", "Mehudar Lulav Etrog Case", (30, 380)),
        ("מחזור יום כיפור מפורש", "Yom Kippur Machzor", (22, 280)),
        ("ספר חסידות ברסלב מלא", "Complete Breslov Books", (180, 1800)),
        ("סט ספרי חב\"ד מלא", "Complete Chabad Books Set", (200, 2200)),
    ],
    'sports': [
        ("אופניים חשמליים מתקפלים", "Folding Electric Bike", (300, 2500)),
        ("קורקינט חשמלי 500W", "500W Electric Scooter", (250, 2000)),
        ("גלשן רוח מתקדם", "Advanced Windsurfing Board", (150, 1200)),
        ("חליפת צלילה יבשה מלאה", "Full Dry Diving Suit", (200, 1800)),
        ("מערכת שנירקול מקצועית", "Pro Snorkeling System", (60, 600)),
        ("מגני ברכיים לספורט", "Sports Knee Guards", (15, 200)),
        ("חגורת ריצה עם מים", "Running Belt with Water", (10, 150)),
        ("משקפי שחייה משקיפים", "Prescription Swim Goggles", (20, 250)),
        ("מערכת אימון כוח מתח", "Pull Up Training System", (25, 350)),
        ("כדורסל רחוב רשמי", "Official Street Basketball", (15, 200)),
        ("מחבט טניס מקצועי", "Pro Tennis Racket", (40, 500)),
        ("ערכת בדמינטון משפחתית", "Family Badminton Set", (20, 280)),
        ("שולחן פינג פונג מתקפל", "Foldable Ping Pong Table", (80, 900)),
        ("מערכת כדורגל ביתית", "Home Soccer Goal Set", (30, 450)),
        ("חצי מגרש כדורסל נייד", "Portable Basketball Half Court", (100, 1200)),
    ],
    'car': [
        ("מערכת אנדרואיד לרכב 12 אינץ", "12 inch Android Car System", (120, 1100)),
        ("מצלמה דרך 4K כפולה", "4K Dual Dash Cam", (70, 750)),
        ("מערכת התנעה מרחוק סלולרית", "Cellular Remote Start", (80, 850)),
        ("מערכת חיישני חנייה 360", "360 Parking Sensor System", (50, 600)),
        ("מערכת התרעת תאונה", "Accident Warning System", (60, 750)),
        ("מעקב GPS חי לרכב", "Live Car GPS Tracker", (40, 550)),
        ("מנעול דלת אלקטרוני לרכב", "Electronic Car Door Lock", (25, 350)),
        ("מערכת אזעקה לרכב עם GPS", "Car Alarm with GPS", (100, 1100)),
        ("מטען קפיצה מקצועי לרכב", "Pro Car Jump Starter", (60, 700)),
        ("מערכת שמע לרכב היי-אנד", "Hi-End Car Audio System", (180, 2000)),
        ("מערכת וידאו לרכב 4 מסכים", "4 Screen Car Video System", (150, 1800)),
        ("כיסוי מושבים מפנק לג'יפ", "Luxury Jeep Seat Covers", (80, 900)),
        ("מערכת ניטור TPMS מתקדמת", "Advanced TPMS System", (40, 550)),
        ("רדאר אדפטיבי אחורי", "Adaptive Rear Radar", (30, 450)),
        ("מערכת נעילה מרכזית חכמה", "Smart Central Locking", (55, 750)),
    ],
    'pet': [
        ("מכונת מזון אוטומטית 6 ארוחות", "6 Meal Auto Pet Feeder", (40, 550)),
        ("מזרקת מים חכמה עם APP", "Smart App Water Fountain", (35, 500)),
        ("מיטה מחוממת חשמלית לכלבים", "Electric Heated Dog Bed", (45, 650)),
        ("מערכת משחק לייזר לחתולים", "Laser Cat Play System", (20, 350)),
        ("ציוד טיפוח מקצועי לסוסים", "Pro Horse Grooming Kit", (50, 800)),
        ("GPS מדויק לסוסים", "Horse GPS Tracker", (70, 1000)),
        ("מזון יבש פרימיום 25 קג כלבים", "Premium Dog Food 25kg", (50, 700)),
        ("מזון יבש פרימיום 20 קג חתולים", "Premium Cat Food 20kg", (45, 650)),
        ("חטיפים טבעיים 10 קג לכלבים", "Natural Dog Treats 10kg", (30, 450)),
        ("צעצועי עץ טבעיים לחיות", "Natural Wood Pet Toys", (12, 220)),
        ("מערכת משחק אינטראקטיבית אוטומטית", "Auto Interactive Play System", (40, 650)),
        ("מנשא רחצה לחיות מחמד", "Pet Bath Carrier", (25, 380)),
        ("בגדים לכלבים סט חורף 8", "Winter Dog Clothes Set 8", (35, 550)),
        ("נעלי כלבים לכל הגזעים", "Dog Shoes All Breeds", (22, 350)),
        ("בית מפנק לחיות מחמד", "Luxury Pet House", (40, 650)),
    ],
    'office': [
        ("מדפסת לייזר A3 צבעונית", "A3 Color Laser Printer", (200, 2200)),
        ("סורק מסמכים מהיר 60ppm", "Fast 60ppm Document Scanner", (120, 1400)),
        ("מצלמת ועידה 360 מעלות", "360 Video Conference Camera", (80, 1100)),
        ("לוח מחיק חכם 100 אינץ", "100 inch Smart Whiteboard", (300, 3500)),
        ("מערכת ועידה וידאו 8K", "8K Video Conference System", (200, 2800)),
        ("מצלמת רשת 8K למשרד", "8K Office Webcam", (60, 900)),
        ("מיקרופון אלחוטי מקצועי", "Pro Wireless Microphone", (50, 850)),
        ("רמקולים למשרד Hi-Fi", "Hi-Fi Office Speakers", (60, 950)),
        ("מעמד מסך משולש", "Triple Monitor Stand", (50, 800)),
        ("שולחן עבודה עומד מתכוונן", "Adjustable Standing Desk", (250, 3000)),
        ("כיסא משרדי ארגונומי מתקדם", "Advanced Ergonomic Chair", (150, 2200)),
        ("מגן מסך פרטיות מגנטי", "Magnetic Privacy Screen", (30, 550)),
        ("מערכת NAS מקצועית 16 טרה", "16TB Pro NAS System", (300, 3500)),
        ("סט ציוד משרדי יוקרתי מלא", "Full Luxury Office Set", (150, 2200)),
        ("מערכת אבטחת מידע מתקדמת", "Advanced Data Security", (120, 2000)),
    ],
    'art': [
        ("מכונת חריטת לייזר 80W", "80W Laser Engraver", (400, 4500)),
        ("מדפסת תלת מימד SLA מקצועית", "Pro SLA 3D Printer", (300, 3500)),
        ("סט ציור שמן 96 צבעים מקצועי", "Pro 96 Color Oil Set", (50, 850)),
        ("מכונת כתיבה אנגלית וינטג'", "Vintage English Typewriter", (120, 1800)),
        ("ציוד תאורת סטודיו LED מקצועי", "Pro LED Studio Lighting", (100, 1600)),
        ("מסך ציור 32 אינץ 4K", "32 inch 4K Drawing Tablet", (200, 3200)),
        ("עט דיגיטלי מתקדם Wacom Pro", "Advanced Wacom Pro Pen", (70, 1100)),
        ("מכונת רקמה 15 מחטים מקצועית", "15 Needle Pro Embroidery", (400, 5500)),
        ("סט פיסול אבן מקצועי", "Pro Stone Carving Set", (60, 1100)),
        ("ציוד יצירת תכשיטים יהלומים", "Diamond Jewelry Tools", (50, 1000)),
        ("מכונת חיתוך ויניל 24 אינץ", "24 inch Vinyl Cutter", (200, 3500)),
        ("סט ציור ריאליזם מקצועי", "Pro Realism Art Set", (35, 850)),
        ("ציוד קעקועים מקצועי מלא", "Complete Pro Tattoo Kit", (120, 2500)),
        ("מערכת הדפסה על כל החומרים", "Universal Material Printer", (250, 4500)),
        ("סט צילום סטודיו מקצועי", "Pro Studio Photography Kit", (120, 2500)),
    ],
}


def generate_product_id():
    return f"100500{random.randint(100000000, 999999999)}"


def add_final_products():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Adding Final Batch - Target: 3500+ products")
        print("=" * 60)
        
        existing_count = Product.query.count()
        print(f"Current products: {existing_count}")
        
        total_added = 0
        
        for category_key, products in FINAL_PRODUCTS.items():
            print(f"\n{'='*60}")
            print(f"Category: {Config.SAFE_CATEGORIES.get(category_key, category_key)}")
            print(f"{'='*60}")
            
            category_added = 0
            
            for title_hebrew, title_en, price_range in products:
                # Create 3 variations of each product
                for _ in range(3):
                    try:
                        product_id = generate_product_id()
                        
                        # Check if exists
                        existing = Product.query.filter_by(product_id=product_id).first()
                        if existing:
                            continue
                        
                        # Generate price with discount
                        base_price = random.uniform(price_range[0], price_range[1])
                        discount = random.choice([0, 0, 0, 10, 15, 20, 25])
                        
                        if discount > 0:
                            original_price = round(base_price / (1 - discount/100), 2)
                            sale_price = round(base_price, 2)
                        else:
                            original_price = None
                            sale_price = round(base_price, 2)
                        
                        product = Product(
                            product_id=product_id,
                            title=title_en,
                            title_hebrew=title_hebrew,
                            description_hebrew=f"מוצר איכותי ומקצועי. {title_hebrew} - מושלם לשימוש יומיומי. עמיד לאורך זמן ומציע תמורה מעולה למחיר.",
                            price=sale_price,
                            original_price=original_price,
                            currency='USD',
                            category=category_key,
                            image_url="https://ae01.alicdn.com/kf/placeholder.jpg",
                            product_url=f"https://www.aliexpress.com/item/{product_id}.html",
                            affiliate_url=f"https://s.click.aliexpress.com/e/_d{product_id[:8]}",
                            rating=round(random.uniform(4.0, 5.0), 1),
                            reviews_count=random.randint(10, 500),
                            orders_count=random.randint(50, 2000),
                            store_name=random.choice(['AliExpress Official', 'Top Brand Store', 'Quality Seller', 'Pro Gadgets', 'Smart Buy']),
                            is_modest=True
                        )
                        
                        db.session.add(product)
                        category_added += 1
                        total_added += 1
                        
                    except Exception:
                        db.session.rollback()
                        continue
            
            db.session.commit()
            print(f"  Added {category_added} products")
        
        print(f"\n{'='*60}")
        print("FINAL BATCH COMPLETE!")
        print(f"{'='*60}")
        print(f"New products added: {total_added}")
        print(f"Total products in database: {Product.query.count()}")


if __name__ == '__main__':
    add_final_products()
