#!/usr/bin/env python
"""
Add thousands more products to reach 2000+ products total.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
from app import create_app, db
from app.models.database import Product
from config import Config

# Extended product templates - 20+ per category
EXTENDED_TEMPLATES = {
    'electronic': [
        ("אוזניות אלחוטיות עם סינון רעשים", "Wireless Noise Cancelling Earbuds", (25, 120)),
        ("רמקול חכם עם עוזר קולי", "Smart Speaker with Voice Assistant", (30, 150)),
        ("טאבלט 10 אינץ עם Android", "10 inch Android Tablet", (80, 250)),
        ("מצלמת פעולה 4K עמידה במים", "4K Waterproof Action Camera", (40, 180)),
        ("מטען רכב USB מהיר שקע כפול", "Fast Dual USB Car Charger", (8, 25)),
        ("סוללה נטענת AA/AAA עם מטען", "Rechargeable Battery Set with Charger", (15, 45)),
        ("מצלמת דלת חכמה עם WiFi", "Smart Doorbell Camera with WiFi", (35, 120)),
        ("משדר FM בלוטות לרכב", "Bluetooth FM Transmitter for Car", (10, 35)),
        ("מיקרופון USB למחשב ושיחות", "USB Microphone for PC and Calls", (20, 80)),
        ("סטנד למחשב נייד מתכוונן", "Adjustable Laptop Stand", (12, 40)),
        ("מאוורר USB שקט למחשב", "Quiet USB Cooling Fan", (8, 25)),
        ("מתאם USB-C לכל החיבורים", "USB-C Multiport Adapter", (15, 50)),
        ("כבל HDMI 2.1 8K אורך 3 מטר", "HDMI 2.1 Cable 8K 3M", (10, 30)),
        ("מצלמת אינטרנט 4K עם כיסוי", "4K Webcam with Privacy Cover", (25, 90)),
        ("תחנת עגינה למחשב נייד USB-C", "USB-C Laptop Docking Station", (40, 150)),
        ("קורא כרטיסים USB 3.0 רב תכליתי", "Multi Card Reader USB 3.0", (8, 25)),
        ("בקר משחק USB אלחוטי", "Wireless USB Game Controller", (20, 70)),
        ("מנורת לילה LED עם חיישן", "LED Night Light with Sensor", (8, 25)),
        ("שעון מעורר דיגיטלי גדול", "Large Digital Alarm Clock", (12, 40)),
        ("מדחום דיגיטלי לבית", "Digital Home Thermometer", (10, 30)),
    ],
    'toys': [
        ("מכונית רובוטית הניתנת לתכנות", "Programmable Robot Car", (30, 100)),
        ("ערכת מדע לילדים 100 ניסויים", "Kids Science Kit 100 Experiments", (25, 80)),
        ("מטוסי נייר חשמליים סט 3", "Electric Paper Airplanes Set 3", (15, 45)),
        ("בובות תיאטרון בובות מעץ", "Wooden Puppet Theater Set", (30, 90)),
        ("קוביות מגנטיות לבנייה 100 חלקים", "Magnetic Building Blocks 100pcs", (20, 70)),
        ("ערכת אריגה וסריגה לילדים", "Kids Weaving and Knitting Kit", (15, 50)),
        ("מיני בריכה מתנפחת לילדים", "Kids Inflatable Mini Pool", (20, 60)),
        ("מצנח צעצוע לריצה", "Parachute Toy for Running", (10, 30)),
        ("בלונים ארוכים לקעקועים 100 יח", "Long Balloons for Twisting 100pcs", (8, 25)),
        ("ערכת גינון לילדים עם כלים", "Kids Gardening Kit with Tools", (15, 45)),
        ("מזרקת בועות סבון אוטומטית", "Automatic Bubble Blower", (12, 40)),
        ("מצלמה לילדים עמידה במים", "Waterproof Kids Camera", (25, 70)),
        ("ערכת תפירה ראשונה לילדים", "My First Sewing Kit for Kids", (12, 35)),
        ("לוח ציור מגנטי צבעוני גדול", "Large Magnetic Drawing Board", (15, 45)),
        ("תחפושות לילדים סט 5 תחפושות", "Kids Dress Up Costumes Set 5", (20, 60)),
        ("בלדרים לטיפוס בבית", "Indoor Rock Climbing Holds", (30, 100)),
        ("מגדל כוסות מהירות משחק חשיבה", "Speed Stacking Cups Game", (10, 30)),
        ("סט ציור על בד עם מסגרות", "Canvas Painting Set with Frames", (18, 55)),
        ("קליעה למטרה עם חצים וקשת", "Target Archery Set with Bow", (25, 80)),
    ],
    'home_garden': [
        ("מנורת שולחן מעוצבת וינטג", "Vintage Style Desk Lamp", (25, 75)),
        ("מחזיק מגבות חם חשמלי", "Electric Towel Warmer", (40, 120)),
        ("מסנן מים לברז ביתי", "Home Faucet Water Filter", (20, 60)),
        ("סט כריות נוי לסלון 4 יח", "Decorative Throw Pillows Set 4", (25, 80)),
        ("מארגן תכשיטים עם מראה", "Jewelry Organizer with Mirror", (15, 50)),
        ("מנורת לילה לילדים עם שלט", "Kids Night Light with Remote", (12, 40)),
        ("מכונת קפה טורקית חשמלית", "Electric Turkish Coffee Maker", (30, 90)),
        ("מערכת השקיה אוטומטית לגינה", "Automatic Garden Watering System", (25, 80)),
        ("ספסל גינה מתקפל עם איחסון", "Folding Garden Bench with Storage", (50, 180)),
        ("מנורת חירום LED נטענת", "Rechargeable LED Emergency Light", (15, 45)),
        ("מארגן נעליים לארון 10 קומות", "10-Tier Shoe Rack for Closet", (20, 60)),
        ("מגבת חדר אמבטיה מפנקת סט 3", "Luxury Bathroom Towel Set 3", (25, 80)),
        ("מצעים למיטה זוגית סט מלא", "Full Bed Sheet Set Queen", (30, 100)),
        ("שטיח שולחן אוכל עמיד בכתמים", "Stain Resistant Dining Rug", (40, 150)),
        ("מעמד יין לשולחן 6 בקבוקים", "Tabletop Wine Rack 6 Bottles", (18, 55)),
        ("מטהר אוויר ביתי עם פחם", "Home Air Purifier with Carbon", (50, 200)),
        ("מנקה חלונות רובוטי אוטומטי", "Automatic Window Cleaning Robot", (80, 250)),
        ("תרמוס שומר חום 24 שעות", "24-Hour Heat Keeping Thermos", (15, 50)),
        ("ערכת תיקונים לבית 100 חלקים", "Home Repair Kit 100 Pieces", (25, 80)),
    ],
    'tools': [
        ("סט מקדחות ומסורים נטענות", "Cordless Drill and Saw Combo", (80, 250)),
        ("מצלמה תרמית לבדיקת חשמל", "Thermal Camera for Electrical", (120, 400)),
        ("מד לחץ אוויר דיגיטלי לרכב", "Digital Tire Pressure Gauge", (10, 35)),
        ("מכשיר בדיקת מתח חשמלי ללא מגע", "Non-Contact Voltage Tester", (8, 30)),
        ("מברג חשמלי עם שליטת מהירות", "Variable Speed Electric Screwdriver", (25, 80)),
        ("משחזת ספסל חשמלית 6 אינץ", "6 inch Bench Grinder", (40, 150)),
        ("מסור גחון חשמלי נטען", "Cordless Jigsaw Electric", (50, 180)),
        ("מכונת חיתוך לזוויות מדוייקת", "Precision Miter Saw", (60, 200)),
        ("משאבת מים נטענת לתעשייתית", "Industrial Cordless Water Pump", (45, 160)),
        ("כלי עבודה ידניים סט 200 חלקים", "Hand Tool Set 200 Pieces", (50, 200)),
        ("מנוף הידראולי 2 טון", "2 Ton Hydraulic Jack", (30, 100)),
        ("מצלמה בורסקופית עם מסך", "Borescope Camera with Screen", (35, 120)),
        ("סט מפתחות דינמומטריים", "Torque Wrench Set", (40, 150)),
        ("מכונת לחץ אוויר ניידת", "Portable Air Compressor", (50, 180)),
        ("מברג אוויר תעשייתי", "Industrial Air Impact Wrench", (60, 200)),
        ("מכשיר לייזר למדידת מרחק", "Laser Distance Measuring Tool", (25, 90)),
        ("סט כלים לעבודה עם עץ", "Woodworking Tool Set", (35, 120)),
        ("משחזת זווית מיני 3 אינץ", "Mini 3 inch Angle Grinder", (25, 90)),
        ("ערכת חשמלאי מקצועית", "Professional Electrician Kit", (40, 150)),
    ],
    'jewish': [
        ("תפארת ישראל מלא עם תרגום", "Tiferet Yisrael Siddur Full", (25, 70)),
        ("סט שמונה תפארת ישראל לבני הזוג", "Tiferet Yisrael Couple Set 8", (150, 400)),
        ("מזוזה מהודרת כתב ספרדי", "Mehudar Mezuzah Sefardi Script", (40, 150)),
        ("מזוזה מהודרת כתב אשכנזי", "Mehudar Mezuzah Ashkenazi Script", (40, 150)),
        ("תיק טלית ותפילין דמוי עור", "Faux Leather Tallit Tefillin Bag", (20, 70)),
        ("נטילת ידיים קערה נירוסטה", "Stainless Steel Netilat Yadayim Cup", (15, 50)),
        ("קערת לחם פסח מעוצבת", "Decorated Pesach Bread Plate", (25, 80)),
        ("סט חנוכה שלם נירוסטה", "Complete Stainless Hanukkah Set", (30, 100)),
        ("נרות שבת בלתי כבים ארוכים", "Long Lasting Shabbat Candles", (10, 35)),
        ("בשמים למהavdilת בלתי כבים", "Besamim for Havdala", (8, 30)),
        ("גביעי קידוש זכוכית מעוטרים", "Decorated Glass Kiddush Cups", (20, 70)),
        ("מגש חלה מנירוסטה מעוצב", "Decorated Stainless Challah Tray", (25, 90)),
        ("כיסוי חלה רקום יוקרתי", "Luxury Embroidered Challah Cover", (18, 65)),
        ("זוג פמוטי שבת מברונזה", "Bronze Shabbat Candlesticks Pair", (30, 120)),
        ("מפה לשולחן שבת דגם עתיק", "Antique Style Shabbat Tablecloth", (25, 90)),
        ("סט כלים לפסח מיוחדים", "Special Pesach Utensils Set", (35, 120)),
        ("מצה שמורה מכוסה בעיטור", "Decorated Covered Matzah Holder", (20, 75)),
        ("ספר תהילים כיס עם תרגום", "Pocket Tehillim with Translation", (10, 40)),
        ("מזוזה למכונית עם ברכה", "Car Mezuzah with Blessing", (8, 30)),
    ],
    'sports': [
        ("מצנח רחיפה לים מקצועי", "Professional Parasailing for Sea", (40, 150)),
        ("גלשן סאפ מתנפח עם משוט", "Inflatable SUP Board with Paddle", (150, 500)),
        ("חליפת צלילה לילדים 3 ממ", "Kids Wetsuit 3mm", (30, 100)),
        ("משקפי שחייה נגד ערפל UV", "Anti-Fog UV Swimming Goggles", (10, 35)),
        ("מצילה חכמה אוטומטית", "Smart Automatic Life Vest", (50, 180)),
        ("ערכת כדורעף חופים מלאה", "Complete Beach Volleyball Set", (40, 150)),
        ("מגרד מקצועי לבריכות", "Professional Pool Skimmer", (15, 50)),
        ("מזרן שטח עמיד במים", "Waterproof Ground Mat", (20, 70)),
        ("מנורת ראש LED לטיולים", "LED Headlamp for Hiking", (10, 40)),
        ("מקלות טיולים מתקפלים קרבון", "Carbon Fiber Folding Trekking Poles", (30, 100)),
        ("תרמיל מים 3 ליטר לטיולים", "3 Liter Hiking Water Bladder", (15, 50)),
        ("בגד ים שרוול ארוך לגברים", "Men's Long Sleeve Swim Shirt", (15, 50)),
        ("מצילת חוף מקצועית", "Professional Lifeguard Float", (25, 90)),
        ("כדורסל רחוב עם רשת", "Street Basketball with Net", (20, 70)),
        ("מגן ברכיים ומרפקים לספורט", "Sports Knee and Elbow Pads", (12, 45)),
        ("מכשיר למדידת דופק בכף יד", "Handheld Heart Rate Monitor", (15, 55)),
        ("גלגיליות מקצועיות לרחוב", "Professional Street Rollerblades", (50, 200)),
        ("חצובת מצלמה קלה למטיילים", "Lightweight Traveler Camera Tripod", (20, 80)),
        ("שק שינה לקמפינג משפחתי", "Family Camping Sleeping Bag", (40, 150)),
    ],
    'car': [
        ("מערכת מולטימדיה לרכב עם GPS", "Car Multimedia System with GPS", (80, 300)),
        ("מצלמת רוורס HD לרכב", "HD Car Reverse Camera", (20, 70)),
        ("בוסטר מושב לילדים עם הגנה", "Child Car Seat Booster with Protection", (30, 120)),
        ("מנקה אבק רטוב/יבש לרכב", "Wet/Dry Car Vacuum Cleaner", (25, 90)),
        ("מטען דחף לרכב חירום", "Emergency Car Jump Starter", (40, 150)),
        ("מערכת חניה אוטומטית חכמה", "Smart Automatic Parking System", (60, 250)),
        ("מערכת איתות לרכב ללא חיווט", "Wireless Car Turn Signal System", (15, 55)),
        ("מזגן נייד לרכב 12V", "Portable 12V Car Air Conditioner", (50, 200)),
        ("כיסוי מושבים מלא עם כריות", "Full Car Seat Cover with Cushions", (40, 150)),
        ("מערכת ניווט GPS לרכב", "Car GPS Navigation System", (50, 200)),
        ("משדר בלוטות לאודיו רכב", "Bluetooth Audio Transmitter for Car", (12, 45)),
        ("מערכת מעקב GPS נסתרת לרכב", "Hidden GPS Tracker for Car", (25, 100)),
        ("מנורת חירום לרכב LED", "LED Car Emergency Light", (10, 40)),
        ("מצבר נייד לרכב חירום", "Portable Car Battery Emergency", (30, 120)),
        ("מערכת נעילה מרכזית לרכב", "Central Locking System for Car", (40, 180)),
        ("מברשת ניקוי גלגלים חשמלית", "Electric Wheel Cleaning Brush", (20, 80)),
        ("מכונת פוליש לרכב חשמלית", "Electric Car Polishing Machine", (35, 150)),
        ("מד מהירות דיגיטלי Heads-Up", "Digital HUD Speedometer", (25, 100)),
        ("מגן מנוע לרכב מתכת", "Metal Car Engine Guard", (40, 180)),
    ],
    'pet': [
        ("מיטה מחוממת לחתולים לחורף", "Heated Cat Bed for Winter", (25, 90)),
        ("מכונת מזון אוטומטית לכלבים", "Automatic Dog Feeder", (40, 150)),
        ("מערכת מים זורמים לחיות מחמד", "Pet Water Fountain System", (20, 80)),
        ("בית לחתולים עם גרדן משולב", "Cat House with Scratching Post", (30, 120)),
        ("מכשיר אילוף לכלבים אלקטרוני", "Electronic Dog Training Device", (25, 100)),
        ("אוהל נייד לכלבים לטיולים", "Portable Dog Tent for Travel", (20, 80)),
        ("ציוד טיפוח מקצועי לכלבים", "Professional Dog Grooming Kit", (30, 120)),
        ("חטיפים לכלבים טבעיים אריזה", "Natural Dog Treats Bulk Pack", (15, 60)),
        ("משחקי אינטראקציה לחתולים", "Interactive Cat Toys Set", (12, 50)),
        ("מזרן אורטופדי לכלבים גדולים", "Orthopedic Dog Bed Large", (35, 150)),
        ("קערת מזון איטית אינטראקטיבית", "Interactive Slow Feed Bowl", (15, 60)),
        ("מנשא לחיות מחמד לתיק גב", "Pet Carrier Backpack Style", (25, 100)),
        ("צעצועי לעיסה לכלבים חזקים", "Heavy Duty Chew Toys for Dogs", (10, 45)),
        ("מערכת GPS לכלבים עם גדר", "GPS Dog System with Geofence", (50, 200)),
        ("מברשת ניקוי אוטומטית לחתולים", "Automatic Cat Grooming Brush", (20, 80)),
        ("מיטה צפה לכלבים לבריכה", "Floating Dog Pool Bed", (15, 60)),
        ("מזון יבש לכלבים אריזת חיסכון", "Dry Dog Food Value Pack", (30, 120)),
        ("ביתן לחיות מחמד לחצר", "Outdoor Pet House for Yard", (40, 180)),
        ("ציוד רפואי בסיסי לחיות מחמד", "Basic Pet Medical Kit", (15, 60)),
    ],
    'office': [
        ("מדפסת תרמית ניידת Bluetooth", "Portable Thermal Printer Bluetooth", (40, 180)),
        ("סט מחברות מהודרות A5 6 יח", "Premium A5 Notebooks Set 6", (20, 70)),
        ("עט דיגיטלי חכם עם הקלטה", "Smart Digital Pen with Recording", (30, 120)),
        ("לוח מחיק חכם 42 אינץ", "Smart 42 inch Erasable Board", (80, 300)),
        ("מארגן כבלים לשולחן עבודה", "Desk Cable Organizer", (10, 40)),
        ("תמונה ממוסגרת דיגיטלית WiFi", "WiFi Digital Photo Frame", (50, 200)),
        ("מצלמת וידאו קונפרנס 4K", "4K Video Conference Camera", (60, 250)),
        ("מיקרופון שולחני למשרד", "Desktop Office Microphone", (25, 100)),
        ("סט ציוד משרדי מלא 50 חלקים", "Complete Office Supplies Set 50pcs", (30, 120)),
        ("משטח עכבר גדול עם טעינה", "Large Mouse Pad with Charging", (20, 80)),
        ("מחזיק מסמכים מתכוונן לשולחן", "Adjustable Document Holder", (15, 60)),
        ("מנורת שולחן LED עם טעינה", "LED Desk Lamp with Charging", (25, 100)),
        ("מגרסת נייר אישית מיני", "Personal Mini Paper Shredder", (20, 80)),
        ("סט תיקי פולדר מעוצבים 12", "Designer File Folders Set 12", (15, 60)),
        ("שעון קיר דיגיטלי גדול", "Large Digital Wall Clock", (15, 60)),
        ("לוח תכנון שבועי מגנטי", "Magnetic Weekly Planner Board", (20, 80)),
        ("מעמד למסמכים עם 5 תאים", "5 Slot Document Organizer", (12, 50)),
        ("מחשבון מדפסת היסטורי", "Printing Calculator with History", (30, 120)),
        ("סט אביזרים למשרד ביתי", "Home Office Accessories Set", (25, 100)),
    ],
    'art': [
        ("סט ציור שמן מקצועי 48 צבעים", "Professional Oil Paint Set 48", (30, 120)),
        ("סט פיסול חימר מקצועי", "Professional Clay Sculpting Set", (25, 100)),
        ("מכונת חיתוך ויניל ביתית", "Home Vinyl Cutting Machine", (80, 350)),
        ("ציוד צילום מקצועי למתחילים", "Beginner Professional Photography Kit", (50, 250)),
        ("סט צבעי גואש 36 צבעים", "Gouache Paint Set 36 Colors", (20, 80)),
        ("ערכת יצירת תכשיטים מלאה", "Complete Jewelry Making Kit", (25, 100)),
        ("סט ציור על משי עם צבעים", "Silk Painting Set with Colors", (20, 80)),
        ("מכשיר חריטת עץ חשמלי", "Electric Wood Engraving Tool", (25, 100)),
        ("סט ציור דיוקנאות מקצועי", "Professional Portrait Drawing Set", (30, 120)),
        ("ציוד קרמיקה ביתית מלא", "Complete Home Ceramics Kit", (40, 180)),
        ("סט צבעי אקריליק נוזליים", "Liquid Acrylic Paint Set", (20, 90)),
        ("מכונת רקמה ביתית דיגיטלית", "Digital Home Embroidery Machine", (150, 600)),
        ("ערכת ציור קיר מקצועית", "Professional Wall Painting Kit", (35, 150)),
        ("סט עטים טכניים 20 חלקים", "Technical Pens Set 20pcs", (18, 75)),
        ("ציוד פיסול אבן מקצועי", "Professional Stone Carving Kit", (40, 180)),
        ("מערכת הדפסה על חולצות", "T-Shirt Printing System", (100, 450)),
        ("סט ציור נוף מקצועי", "Professional Landscape Painting Set", (25, 110)),
        ("ציוד גרפיטי מקצועי למתחילים", "Beginner Graffiti Art Kit", (30, 130)),
        ("מכונת חיתוך נייר אומנותית", "Artistic Paper Cutting Machine", (40, 180)),
    ],
}


def generate_product_id():
    return f"100500{random.randint(100000000, 999999999)}"


def add_more_products():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Adding More Products - Target: 2000+ products")
        print("=" * 60)
        
        existing_count = Product.query.count()
        print(f"Current products: {existing_count}")
        
        total_added = 0
        
        for category_key, templates in EXTENDED_TEMPLATES.items():
            print(f"\n{'='*60}")
            print(f"Category: {Config.SAFE_CATEGORIES.get(category_key, category_key)}")
            print(f"{'='*60}")
            
            category_added = 0
            
            for title_hebrew, title_en, price_range in templates:
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
                        
                    except Exception as e:
                        db.session.rollback()
                        continue
            
            db.session.commit()
            print(f"  Added {category_added} products")
        
        print(f"\n{'='*60}")
        print("ADDITION COMPLETE!")
        print(f"{'='*60}")
        print(f"New products added: {total_added}")
        print(f"Total products in database: {Product.query.count()}")


if __name__ == '__main__':
    add_more_products()
