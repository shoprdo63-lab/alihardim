#!/usr/bin/env python
"""
Generate sample products for the store.
Creates thousands of realistic products across all categories.
"""
import os
os.environ['FLASK_ENV'] = 'development'

import random
from app import create_app, db
from app.models.database import Product
from config import Config

# Product templates by category - using proper string escaping
PRODUCT_TEMPLATES = {
    'electronic': [
        {'title_hebrew': "אוזניות בלוטות אלחוטיות מקצועיות", 'title_en': 'Wireless Bluetooth Headphones Pro', 'price_range': (15, 80)},
        {'title_hebrew': "מטען מהיר USB-C 65W", 'title_en': 'Fast Charger USB-C 65W', 'price_range': (12, 35)},
        {'title_hebrew': "כבל טעינה מהירה אורך 2 מטר", 'title_en': 'Fast Charging Data Cable 2M', 'price_range': (5, 15)},
        {'title_hebrew': "מטען נייד 20000mAh דק במיוחד", 'title_en': 'Power Bank 20000mAh Ultra Slim', 'price_range': (20, 50)},
        {'title_hebrew': "עכבר גיימינג RGB אופטי", 'title_en': 'Gaming Mouse RGB Optical', 'price_range': (10, 45)},
        {'title_hebrew': "מקלדת מכנית RGB לגיימרים", 'title_en': 'Mechanical Keyboard RGB', 'price_range': (25, 120)},
        {'title_hebrew': "רמקול בלוטות נייד עמיד במים", 'title_en': 'Portable Bluetooth Speaker Waterproof', 'price_range': (15, 60)},
        {'title_hebrew': "שעון חכם עם מד דופק ושינה", 'title_en': 'Smart Watch with Heart Rate Monitor', 'price_range': (25, 100)},
        {'title_hebrew': "מצלמת אבטחה WiFi HD לבית", 'title_en': 'WiFi Security Camera HD Home', 'price_range': (20, 80)},
        {'title_hebrew': "עמדת טעינה אלחוטית מהירה 15W", 'title_en': 'Fast Wireless Charger 15W', 'price_range': (12, 30)},
        {'title_hebrew': "האב USB 7 יציאות עם מתגים", 'title_en': 'USB Hub 7 Ports with Switches', 'price_range': (10, 25)},
        {'title_hebrew': "מצלמת רשת HD 1080P למחשב", 'title_en': 'Webcam HD 1080P for PC', 'price_range': (15, 50)},
        {'title_hebrew': "ממיר HDMI ל-VGA עם אודיו", 'title_en': 'HDMI to VGA Adapter with Audio', 'price_range': (8, 20)},
        {'title_hebrew': "דיסק און קי 128GB USB 3.0", 'title_en': 'USB Flash Drive 128GB USB 3.0', 'price_range': (10, 25)},
        {'title_hebrew': "כרטיס זיכרון microSD 256GB", 'title_en': 'MicroSD Card 256GB', 'price_range': (15, 40)},
    ],
    'toys': [
        {'title_hebrew': "סט בנייה לגו טכני 500 חלקים", 'title_en': 'Lego Technic Building Set 500pcs', 'price_range': (25, 80)},
        {'title_hebrew': "מכונית שלט רחוק 4WD עלית", 'title_en': 'Remote Control Car 4WD Off-Road', 'price_range': (30, 100)},
        {'title_hebrew': "רובוט לילדים הניתן לתכנות", 'title_en': 'Programmable Robot for Kids', 'price_range': (25, 70)},
        {'title_hebrew': "סט חידות עץ איכותי 6 חלקים", 'title_en': 'Wooden Puzzle Set 6pcs Quality', 'price_range': (15, 40)},
        {'title_hebrew': "דינוזאור טירקס אינטראקטיבי", 'title_en': 'Interactive T-Rex Dinosaur', 'price_range': (20, 60)},
        {'title_hebrew': "מגדל גנגה עץ איכותי 54 חלקים", 'title_en': 'Jenga Tower Wood 54pcs Quality', 'price_range': (12, 30)},
        {'title_hebrew': "סט פיסול חימר 24 צבעים", 'title_en': 'Clay Modeling Set 24 Colors', 'price_range': (10, 25)},
        {'title_hebrew': "מבוך מגנטי למיומנות וסבלנות", 'title_en': 'Magnetic Maze Skill Game', 'price_range': (12, 30)},
        {'title_hebrew': "מטוס נייר חשמלי לילדים", 'title_en': 'Electric Paper Plane for Kids', 'price_range': (15, 35)},
        {'title_hebrew': "סט קסמים 100 טריקים לילדים", 'title_en': 'Magic Set 100 Tricks for Kids', 'price_range': (18, 45)},
        {'title_hebrew': "רכבת חשמלית עם מסילה 3 מטר", 'title_en': 'Electric Train with 3m Track', 'price_range': (30, 80)},
        {'title_hebrew': "מיקרוסקופ לילדים x1200 הגדלה", 'title_en': 'Kids Microscope 1200x Magnification', 'price_range': (25, 60)},
    ],
    'home_garden': [
        {'title_hebrew': "מארגן מגירות מטבח סט 8 חלקים", 'title_en': 'Kitchen Drawer Organizer Set 8pcs', 'price_range': (15, 40)},
        {'title_hebrew': "קופסאות אחסון שקופות סט 6", 'title_en': 'Clear Storage Boxes Set 6', 'price_range': (12, 30)},
        {'title_hebrew': "מנורת שולחן LED עם 3 מצבי תאורה", 'title_en': 'LED Desk Lamp 3 Lighting Modes', 'price_range': (18, 50)},
        {'title_hebrew': "מדף קיר צף ללא קידוחים", 'title_en': 'Floating Wall Shelf No Drilling', 'price_range': (15, 40)},
        {'title_hebrew': "מתלה מעילים וכובעים 6 ווים", 'title_en': 'Coat and Hat Rack 6 Hooks', 'price_range': (12, 35)},
        {'title_hebrew': "פח אשפה אוטומטי עם חיישן", 'title_en': 'Automatic Trash Can with Sensor', 'price_range': (25, 70)},
        {'title_hebrew': "סל כביסה מתקפל עם ידיות", 'title_en': 'Collapsible Laundry Basket with Handles', 'price_range': (10, 25)},
        {'title_hebrew': "סט כלי גינה 5 חלקים עם תיק", 'title_en': 'Garden Tools Set 5pcs with Bag', 'price_range': (18, 45)},
        {'title_hebrew': "עציצי שתילה אוטומטית סט 3", 'title_en': 'Self-Watering Plant Pots Set 3', 'price_range': (15, 35)},
        {'title_hebrew': "מזרקת מים חשמלית לגינה", 'title_en': 'Electric Water Pump for Garden', 'price_range': (20, 50)},
        {'title_hebrew': "גריל פחמים נייד למחנאות", 'title_en': 'Portable Charcoal Grill Camping', 'price_range': (30, 80)},
        {'title_hebrew': "כיסא קמפינג מתקפל עם משענת", 'title_en': 'Folding Camping Chair with Backrest', 'price_range': (20, 50)},
    ],
    'tools': [
        {'title_hebrew': "מברגה מקדחה נטענת 18V סט מלא", 'title_en': 'Cordless Drill Driver 18V Full Set', 'price_range': (35, 120)},
        {'title_hebrew': "סט מברגים מקצועי 48 חלקים", 'title_en': 'Professional Screwdriver Set 48pcs', 'price_range': (15, 45)},
        {'title_hebrew': "ארגז כלים מקצועי 102 חלקים", 'title_en': 'Professional Tool Box 102pcs', 'price_range': (40, 150)},
        {'title_hebrew': "סט מפתחות שבדי 15 חלקים", 'title_en': 'Wrench Set 15pcs Chrome Vanadium', 'price_range': (18, 50)},
        {'title_hebrew': "מולטימטר דיגיטלי מקצועי", 'title_en': 'Digital Multimeter Professional', 'price_range': (12, 35)},
        {'title_hebrew': "אקדח דבק חם תעשייתי 60W", 'title_en': 'Industrial Hot Glue Gun 60W', 'price_range': (8, 25)},
        {'title_hebrew': "מסור חשמלי נטען לעץ ומתכת", 'title_en': 'Cordless Electric Saw for Wood/Metal', 'price_range': (45, 150)},
        {'title_hebrew': "משחזת זווית נטענת 4 אינץ", 'title_en': 'Cordless Angle Grinder 4 inch', 'price_range': (35, 100)},
        {'title_hebrew': "מצלמה תרמית לאיתור נזילות", 'title_en': 'Thermal Camera for Leak Detection', 'price_range': (150, 400)},
        {'title_hebrew': "רצועת כלים עם 14 כיסים", 'title_en': 'Tool Belt with 14 Pockets', 'price_range': (15, 40)},
    ],
    'jewish': [
        {'title_hebrew': "כיפה סרוגה איכותית עבודת יד", 'title_en': 'Handmade Knitted Kippah Quality', 'price_range': (8, 25)},
        {'title_hebrew': "טלית גדולה צמר מרובע 1.40m", 'title_en': 'Wool Tallit Gadol 1.40m Square', 'price_range': (25, 80)},
        {'title_hebrew': "ארבעה זוגות ציצית כשרה מהודרת", 'title_en': 'Four Pairs Tzitzit Kosher Mehudar', 'price_range': (12, 40)},
        {'title_hebrew': "חנוכיה כסף מעוצבת מהודרת", 'title_en': 'Decorated Silver Menorah Mehudar', 'price_range': (30, 150)},
        {'title_hebrew': "סט סביבוני עץ צבעוניים 4 יח", 'title_en': 'Colorful Wooden Dreidels Set 4', 'price_range': (8, 20)},
        {'title_hebrew': "בית מזוזה אלומיניום חתוך לייזר", 'title_en': 'Laser Cut Aluminum Mezuzah Case', 'price_range': (10, 30)},
        {'title_hebrew': "סידור תפילה גדול עם תרגום", 'title_en': 'Siddur Large with Translation', 'price_range': (20, 60)},
        {'title_hebrew': "פמוטי שבת נירוסטה מהודרים", 'title_en': 'Stainless Steel Shabbat Candlesticks', 'price_range': (15, 50)},
        {'title_hebrew': "גביע קידוש נירוסטה מעוצב", 'title_en': 'Decorated Stainless Kiddush Cup', 'price_range': (12, 40)},
        {'title_hebrew': "קרש חלה מעץ עם סכין", 'title_en': 'Wooden Challah Board with Knife', 'price_range': (20, 60)},
        {'title_hebrew': "שלחן שבת נפתח לשמונה מקומות", 'title_en': 'Extendable Shabbat Table 8 Seats', 'price_range': (80, 300)},
    ],
    'sports': [
        {'title_hebrew': "אוהל קמפינג 4 אנשים עמיד במים", 'title_en': 'Camping Tent 4 Person Waterproof', 'price_range': (50, 200)},
        {'title_hebrew': "שק שינה מומה לטמפרטורות נמוכות", 'title_en': 'Sleeping Bag for Low Temperatures', 'price_range': (30, 100)},
        {'title_hebrew': "תרמיל גב 50 ליטר לטיולים", 'title_en': 'Hiking Backpack 50L', 'price_range': (25, 90)},
        {'title_hebrew': "בקבוק מים נירוסטה מבודד 1 ליטר", 'title_en': 'Insulated Stainless Water Bottle 1L', 'price_range': (12, 30)},
        {'title_hebrew': "אורות LED לאופניים סט קדמי ואחורי", 'title_en': 'LED Bike Lights Front and Rear Set', 'price_range': (10, 25)},
        {'title_hebrew': "חכה לדיג מתקפלת 2.7 מטר", 'title_en': 'Fishing Rod Telescopic 2.7m', 'price_range': (20, 60)},
        {'title_hebrew': "כדורסל רשמי מקצועי מעור", 'title_en': 'Official Professional Leather Basketball', 'price_range': (15, 45)},
        {'title_hebrew': "כדורגל רשמי מקצועי מעור", 'title_en': 'Official Professional Leather Soccer Ball', 'price_range': (12, 40)},
        {'title_hebrew': "סט גומיות התנגדות 5 חוזקות", 'title_en': 'Resistance Bands Set 5 Strengths', 'price_range': (10, 30)},
        {'title_hebrew': "מזרן יוגה TPE אקולוגי 6 ממ", 'title_en': 'Yoga Mat TPE Eco-Friendly 6mm', 'price_range': (15, 40)},
        {'title_hebrew': "סט משקולות יד 1-5 קג 6 חלקים", 'title_en': 'Dumbbell Set 1-5kg 6pcs', 'price_range': (20, 60)},
        {'title_hebrew': "חבל קפיצה מתכוונן עם מוני קפיצות", 'title_en': 'Adjustable Jump Rope with Counter', 'price_range': (8, 20)},
        {'title_hebrew': "כירת שטח ניידת לקמפינג", 'title_en': 'Portable Camping Stove', 'price_range': (20, 60)},
        {'title_hebrew': "נעלי טיולים עמידות למים לגברים", 'title_en': 'Waterproof Hiking Boots for Men', 'price_range': (40, 150)},
    ],
    'car': [
        {'title_hebrew': "מחזיק טלפון לרכב לוח מחוונים", 'title_en': 'Car Phone Holder Dashboard Mount', 'price_range': (8, 25)},
        {'title_hebrew': "מטען רכב USB-C מהיר 45W", 'title_en': 'Car Charger USB-C Fast 45W', 'price_range': (12, 35)},
        {'title_hebrew': "שואב אבק לרכב חשמלי 12V", 'title_en': 'Car Vacuum Cleaner Electric 12V', 'price_range': (15, 45)},
        {'title_hebrew': "מארגן תא מטען מתכוונן", 'title_en': 'Adjustable Trunk Organizer', 'price_range': (15, 40)},
        {'title_hebrew': "כיסוי מכונית חיצוני עמיד למים", 'title_en': 'Car Cover Outdoor Waterproof', 'price_range': (25, 80)},
        {'title_hebrew': "כיסוי הגה עור אמיתי נושם", 'title_en': 'Genuine Leather Steering Wheel Cover', 'price_range': (12, 35)},
        {'title_hebrew': "ערכת ניקוי רכב מקצועית 10 חלקים", 'title_en': 'Professional Car Cleaning Kit 10pcs', 'price_range': (20, 60)},
        {'title_hebrew': "מדחס אוויר חשמלי דיגיטלי לצמיגים", 'title_en': 'Digital Electric Tire Inflator', 'price_range': (25, 70)},
        {'title_hebrew': "מצלמת דרך HD 1080P עם ראיית לילה", 'title_en': 'Dash Cam HD 1080P with Night Vision', 'price_range': (30, 100)},
        {'title_hebrew': "כיסויי מושבים לרכב סט מלא", 'title_en': 'Full Set Car Seat Covers', 'price_range': (30, 100)},
        {'title_hebrew': "מטהר אוויר לרכב פחם פעיל", 'title_en': 'Car Air Purifier with Active Carbon', 'price_range': (12, 35)},
        {'title_hebrew': "ערכת כלים לרכב 30 חלקים", 'title_en': 'Car Tool Kit 30pcs Emergency', 'price_range': (20, 60)},
    ],
    'pet': [
        {'title_hebrew': "צעצוע לכלב עמיד בלעיסה קשיח", 'title_en': 'Heavy Duty Chew Toy for Dogs', 'price_range': (8, 25)},
        {'title_hebrew': "עכבר צעצוע לחתולים אינטראקטיבי", 'title_en': 'Interactive Mouse Toy for Cats', 'price_range': (5, 15)},
        {'title_hebrew': "מיטה לכלבים גדולים מזיכרון קצף", 'title_en': 'Large Dog Bed Memory Foam', 'price_range': (25, 80)},
        {'title_hebrew': "קערת מזון נירוסטה איטית", 'title_en': 'Stainless Steel Slow Feed Bowl', 'price_range': (10, 25)},
        {'title_hebrew': "רצועה לכלב עם חזה נגד משיכה", 'title_en': 'Dog Leash with Anti-Pull Harness', 'price_range': (15, 40)},
        {'title_hebrew': "גרדן לחתולים גדול 3 קומות", 'title_en': 'Large Cat Tree 3 Levels', 'price_range': (40, 150)},
        {'title_hebrew': "מנשא לחיות מחמד עד 10 קג", 'title_en': 'Pet Carrier up to 10kg', 'price_range': (20, 60)},
        {'title_hebrew': "ערכת טיפוח לכלבים 8 חלקים", 'title_en': 'Dog Grooming Kit 8pcs', 'price_range': (15, 45)},
        {'title_hebrew': "מברשת פרווה לחיות מחמד אוטומטית", 'title_en': 'Automatic Pet Fur Brush', 'price_range': (12, 35)},
        {'title_hebrew': "חטיפי אימון לכלבים אריזת חיסכון", 'title_en': 'Dog Training Treats Value Pack', 'price_range': (10, 30)},
        {'title_hebrew': "קולר לכלב עם GPS ועמיד במים", 'title_en': 'Dog Collar with GPS Waterproof', 'price_range': (25, 70)},
    ],
    'office': [
        {'title_hebrew': "מחברת מקצועית A4 עם כריכה קשה", 'title_en': 'Professional Notebook A4 Hardcover', 'price_range': (8, 20)},
        {'title_hebrew': "סט עטים גל 12 צבעים", 'title_en': 'Gel Pen Set 12 Colors', 'price_range': (6, 18)},
        {'title_hebrew': "קלמר שולחני רב תכליתי", 'title_en': 'Multi-Functional Desk Pencil Case', 'price_range': (8, 25)},
        {'title_hebrew': "מהדק חשמלי אוטומטי 25 דף", 'title_en': 'Automatic Electric Stapler 25 Sheets', 'price_range': (15, 45)},
        {'title_hebrew': "מארגן שולחני מרובע עם מגירות", 'title_en': 'Desktop Organizer with Drawers', 'price_range': (12, 35)},
        {'title_hebrew': "תיקי תיוק קרטון עבה סט 20", 'title_en': 'Thick Cardboard File Folders 20pcs', 'price_range': (10, 30)},
        {'title_hebrew': "לוח מחיק לבן עם מחזיק קיר", 'title_en': 'Whiteboard with Wall Mount', 'price_range': (20, 60)},
        {'title_hebrew': "סט טושים מחיקים 8 צבעים", 'title_en': 'Dry Erase Markers Set 8 Colors', 'price_range': (8, 25)},
        {'title_hebrew': "מחשבון מדעי מקצועי 417 פונקציות", 'title_en': 'Professional Scientific Calculator 417 Functions', 'price_range': (12, 35)},
        {'title_hebrew': "מגש מסמכים 3 קומות מתכת", 'title_en': '3-Tier Metal Document Tray', 'price_range': (15, 40)},
        {'title_hebrew': "מפזר קלטפה שולחני כבד", 'title_en': 'Heavy Desktop Tape Dispenser', 'price_range': (8, 25)},
        {'title_hebrew': "משטח עכבר גדול מקצועי", 'title_en': 'Large Professional Mouse Pad', 'price_range': (6, 20)},
    ],
    'art': [
        {'title_hebrew': "סט צבעי אקריליק 24 צבעים 60 מל", 'title_en': 'Acrylic Paint Set 24 Colors 60ml', 'price_range': (20, 60)},
        {'title_hebrew': "סט צבעי מים 48 צבעים במחסנית", 'title_en': 'Watercolor Set 48 Colors in Tin', 'price_range': (18, 50)},
        {'title_hebrew': "בד קנבס לציור סט 6 מידות", 'title_en': 'Canvas Board Set 6 Sizes', 'price_range': (15, 45)},
        {'title_hebrew': "סט מכחולים לציור 15 חלקים", 'title_en': 'Paint Brush Set 15pcs All Types', 'price_range': (12, 35)},
        {'title_hebrew': "סקצבוק A4 100 דף נייר איכותי", 'title_en': 'Sketchbook A4 100 Sheets Quality Paper', 'price_range': (10, 30)},
        {'title_hebrew': "סט עפרונות צבעוניים 72 צבעים", 'title_en': 'Colored Pencils Set 72 Colors', 'price_range': (15, 45)},
        {'title_hebrew': "גירי שמן 50 צבעים לאומנים", 'title_en': 'Oil Pastels 50 Colors for Artists', 'price_range': (12, 35)},
        {'title_hebrew': "דבק חם מקצועי עם מקלות 20 יח", 'title_en': 'Professional Hot Glue with 20 Sticks', 'price_range': (10, 30)},
        {'title_hebrew': "מספריים מקצועיים ליצירה 3 מידות", 'title_en': 'Professional Craft Scissors 3 Sizes', 'price_range': (8, 25)},
        {'title_hebrew': "ערכת חרוזים 1000 חלקים צבעוניים", 'title_en': 'Beads Kit 1000pcs Colorful', 'price_range': (12, 35)},
        {'title_hebrew': "פלסטלינה מקצועית 24 צבעים", 'title_en': 'Professional Modeling Clay 24 Colors', 'price_range': (10, 30)},
        {'title_hebrew': "משחזת עיפרון חשמלית אוטומטית", 'title_en': 'Automatic Electric Pencil Sharpener', 'price_range': (12, 35)},
    ],
}


def generate_product_id():
    """Generate a realistic AliExpress product ID."""
    return f"100500{random.randint(100000000, 999999999)}"


def generate_sample_products():
    """Generate thousands of sample products."""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Generating Sample Products")
        print("=" * 60)
        
        total_added = 0
        
        for category_key, templates in PRODUCT_TEMPLATES.items():
            print(f"\n{'='*60}")
            print(f"Category: {Config.SAFE_CATEGORIES.get(category_key, category_key)}")
            print(f"{'='*60}")
            
            category_added = 0
            
            # Generate multiple variations of each template
            for template in templates:
                # Create 3-5 variations of each product
                num_variations = random.randint(3, 5)
                
                for i in range(num_variations):
                    try:
                        product_id = generate_product_id()
                        
                        # Check if product already exists
                        existing = Product.query.filter_by(product_id=product_id).first()
                        
                        if existing:
                            continue
                        
                        # Generate price with discount
                        base_price = random.uniform(template['price_range'][0], template['price_range'][1])
                        discount = random.choice([0, 0, 0, 10, 15, 20, 25])
                        
                        if discount > 0:
                            original_price = round(base_price / (1 - discount/100), 2)
                            sale_price = round(base_price, 2)
                        else:
                            original_price = None
                            sale_price = round(base_price, 2)
                        
                        # Generate product
                        product = Product(
                            product_id=product_id,
                            title=template['title_en'],
                            title_hebrew=template['title_hebrew'],
                            description_hebrew=f"מוצר איכותי ומקצועי. מושלם לשימוש יומיומי. עמיד לאורך זמן ומציע תמורה מעולה למחיר.",
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
                            store_name=random.choice(['Best Store', 'Quality Shop', 'Top Seller', 'Pro Deals']),
                            is_modest=True
                        )
                        
                        db.session.add(product)
                        category_added += 1
                        total_added += 1
                        
                    except Exception as e:
                        print(f"    Error adding product: {e}")
                        db.session.rollback()
                        continue
            
            db.session.commit()
            print(f"  Added {category_added} products")
        
        print(f"\n{'='*60}")
        print("GENERATION COMPLETE!")
        print(f"{'='*60}")
        print(f"Total products generated: {total_added}")
        print(f"{'='*60}")
        
        # Show breakdown by category
        print("\nProducts by category:")
        for key, name in Config.SAFE_CATEGORIES.items():
            count = Product.query.filter_by(category=key).count()
            print(f"  {name}: {count}")
        
        print(f"\nTOTAL IN DATABASE: {Product.query.count()}")


if __name__ == '__main__':
    generate_sample_products()
