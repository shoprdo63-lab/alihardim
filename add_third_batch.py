#!/usr/bin/env python
"""
Add third batch of products to reach 2000+ products.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
from app import create_app, db
from app.models.database import Product
from config import Config

# Third batch - more products per category
THIRD_BATCH = {
    'electronic': [
        ("אוזניות ספורט אלחוטיות עמידות בזיעה", "Wireless Sports Earbuds Sweatproof", (20, 90)),
        ("רמקול Bluetooth עם אורות LED", "Bluetooth Speaker with LED Lights", (25, 85)),
        ("מטען שמשי נייד 20000mAh", "Solar Power Bank 20000mAh", (25, 80)),
        ("מצלמת אבטחה 360 מעלות פנורמית", "360 Degree Panoramic Security Camera", (35, 150)),
        ("עכבר ארגונומי אנכי אלחוטי", "Ergonomic Vertical Wireless Mouse", (15, 60)),
        ("מקלדת זעירה Bluetooth", "Mini Bluetooth Keyboard", (12, 45)),
        ("מיקרופון שורטגאן למחשב", "Shotgun Microphone for PC", (30, 120)),
        ("כרטיס קול USB חיצוני", "External USB Sound Card", (10, 40)),
        ("מתאם אודיו Bluetooth לטלוויזיה", "Bluetooth Audio Adapter for TV", (15, 55)),
        ("מצלמה נסתרת במטען", "Hidden Camera in Charger", (25, 100)),
        ("מצלמת גוף לשוטרים אבטחה", "Body Camera for Security", (40, 180)),
        ("מערכת אינטרקום אלחוטית", "Wireless Intercom System", (35, 140)),
        ("מנעול חכם לדלת עם טביעת אצבע", "Smart Door Lock Fingerprint", (80, 300)),
        ("פעמון דלת חכם עם מצלמה", "Smart Doorbell with Camera", (40, 180)),
        ("בקר IR חכם לכל המזגנים", "Universal Smart IR AC Controller", (15, 60)),
        ("שקע חכם WiFi עם מדידת צריכה", "Smart WiFi Plug with Energy Monitor", (12, 50)),
        ("מערכת גילוי עשן חכמה", "Smart Smoke Detection System", (25, 100)),
        ("מצלמת תינוק עם מוניטור", "Baby Monitor Camera with Screen", (45, 200)),
    ],
    'toys': [
        ("רובוט הרכבה לגו Mindstorms", "Lego Mindstorms Robot Kit", (200, 500)),
        ("מטוס RC מוכן לטיסה RTF", "RC Plane Ready To Fly", (60, 250)),
        ("סט חצים וקשת לילדים", "Kids Bow and Arrow Set", (15, 55)),
        ("ערכת כימיה לבית הספר", "School Chemistry Kit", (25, 90)),
        ("מיני זרוע רובוטית ללימוד", "Mini Robotic Arm for Learning", (30, 120)),
        ("סט בנייה ארכיטקטורה מודרנית", "Modern Architecture Building Set", (40, 180)),
        ("דינוזאור טרקס על שלט רחוק", "Remote Control T-Rex Dinosaur", (25, 100)),
        ("ערכת חקירה ביולוגית לילדים", "Kids Biology Exploration Kit", (20, 80)),
        ("משחק חשיבה חשמלי", "Electronic Brain Game", (20, 75)),
        ("בלדרים לטיפוס על קיר", "Wall Climbing Climbing Holds", (40, 180)),
        ("קורקינט תלת-אופן לילדים", "Kids Three Wheel Scooter", (25, 100)),
        ("סט משחקי חשיבה קלאסיים", "Classic Brain Games Set", (18, 70)),
        ("מיני בריכת שכשוך לפעוטות", "Toddler Splash Mini Pool", (20, 80)),
        ("צעצועי מים לקיץ סט 10", "Summer Water Toys Set 10", (15, 60)),
        ("מזרקת בועות ענקית", "Giant Bubble Fountain", (20, 80)),
    ],
    'home_garden': [
        ("מערכת גינון הידרופונית ביתית", "Home Hydroponic Garden System", (40, 180)),
        ("מנורת לילה הקרינה UV להדברה", "UV Night Light Pest Control", (15, 60)),
        ("מערכת השקיה טיפטוף אוטומטית", "Automatic Drip Irrigation System", (20, 90)),
        ("כיסא נדנדה לגינה מתקפל", "Folding Garden Rocking Chair", (60, 250)),
        ("מטבח חוץ נייד למחנאות", "Portable Outdoor Kitchen Camping", (80, 350)),
        ("מקרר נייד לרכב 12V/24V", "Portable Car Fridge 12V/24V", (100, 450)),
        ("מערכת פילטר מים לבית", "Whole House Water Filter System", (60, 300)),
        ("מכונת קפה אוטומטית", "Automatic Coffee Machine", (100, 500)),
        ("טוסטר אובן אינפרא אדום", "Infrared Toaster Oven", (40, 200)),
        ("מעבד מזון מקצועי 1000W", "Professional Food Processor 1000W", (50, 250)),
        ("מסחטת מיצים איטית", "Slow Juicer Machine", (60, 280)),
        ("מכונת לחם אוטומטית לבית", "Automatic Home Bread Maker", (70, 320)),
        ("מטחנת בשר חשמלית", "Electric Meat Grinder", (50, 220)),
        ("מערכת חימום מים שמשית", "Solar Water Heating System", (150, 600)),
        ("תריסים חשמליים חכמים", "Smart Electric Blinds", (80, 400)),
    ],
    'tools': [
        ("מקדחת עמוד שולחנית", "Bench Drill Press", (120, 500)),
        ("מסור שולחני חשמלי", "Table Saw Electric", (150, 700)),
        ("מכונת חיתוך פלזמה CNC", "CNC Plasma Cutting Machine", (300, 1500)),
        ("מלחם תעשייתי לעבודה כבדה", "Industrial Soldering Station", (40, 180)),
        ("מכשיר בדיקת מתכות", "Metal Detector Device", (30, 150)),
        ("מד לחץ שמן הידראולי", "Hydraulic Oil Pressure Gauge", (25, 100)),
        ("מערכת שאיבת אבק תעשייתית", "Industrial Dust Extraction System", (80, 400)),
        ("מכונת חיתוך גיליונות מתכת", "Sheet Metal Cutting Machine", (200, 900)),
        ("מסור סרט נייד לעץ ומתכת", "Portable Band Saw Wood Metal", (100, 500)),
        ("מד טמפרטורה לייזר אינפרא", "Infrared Laser Thermometer", (20, 100)),
        ("מכונת חריטה CNC שולחנית", "Desktop CNC Engraving Machine", (250, 1200)),
        ("מד עובי ציפוי צבע", "Paint Coating Thickness Meter", (40, 200)),
        ("מערכת ריתוך אינוורטר", "Inverter Welding System", (80, 400)),
        ("מכשיר בדיקת איכות אוויר", "Air Quality Testing Device", (50, 250)),
        ("מצלמה תרמית לבנייה", "Construction Thermal Camera", (150, 700)),
    ],
    'jewish': [
        ("סט תפילין מהודרות גסות", "Mehudar Tefillin Gasot Set", (200, 800)),
        ("סט תפילין מהודרות זעירות", "Mehudar Tefillin Zekinim Set", (180, 700)),
        ("ספר תורה בינוני כתב ספרדי", "Medium Sefer Torah Sefardi", (5000, 20000)),
        ("ספר תורה גדול מהודר", "Large Mehudar Sefer Torah", (8000, 35000)),
        ("מגילת אסתר כתב עתיק", "Ancient Megillat Esther Scroll", (300, 1500)),
        ("ספר זוהר מלא 23 כרכים", "Full Zohar 23 Volumes", (200, 800)),
        ("סט משניות מבוארות 12 כרכים", "Mishnah Berurah Set 12 Vol", (150, 600)),
        ("שולחן ערוך המבואר 28 כרכים", "Shulchan Aruch HaMevuar 28", (400, 1800)),
        ("תלמוד בבלי מבואר 20 כרכים", "Talmud Bavli Mevuar 20", (350, 1500)),
        ("סט חומש מבואר עם רשי", "Chumash with Rashi Set", (80, 350)),
        ("תיק טלית מרופד דמוי עור", "Padded Faux Leather Tallit Bag", (25, 100)),
        ("תיק תפילין מרופד מהודר", "Padded Mehudar Tefillin Bag", (30, 120)),
        ("מעמד לספרים נייד", "Portable Book Stand", (15, 60)),
        ("שעון שבת חשמלי דיגיטלי", "Digital Shabbat Clock", (20, 80)),
        ("מחשבון כשר לשבת", "Shabbat Kosher Calculator", (15, 60)),
    ],
    'sports': [
        ("גלשן גלים מתחילים מוקצף", "Beginner Foam Surfboard", (80, 350)),
        ("חליפת צלילה יבשה מקצועית", "Professional Dry Diving Suit", (200, 800)),
        ("מצנח צניחה ספורטיבית", "Sport Skydiving Parachute", (800, 3500)),
        ("חגורת משקולות לטבילה", "Weight Belt for Diving", (20, 80)),
        ("מערכת שנירקול ניידת", "Portable Snorkeling System", (40, 180)),
        ("מגני שיניים מקצועיים", "Professional Mouth Guards", (10, 50)),
        ("מערכת אימון TRX לבית", "Home TRX Training System", (30, 150)),
        ("מכשיר אימון חשמלי EMS", "EMS Electric Muscle Stimulator", (40, 200)),
        ("סט משקולות אולימפיות", "Olympic Weight Set", (150, 700)),
        ("ספת כושר מתכווננת לבית", "Adjustable Home Workout Bench", (80, 400)),
        ("מכשיר חתירה ביתי מתקפל", "Foldable Home Rowing Machine", (150, 700)),
        ("אופני כושר ספינינג ביתיים", "Home Spin Exercise Bike", (120, 600)),
        ("מסלול ריצה ביתי מתקפל", "Foldable Home Treadmill", (200, 1000)),
        ("מערכת סטרים טריינינג לטלוויזיה", "TV Streaming Workout System", (100, 500)),
        ("סקייטבורד חשמלי עם שלט", "Electric Skateboard with Remote", (150, 700)),
    ],
    'car': [
        ("מערכת אנדרואיד לרכב 10 אינץ", "10 inch Android Car System", (100, 500)),
        ("מצלמת 360 מעלות לרכב", "360 Degree Car Camera System", (80, 400)),
        ("רדאר גילוי מכוניות בסימון", "Blind Spot Car Detection Radar", (40, 200)),
        ("מערכת התנעה מרחוק לרכב", "Remote Car Start System", (50, 250)),
        ("מערכת בקרת שיוט אדפטיבית", "Adaptive Cruise Control System", (100, 600)),
        ("מערכת ניטור לחץ צמיגים", "Tire Pressure Monitoring System", (30, 150)),
        ("מערכת אזעקה לרכב חכמה", "Smart Car Alarm System", (40, 200)),
        ("מערכת שמע לרכב היי-פי", "Hi-Fi Car Audio System", (150, 800)),
        ("מערכת חיישני חנייה אחורית", "Rear Parking Sensor System", (20, 100)),
        ("רכיב רכב אנדרואיד CarPlay", "Android CarPlay Car Module", (60, 350)),
        ("מערכת ניווט GPS לקטנוע", "GPS Navigation for Scooter", (40, 200)),
        ("מעמד אופניים לגג הרכב", "Car Roof Bike Rack", (40, 200)),
        ("נגרר קטנוע לרכב", "Car Scooter Trailer", (150, 700)),
        ("מערכת חימום מושבים לרכב", "Car Seat Heating System", (30, 150)),
        ("מערכת טיהור אוויר אוטומטית", "Automatic Air Purifier System", (40, 250)),
    ],
    'pet': [
        ("בית חכם לחתול עם ציפוי חום", "Smart Heated Cat House", (50, 250)),
        ("מערכת מזון אוטומטית לחתולים", "Automatic Cat Feeding System", (60, 300)),
        ("מערכת שירותים אוטומטית לחתולים", "Automatic Cat Toilet System", (150, 800)),
        ("מזרקת מים חכמה לחיות מחמד", "Smart Pet Water Fountain", (25, 120)),
        ("ציוד אילוף אלקטרוני מתקדם", "Advanced Electronic Training Kit", (40, 200)),
        ("GPS מדויק לכלבים עם היסטוריה", "Precision Dog GPS with History", (60, 350)),
        ("ציוד טיפוח מקצועי לכלבים", "Professional Dog Grooming Set", (40, 220)),
        ("מיטה אורטופדית לכלבים ענקית", "Giant Orthopedic Dog Bed", (60, 350)),
        ("מזון יבש פרימיום לכלבים 20 קג", "Premium Dry Dog Food 20kg", (40, 200)),
        ("מזון יבש פרימיום לחתולים 10 קג", "Premium Dry Cat Food 10kg", (30, 180)),
        ("חטיפים טבעיים לכלבים 5 קג", "Natural Dog Treats 5kg", (25, 120)),
        ("צעצועים לעיסה לכלבים חזקים", "Heavy Duty Dog Chew Toys", (15, 80)),
        ("מערכת משחק אינטראקטיבית לחתולים", "Interactive Cat Play System", (30, 180)),
        ("בגדים לכלבים לחורף סט 3", "Winter Dog Clothes Set 3", (20, 100)),
        ("נעלי כלבים לטיולים סט 4", "Dog Walking Shoes Set 4", (15, 80)),
    ],
    'office': [
        ("מדפסת לייזר צבעונית WiFi", "WiFi Color Laser Printer", (150, 700)),
        ("סורק מסמכים אוטומטי ADF", "ADF Automatic Document Scanner", (100, 500)),
        ("מכונת צילום מסמכים ניידת", "Portable Document Camera", (60, 350)),
        ("לוח מחיק חכם 75 אינץ", "Smart 75 inch Whiteboard", (300, 1500)),
        ("מערכת ועידת וידאו מלאה", "Full Video Conference System", (200, 1000)),
        ("מצלמת רשת 4K למשרד", "4K Webcam for Office", (50, 300)),
        ("מיקרופון לועדות אלחוטי", "Wireless Conference Microphone", (60, 350)),
        ("סט רמקולים למשרד Bluetooth", "Office Bluetooth Speaker Set", (40, 250)),
        ("מעמד מסך מתכוונן ארגונומי", "Ergonomic Adjustable Monitor Arm", (40, 220)),
        ("שולחן עבודה מתכוונן חשמלי", "Electric Adjustable Desk", (200, 1000)),
        ("כיסא ארגונומי למשרד", "Ergonomic Office Chair", (150, 800)),
        ("מגן מסך פרטיות למחשב", "Computer Privacy Screen Protector", (20, 120)),
        ("מערכת גיבוי נתונים NAS", "Network NAS Backup System", (150, 800)),
        ("סט ציוד משרדי חברה", "Company Office Supplies Set", (100, 600)),
        ("מערכת אבטחת מידע למשרד", "Office Data Security System", (80, 500)),
    ],
    'art': [
        ("מכונת חריטת לייזר שולחנית", "Desktop Laser Engraver", (200, 1200)),
        ("מדפסת תלת מימד לבית", "Home 3D Printer", (150, 800)),
        ("סט ציור שמן מקצועי 72 צבעים", "Professional Oil Paint 72 Colors", (40, 250)),
        ("מכונת כתיבה וינטג' פעילה", "Working Vintage Typewriter", (100, 600)),
        ("ציוד צילום תאורה מקצועית", "Professional Photography Lighting", (80, 500)),
        ("מסך ציור גרפי 22 אינץ", "22 inch Graphic Drawing Tablet", (150, 800)),
        ("עט דיגיטלי למעצבים Wacom", "Wacom Digital Design Pen", (60, 400)),
        ("מכונת רקמה ממוחשבת ביתית", "Home Computerized Embroidery", (200, 1200)),
        ("סט פיסול חימר מקצועי מלא", "Complete Professional Clay Kit", (50, 350)),
        ("ציוד יצירת תכשיטים מתקדם", "Advanced Jewelry Making Kit", (40, 300)),
        ("מכונת חיתוך ויניל Cricut", "Cricut Vinyl Cutting Machine", (150, 700)),
        ("סט ציור פנים מקצועי", "Professional Portrait Painting Set", (30, 250)),
        ("ציוד ציור קעקועים למתחילים", "Beginner Tattoo Art Kit", (60, 450)),
        ("מערכת הדפסה על מוצרים", "Product Printing System", (100, 700)),
        ("ציוד סטודיו צילום נייד", "Portable Photography Studio Kit", (50, 400)),
    ],
}


def generate_product_id():
    return f"100500{random.randint(100000000, 999999999)}"


def add_third_batch():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Adding Third Batch - Target: 2000+ products")
        print("=" * 60)
        
        existing_count = Product.query.count()
        print(f"Current products: {existing_count}")
        
        total_added = 0
        
        for category_key, products in THIRD_BATCH.items():
            print(f"\n{'='*60}")
            print(f"Category: {Config.SAFE_CATEGORIES.get(category_key, category_key)}")
            print(f"{'='*60}")
            
            category_added = 0
            
            for title_hebrew, title_en, price_range in products:
                # Create 4 variations of each product
                for _ in range(4):
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
                        
                    except Exception as e:
                        db.session.rollback()
                        continue
            
            db.session.commit()
            print(f"  Added {category_added} products")
        
        print(f"\n{'='*60}")
        print("THIRD BATCH COMPLETE!")
        print(f"{'='*60}")
        print(f"New products added: {total_added}")
        print(f"Total products in database: {Product.query.count()}")


if __name__ == '__main__':
    add_third_batch()
