#!/usr/bin/env python
"""
Add more products to reach 5000+ products - Batch 1
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
from app import create_app, db
from app.models.database import Product
from config import Config

# More products for each category
MORE_PRODUCTS = {
    'electronic': [
        ("מסך מחשב 24 אינץ LED", "24 inch LED Computer Monitor", (80, 300)),
        ("מקלדת גיימינג מכנית RGB", "RGB Mechanical Gaming Keyboard", (40, 180)),
        ("עכבר אלחוטי ארגונומי", "Ergonomic Wireless Mouse", (15, 70)),
        ("רמקולים למחשב 2.1", "2.1 Computer Speakers", (25, 120)),
        ("מצלמת אבטחה PTZ חיצונית", "Outdoor PTZ Security Camera", (50, 250)),
        ("מערכת אינטרקום וידאו", "Video Intercom System", (60, 300)),
        ("מטען מהיר 100W USB-C", "100W USB-C Fast Charger", (20, 90)),
        ("כבל HDMI 2.1 8K אורך 5 מטר", "HDMI 2.1 8K Cable 5M", (12, 50)),
        ("דיסק SSD חיצוני 1TB", "1TB External SSD Drive", (60, 180)),
        ("מצלמת רשת 4K למחשב", "4K Webcam for Computer", (40, 180)),
        ("מתאם USB-C לכל החיבורים", "USB-C All-in-One Adapter", (25, 100)),
        ("מערכת בית חכם Starter Kit", "Smart Home Starter Kit", (80, 400)),
        ("מנעול חכם לדלת עם אפליקציה", "Smart Door Lock with App", (70, 350)),
        ("מצלמה נסתרת WiFi", "WiFi Hidden Camera", (30, 150)),
        ("רמקול חכם עם Alexa", "Smart Speaker with Alexa", (40, 200)),
        ("טאבלט ציור גרפי Wacom", "Wacom Graphic Drawing Tablet", (60, 350)),
        ("מערכת GPS לרכב מקיפה", "Complete Car GPS System", (50, 250)),
        ("משדר FM Bluetooth לרכב", "Bluetooth FM Car Transmitter", (10, 50)),
        ("מצלמת דרך 4K עם GPS", "4K Dash Cam with GPS", (60, 300)),
        ("מערכת שמע לרכב 7 אינץ", "7 inch Car Audio System", (80, 400)),
    ],
    'toys': [
        ("רובוט הרכבה מתקדם לילדים", "Advanced Build Robot for Kids", (40, 200)),
        ("סט משחקי קסמים מקצועי", "Professional Magic Tricks Set", (20, 100)),
        ("ערכת מדע כימיה לבית ספר", "School Chemistry Science Kit", (25, 120)),
        ("מכונית שלט רחוק 60 קמ\"ש", "60km/h RC Racing Car", (50, 250)),
        ("בלדרים לטיפוס על קיר", "Wall Climbing Rock Holds", (40, 200)),
        ("מטוס רחף על שלט רחוק", "Remote Control Glider Plane", (30, 150)),
        ("ערכת בניית גשרים", "Bridge Building Kit", (20, 100)),
        ("סט צעצועי מים לקיץ", "Summer Water Toys Set", (15, 80)),
        ("מיקרוסקופ דיגיטלי לילדים", "Digital Kids Microscope", (30, 150)),
        ("טלסקופ אסטרונומיה לילדים", "Kids Astronomy Telescope", (40, 200)),
        ("ערכת יצירת רובוט", "DIY Robot Creation Kit", (25, 130)),
        ("סט משחקי חשיבה יפניים", "Japanese Brain Games Set", (15, 90)),
        ("מבוך מגנטי מתקדם", "Advanced Magnetic Maze", (18, 100)),
        ("מטוס נייר חשמלי נטען", "Rechargeable Electric Paper Plane", (15, 80)),
        ("ערכת בנייה הנדסית", "Engineering Construction Kit", (30, 160)),
        ("צעצוע רובה חצים", "Bow and Arrow Toy Set", (12, 70)),
        ("בית בובות מתקפל", "Foldable Dollhouse", (35, 180)),
        ("סט בישול צעצוע מעץ", "Wooden Cooking Play Set", (20, 110)),
        ("מגרד לחתולים בית גדול", "Large Cat Scratching House", (25, 140)),
        ("ערכת יצירת סבונים", "DIY Soap Making Kit", (15, 85)),
    ],
    'home_garden': [
        ("מערכת השקיה חכמה WiFi", "WiFi Smart Irrigation", (40, 220)),
        ("מכונת קפה נספרסו אוטומטית", "Automatic Espresso Machine", (100, 600)),
        ("מטחנת בשר חשמלית 2000W", "2000W Electric Meat Grinder", (50, 280)),
        ("מסחטת מיצים איטית מקצועית", "Professional Slow Juicer", (60, 350)),
        ("מכונת לחם אוטומטית דיגיטלית", "Digital Automatic Bread Maker", (70, 400)),
        ("מערכת טיהור מים 5 שלבים", "5-Stage Water Purification", (80, 450)),
        ("מנורת UV לחיטוי חדרים", "UV Room Sanitizing Lamp", (30, 180)),
        ("מטהר אוויר HEPA לבית", "HEPA Home Air Purifier", (60, 400)),
        ("מערכת ביטחון ביתית אלחוטית", "Wireless Home Security", (70, 450)),
        ("מנעול דלת חכם ביומטרי", "Biometric Smart Door Lock", (80, 500)),
        ("מצלמה נסתרת לבית HD", "HD Hidden Home Camera", (25, 180)),
        ("מערכת בקרת אקלים חכמה", "Smart Climate Control", (90, 650)),
        ("שואב אבק רובוטי לבית", "Home Robotic Vacuum", (120, 700)),
        ("מנקה חלונות רובוטי", "Window Cleaning Robot", (80, 450)),
        ("מערכת שמע ביתית Bluetooth", "Home Bluetooth Audio System", (50, 350)),
        ("מקרר מיני לחדר 50 ליטר", "50L Mini Fridge", (80, 400)),
        ("מערכת גילוי עשן חכמה", "Smart Smoke Detection", (25, 150)),
        ("מנורת שולחן LED מתכווננת", "Adjustable LED Desk Lamp", (20, 130)),
        ("מארגן חדר ארונות מודולרי", "Modular Closet Organizer", (40, 250)),
        ("שטיח מטבח אנטי-החלקה", "Anti-Slip Kitchen Mat", (12, 80)),
    ],
    'tools': [
        ("מקדחה רוטטת נטענת 20V", "20V Cordless Rotary Hammer", (80, 450)),
        ("מסור שולחני 10 אינץ", "10 inch Table Saw", (150, 850)),
        ("מכונת חריטת עץ CNC שולחנית", "Desktop Wood CNC Machine", (250, 1500)),
        ("מלחם תעשייתי 80W", "80W Industrial Soldering", (30, 200)),
        ("מד לחץ דיגיטלי מדויק", "Precision Digital Pressure Gauge", (20, 140)),
        ("מערכת שאיבת אבק תעשייתית", "Industrial Dust Collection", (60, 450)),
        ("מצלמה בורסקופית HD", "HD Borescope Camera", (20, 180)),
        ("מד טמפרטורה לייזר -50 עד 550", "-50 to 550 Laser Thermometer", (25, 200)),
        ("מערכת ריתוך MIG/MAG", "MIG/MAG Welding System", (250, 1400)),
        ("מכונת חיתוך פלזמה 50A", "50A Plasma Cutter", (350, 2000)),
        ("מערכת כרסום CNC 3 צירים", "3-Axis CNC Milling", (600, 3500)),
        ("מקדחת עמוד שולחנית", "Bench Drill Press", (100, 600)),
        ("מסור סרט שולחני", "Bench Band Saw", (120, 750)),
        ("משחזת זווית 7 אינץ", "7 inch Angle Grinder", (40, 280)),
        ("מצלמה תרמית לבניין", "Building Thermal Camera", (180, 1200)),
        ("מד עובי ציפוי דיגיטלי", "Digital Coating Thickness Meter", (50, 350)),
        ("מערכת ריתוך אלקטרונית", "Electronic Welding System", (90, 650)),
        ("מכשיר בדיקת גזים", "Gas Testing Device", (40, 300)),
        ("מצלמה בדיקת צנרת", "Pipe Inspection Camera", (60, 450)),
        ("מערכת כלי עבודה מקצועית", "Professional Tool System", (100, 700)),
    ],
    'jewish': [
        ("סט תפילין מהודרות גסות מיוחד", "Special Mehudar Tefillin", (220, 900)),
        ("תיק טלית ותפילין עור אמיתי", "Genuine Leather Tallit Bag", (45, 220)),
        ("מזוזה מהודרת 12 ס\"מ כתב ספרדי", "12cm Mehudar Mezuzah", (60, 280)),
        ("חנוכיה כסף 925 מעוצבת", "925 Silver Designer Menorah", (120, 800)),
        ("סט פמוטי שבת נחושת מוברשת", "Brushed Copper Candlesticks", (35, 180)),
        ("סידור תפילה עם פירוש הגר\"א", "Gra Siddur with Commentary", (30, 160)),
        ("ספר תהילים עם ביאור מטה אפרים", "Mateh Ephraim Tehillim", (18, 120)),
        ("סט חומש אור החיים 5 כרכים", "Or Hachaim Chumash Set", (70, 450)),
        ("ספר משנה ברורה 24 כרכים", "24 Vol Mishnah Berurah", (100, 650)),
        ("סט שולחן ערוך הרב קוק", "Rav Kook Shulchan Aruch", (140, 900)),
        ("מחזור ראש השנה מפורש", "Rosh Hashanah Machzor", (25, 150)),
        ("הגדה של פסח בני יששכר", "Bnei Yissachar Haggadah", (15, 100)),
        ("סט תפילות שבת מבוארות", "Shabbat Prayers Explained", (35, 250)),
        ("תיקי תפילין מהודרים עור", "Leather Mehudar Tefillin Bags", (25, 180)),
        ("טלית קטן מהודר צמר", "Mehudar Wool Tzitzit Katan", (12, 90)),
        ("קרש חלה עץ מהגוני מעוטר", "Decorated Mahogany Challah Board", (30, 200)),
        ("גביע קידוש כסף מצופה", "Silver Plated Kiddush Cup", (20, 160)),
        ("מעמד נרות שבת מתכוונן", "Adjustable Shabbat Candle Holder", (15, 110)),
        ("סט כיסויים לספרים", "Book Cover Set", (18, 130)),
        ("קופסת אתרוג מהודרת", "Mehudar Etrog Box", (25, 180)),
    ],
    'sports': [
        ("גלשן גלים סופט 8 פיט", "8ft Soft Surfboard", (100, 550)),
        ("חליפת צלילה יבשה מקצועית", "Professional Dry Suit", (250, 1500)),
        ("מסיכת צלילה פנoramית", "Panoramic Diving Mask", (40, 280)),
        ("סנפירי שחייה ארוכים", "Long Swimming Fins", (25, 180)),
        ("מצוף הצלה אוטומטי", "Automatic Life Float", (20, 150)),
        ("מקלות טיולים מתקפלים 3 קטעים", "3-Section Trekking Poles", (25, 190)),
        ("תרמיל גב 80 ליטר לטיולים", "80L Hiking Backpack", (50, 400)),
        ("מזרן שטח מתנפח כפול", "Double Inflatable Camping Mat", (35, 280)),
        ("אוהל משפחתי 8 אנשים", "8 Person Family Tent", (120, 900)),
        ("כירת שטח גז כפולה", "Double Gas Camping Stove", (40, 300)),
        ("פנס ראש LED חזק 1000 לומן", "1000 Lumen LED Headlamp", (20, 180)),
        ("מערכת מים ניידת לטיולים", "Portable Hiking Water System", (45, 350)),
        ("גלשן SUP מתקפל נייד", "Portable Foldable SUP", (120, 850)),
        ("חליפת צלילה 7 ממ לקור", "7mm Cold Water Wetsuit", (80, 600)),
        ("מערכת שנירקול מלאה", "Complete Snorkeling System", (50, 400)),
        ("מגני שיניים מקצועיים", "Professional Mouth Guards", (12, 100)),
        ("מערכת אימון TRX Pro", "TRX Pro Training System", (40, 320)),
        ("מכשיר EMS לאימון שרירים", "EMS Muscle Training Device", (50, 420)),
        ("סט משקולות אולימפיות 150 קג", "150kg Olympic Weight Set", (180, 1400)),
        ("ספת כושר מתכווננת מקצועית", "Professional Adjustable Bench", (100, 800)),
    ],
    'car': [
        ("מערכת אנדרואיד לרכב 10 אינץ", "10 inch Android Car System", (100, 650)),
        ("מצלמת 360 מעלות לרכב 4K", "4K 360 Car Camera", (90, 600)),
        ("מערכת התנעה מרחוק חכמה GPS", "Smart GPS Remote Start", (70, 500)),
        ("מערכת חיישני חנייה קדמיים", "Front Parking Sensors", (35, 280)),
        ("מערכת התרעת מכוניות בסימן מת", "Blind Spot Warning System", (45, 380)),
        ("מעקב GPS מתקדם לרכב", "Advanced Car GPS Tracker", (55, 480)),
        ("מנעול הגה נגד גניבה מתקדם", "Advanced Anti-Theft Lock", (18, 150)),
        ("מערכת אזעקה לרכב עם אפליקציה", "Car Alarm with App", (90, 700)),
        ("מטען קפיצה 20000mAh לרכב", "20000mAh Car Jump Starter", (50, 450)),
        ("מערכת שמע היי-פי 9 רמקולים", "9 Speaker Hi-Fi Car Audio", (140, 1200)),
        ("מערכת וידאו אנדרואיד לרכב", "Android Car Video System", (110, 900)),
        ("כיסוי מושבים מפנק עור", "Luxury Leather Seat Covers", (60, 550)),
        ("מערכת ניטור לחץ צמיגים TPMS", "TPMS Tire Pressure Monitor", (30, 280)),
        ("רדאר גילוי מכשולים אחורי", "Rear Obstacle Detection Radar", (25, 220)),
        ("מערכת נעילה מרכזית לרכב", "Car Central Locking System", (45, 420)),
        ("מברשת ניקוי חשמלית לרכב", "Electric Car Cleaning Brush", (25, 220)),
        ("מכונת פוליש לרכב חשמלית", "Electric Car Polisher", (40, 380)),
        ("מד מהירות Heads-Up Display", "Heads-Up Speed Display", (30, 280)),
        ("מגן מנוע מתכת לרכב", "Metal Car Engine Guard", (45, 420)),
        ("מערכת חימום מושבים לרכב", "Car Seat Heating System", (35, 320)),
    ],
    'pet': [
        ("בית חכם מחומם לחתולים", "Smart Heated Cat House", (70, 550)),
        ("מערכת מזון אוטומטית WiFi HD", "WiFi HD Automatic Feeder", (60, 500)),
        ("מזרקת מים חכמה עם פילטר", "Smart Water Fountain Filter", (35, 320)),
        ("מיטה אורטופדית גדולה לכלבים", "Large Orthopedic Dog Bed", (35, 320)),
        ("ציוד טיפוח מקצועי לכלבים", "Pro Dog Grooming Equipment", (40, 400)),
        ("GPS מדויק לכלבים בזמן אמת", "Real-time Dog GPS Tracker", (60, 550)),
        ("מזון יבש פרימיום 20 קג כלבים", "Premium Dog Food 20kg", (40, 380)),
        ("מזון יבש פרימיום 15 קג חתולים", "Premium Cat Food 15kg", (35, 350)),
        ("חטיפים טבעיים 5 קג לכלבים", "Natural Dog Treats 5kg", (20, 200)),
        ("צעצועי לעיסה חזקים במיוחד", "Extra Strong Chew Toys", (15, 150)),
        ("מערכת משחק אינטראקטיבית WiFi", "WiFi Interactive Play System", (30, 300)),
        ("מנשא נוח לחיות מחמד לטיולים", "Travel Pet Carrier", (22, 220)),
        ("בגדים לכלבים לחורף סט 5", "Winter Dog Clothes Set 5", (25, 250)),
        ("נעליים לכלבים לטיולים סט 4", "Dog Walking Shoes Set 4", (18, 180)),
        ("מיטה מחוממת לחיות מחמד", "Heated Pet Bed", (30, 300)),
        ("ערכת טיפוח בסיסית לחתולים", "Basic Cat Grooming Kit", (20, 200)),
        ("צעצועי חתולים אינטראקטיביים", "Interactive Cat Toys Set", (15, 150)),
        ("קולר חכם לכלבים עם GPS", "Smart Dog Collar with GPS", (40, 420)),
        ("מזרקת מים אוטומטית לחתולים", "Automatic Cat Water Fountain", (25, 250)),
    ],
    'office': [
        ("מדפסת לייזר צבעונית WiFi A3", "A3 WiFi Color Laser Printer", (180, 1500)),
        ("סורק מסמכים אוטומטי ADF", "ADF Document Scanner", (100, 900)),
        ("מצלמת מסמכים HD למורה", "HD Document Camera for Teachers", (50, 550)),
        ("לוח מחיק חכם 86 אינץ", "86 inch Smart Whiteboard", (250, 2500)),
        ("מערכת ועידת וידאו 4K", "4K Video Conference System", (150, 1500)),
        ("מצלמת רשת 4K למשרד", "4K Office Webcam", (35, 450)),
        ("מיקרופון אלחוטי למשרד", "Wireless Office Microphone", (30, 400)),
        ("רמקולים למשרד סראונד", "Office Surround Speakers", (40, 500)),
        ("מעמד מסך מתכוונן כפול", "Dual Adjustable Monitor Arm", (35, 450)),
        ("שולחן עבודה מתכוונן חשמלי", "Electric Adjustable Desk", (220, 2000)),
        ("כיסא משרדי ארגונומי יוקרתי", "Luxury Ergonomic Office Chair", (120, 1500)),
        ("מגן מסך פרטיות 27 אינץ", "27 inch Privacy Screen", (20, 250)),
        ("מערכת גיבוי NAS 4 טרה", "4TB NAS Backup System", (180, 1800)),
        ("סט ציוד משרדי יוקרתי", "Luxury Office Supplies Set", (120, 1200)),
        ("מערכת אבטחת מידע למשרד", "Office Data Security System", (90, 1100)),
        ("מדפסת תרמית ניידת", "Portable Thermal Printer", (50, 550)),
        ("לוח תכנון חכם דיגיטלי", "Smart Digital Planning Board", (80, 900)),
        ("מערכת ניהול מסמכים דיגיטלית", "Digital Document Management", (100, 1100)),
        ("מקרן נייד HD למשרד", "Portable HD Office Projector", (150, 1500)),
        ("מערכת שמע למשרד conference", "Conference Room Audio System", (200, 2000)),
    ],
    'art': [
        ("מכונת חריטת לייזר 40W", "40W Laser Engraver", (220, 2200)),
        ("מדפסת תלת מימד FDM מקצועית", "Professional FDM 3D Printer", (180, 1800)),
        ("סט ציור שמן 72 צבעים מקצועי", "Pro 72 Color Oil Paint Set", (35, 550)),
        ("מכונת כתיבה וינטג' פעילה", "Working Vintage Typewriter", (90, 1100)),
        ("ציוד תאורת סטודיו מקצועי", "Pro Studio Lighting Kit", (70, 900)),
        ("מסך ציור גרפי 22 אינץ 4K", "22 inch 4K Drawing Tablet", (120, 1500)),
        ("עט דיגיטלי Wacom Pro", "Wacom Pro Digital Pen", (50, 600)),
        ("מכונת רקמה מקצועית 10 מחטים", "10 Needle Pro Embroidery", (220, 2800)),
        ("סט פיסול חימר מקצועי מלא", "Complete Pro Clay Kit", (40, 650)),
        ("ציוד יצירת תכשיטים מקצועי", "Pro Jewelry Making Tools", (35, 550)),
        ("מכונת חיתוך ויניל Cricut Pro", "Cricut Pro Vinyl Cutter", (120, 1500)),
        ("סט ציור דיוקנאות מקצועי", "Pro Portrait Art Set", (25, 450)),
        ("ציוד קעקועים למתחילים", "Beginner Tattoo Equipment", (70, 1100)),
        ("מערכת הדפסה על חולצות DTG", "DTG T-Shirt Printing System", (120, 1800)),
        ("סט צילום סטודיו ביתי", "Home Studio Photography Set", (60, 900)),
        ("מכונת חריטת עץ CNC 3018", "3018 Wood CNC Machine", (150, 1500)),
        ("ציוד יצירת נרות מקצועי", "Pro Candle Making Kit", (30, 550)),
        ("סט ציור אקריליק נוזלי", "Liquid Acrylic Painting Set", (20, 450)),
        ("מכונת רקמה ידנית", "Hand Embroidery Machine", (80, 1100)),
    ],
}


def generate_product_id():
    return f"100500{random.randint(100000000, 999999999)}"


def add_products():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Adding More Products - Target: 3000+ products")
        print("=" * 60)
        
        existing_count = Product.query.count()
        print(f"Current products: {existing_count}")
        
        total_added = 0
        
        for category_key, products in MORE_PRODUCTS.items():
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
        print("BATCH COMPLETE!")
        print(f"{'='*60}")
        print(f"New products added: {total_added}")
        print(f"Total products in database: {Product.query.count()}")


if __name__ == '__main__':
    add_products()
