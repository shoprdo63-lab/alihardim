"""
Content filter for modesty (צניעות) compliance.
Filters out products and categories that are not appropriate for the religious audience.
"""

# Hebrew and English words to filter out
NON_MODEST_KEYWORDS = {
    # Women's clothing
    'woman', 'women', 'female', 'lady', 'ladies', 'dress', 'dresses', 'skirt', 'skirts',
    'בגדים', 'שמלה', 'שמלות', 'חצאית', 'נשים', 'אישה', 'בגדי נשים', 'בגד נשים',
    'lingerie', 'bra', 'bras', 'panties', 'underwear', 'bikini', 'swimsuit', 'swimwear',
    'חזייה', 'תחתונים', 'ביקיני', 'בגד ים', 'בגדי ים', 'הלבשה תחתונה',
    
    # Makeup and cosmetics
    'makeup', 'cosmetics', 'lipstick', 'mascara', 'eyeshadow', 'foundation',
    'איפור', 'משחת שפה', 'מסקרה', 'צללית', 'קרם בסיס',
    
    # Jewelry and accessories for women specifically
    'earrings', 'necklace', 'bracelet', 'ring', 'jewelry',
    'עגילים', 'שרשרת', 'צמיד', 'טבעת', 'תכשיטים',
    
    # Other sensitive items
    'wig', 'wigs', 'hair extension', 'perücke',
    'פאה', 'פאות', 'תוספות שיער',
    
    # Adult content
    'adult', 'sexy', 'sexy lingerie', 'nightgown', 'nightwear',
    'מבוגרים', 'סקסי', 'כותונת לילה',
}

# Categories to completely skip
BLOCKED_CATEGORIES = {
    'women', 'women\'s', 'womens', 'ladies', 'female',
    'clothing-women', 'women-clothing', 'women-dresses',
    'lingerie', 'intimates', 'swimwear', 'bikinis',
    'makeup', 'beauty-personal-care',
    'wigs-hair-extensions',
    'women-shoes', 'women-bags',
}

# Safe search terms for product fetching
SAFE_SEARCH_KEYWORDS = [
    # Electronics
    'smartphone', 'tablet', 'laptop', 'headphones', 'charger', 'cable', 'case',
    'mouse', 'keyboard', 'usb', 'power bank', 'bluetooth', 'wireless',
    'גאדג\'ט', 'טלפון', 'אוזניות', 'מטען', 'כבל', 'מחשב', 'אלחוטי',
    
    # Toys
    'toy', 'lego', 'building blocks', 'educational toy', 'puzzle', 'dollhouse',
    'remote control car', 'toy car', 'stuffed animal', 'action figure',
    'צעצוע', 'לגו', 'קוביות', 'חינוכי', 'פאזל', 'בית בובות', 'מכונית שלט',
    
    # Home & Garden
    'kitchen', 'cooking', 'storage', 'organizer', 'garden', 'tools', 'light',
    'lamp', 'led', 'decor', 'furniture', 'home improvement',
    'מטבח', 'בישול', 'איחסון', 'גינה', 'תאורה', 'מנורה', 'ריהוט',
    
    # Tools & DIY
    'drill', 'screwdriver', 'tool set', 'electric tool', 'saw', 'hammer',
    'כלי עבודה', 'מברגה', 'מקדחה', 'פטיש', 'מסור',
    
    # Jewish items
    'kippah', 'tzitzit', 'tallit', 'hanukkah', 'dreidel', 'mezuzah', 'siddur',
    'jewish', 'judaica', 'torah', 'menorah',
    'כיפה', 'ציצית', 'טלית', 'חנוכיה', 'סביבון', 'מזוזה', 'סידור', 'יהדות',
    
    # Sports & Outdoor
    'camping', 'hiking', 'tent', 'backpack', 'sports equipment', 'ball',
    'fitness', 'exercise', 'bicycle', 'fishing',
    'קמפינג', 'טיולים', 'אוהל', 'תרמיל', 'ספורט', 'כדור', 'אופניים', 'דיג',
    
    # Car
    'car accessories', 'car tool', 'cleaner', 'car organizer',
    'אביזרי רכב', 'ניקוי רכב', 'מכונית',
    
    # Pets
    'dog', 'cat', 'pet', 'pet toy', 'pet food', 'leash', 'collar',
    'כלב', 'חתול', 'חיית מחמד', 'משחק לכלב', 'מזון כלבים', 'רצועה',
    
    # Office
    'pen', 'pencil', 'notebook', 'stapler', 'desk organizer', 'marker',
    'עט', 'עיפרון', 'מחברת', 'שולחן עבודה', 'מדבקה',
    
    # Art
    'paint', 'canvas', 'brush', 'drawing', 'art supplies', 'craft',
    'צבע', 'בד', 'מכחול', 'ציור', 'אומנות', 'יצירה',
]


def is_modest_product(title: str, description: str = '', category: str = '') -> bool:
    """
    Check if a product is modest based on its title, description, and category.
    Returns True if the product is modest/safe to display.
    """
    text_to_check = f"{title} {description} {category}".lower()
    
    # Check against blocked keywords
    for keyword in NON_MODEST_KEYWORDS:
        if keyword.lower() in text_to_check:
            return False
    
    # Check against blocked categories
    for blocked_cat in BLOCKED_CATEGORIES:
        if blocked_cat.lower() in category.lower():
            return False
    
    return True


def get_safe_search_keywords():
    """Return list of safe search keywords for product fetching."""
    return SAFE_SEARCH_KEYWORDS


def translate_to_hebrew(title: str, description: str = '') -> tuple:
    """
    Translate product title and description to Hebrew.
    Returns (hebrew_title, hebrew_description)
    """
    # Translation dictionary for common terms
    translations = {
        # Electronics
        'smartphone': 'טלפון חכם',
        'tablet': 'טאבלט',
        'laptop': 'מחשב נייד',
        'headphones': 'אוזניות',
        'wireless': 'אלחוטי',
        'bluetooth': 'בלוטות\'',
        'charger': 'מטען',
        'cable': 'כבל',
        'usb': 'USB',
        'case': 'נרתיק',
        'cover': 'מגן',
        'screen protector': 'מגן מסך',
        'power bank': 'מטען נייד',
        'battery': 'סוללה',
        'adapter': 'מתאם',
        'memory': 'זיכרון',
        'storage': 'איחסון',
        'camera': 'מצלמה',
        'lens': 'עדשה',
        'tripod': 'חצובה',
        'selfie stick': 'מקל סלפי',
        'smart watch': 'שעון חכם',
        'fitness tracker': 'צמיד כושר',
        
        # Quality descriptors
        'original': 'מקורי',
        'new': 'חדש',
        'pro': 'מקצועי',
        'premium': 'פרימיום',
        'high quality': 'איכותי',
        'best seller': 'רב מכר',
        'hot sale': 'מבצע חם',
        'discount': 'הנחה',
        'free shipping': 'משלוח חינם',
        'waterproof': 'עמיד במים',
        'durable': 'עמיד',
        'portable': 'נייד',
        'compact': 'קומפקטי',
        'mini': 'מיני',
        'professional': 'מקצועי',
        'universal': 'אוניברסלי',
        'compatible': 'תואם',
        'multifunction': 'רב תכליתי',
        'adjustable': 'מתכוונן',
        'foldable': 'ניתן לקיפול',
        'rechargeable': 'ניתן לטעינה',
        'wireless charging': 'טעינה אלחוטית',
        'fast charging': 'טעינה מהירה',
        'long battery life': 'חיי סוללה ארוכים',
        'easy to use': 'קל לשימוש',
        'lightweight': 'קל משקל',
        'heavy duty': 'כבד וחזק',
        'anti-slip': 'מונע החלקה',
        'shockproof': 'עמיד בזעזועים',
        'dustproof': 'עמיד באבק',
        
        # Home
        'kitchen': 'מטבח',
        'bathroom': 'אמבטיה',
        'bedroom': 'חדר שינה',
        'living room': 'סלון',
        'home': 'בית',
        'garden': 'גינה',
        'office': 'משרד',
        'storage': 'איחסון',
        'organizer': 'מארגן',
        'container': 'מיכל',
        'box': 'קופסה',
        'basket': 'סל',
        'shelf': 'מדף',
        'rack': 'מתקן תלייה',
        'hook': 'וו',
        'hanger': 'קולב',
        'mirror': 'מראה',
        'clock': 'שעון',
        'lamp': 'מנורה',
        'light': 'תאורה',
        'led': 'LED',
        'bulb': 'נורה',
        'curtain': 'וילון',
        'carpet': 'שטיח',
        'mat': 'שטיחון',
        'pillow': 'כרית',
        'blanket': 'שמיכה',
        'towel': 'מגבת',
        'table': 'שולחן',
        'chair': 'כיסא',
        'furniture': 'ריהוט',
        'decoration': 'קישוט',
        'wall sticker': 'מדבקת קיר',
        'frame': 'מסגרת',
        'vase': 'אגרטל',
        
        # Colors
        'black': 'שחור',
        'white': 'לבן',
        'red': 'אדום',
        'blue': 'כחול',
        'green': 'ירוק',
        'yellow': 'צהוב',
        'orange': 'כתום',
        'purple': 'סגול',
        'pink': 'ורוד',
        'brown': 'חום',
        'gray': 'אפור',
        'silver': 'כסף',
        'gold': 'זהב',
        'transparent': 'שקוף',
        'multicolor': 'צבעוני',
        
        # Sizes
        'small': 'קטן',
        'medium': 'בינוני',
        'large': 'גדול',
        'xl': 'XL',
        'xxl': 'XXL',
        'size': 'מידה',
        'cm': 'ס"מ',
        'mm': 'מ"מ',
        'inch': 'אינץ',
    }
    
    hebrew_title = title
    hebrew_description = description
    
    # Apply translations
    for en, he in translations.items():
        hebrew_title = hebrew_title.replace(en, he)
        hebrew_description = hebrew_description.replace(en, he)
    
    return hebrew_title, hebrew_description


def generate_hebrew_description(product_data: dict) -> str:
    """Generate a quality Hebrew description for a product."""
    title = product_data.get('title', '')
    category = product_data.get('category', '')
    
    # Base description template
    templates = {
        'electronics': "מוצר אלקטרוני איכותי המושלם לשימוש יומיומי. עמיד, נוח ואמין. מומלץ לכל בית!",
        'toys': "צעצוע מהנה וחינוכי לילדים. מפתח דמיון ויצירתיות. בטוח לשימוש ועמיד לאורך זמן.",
        'home': "מוצר ביתי שימושי שישדרג את הבית שלכם. איכותי, נוח וקל לתחזוקה. ערך מעולה למחיר!",
        'tools': "כלי עבודה מקצועי לאנשי מקצוע וחובבים כאחד. חזק, עמיד ומדויק. כל בעל בית צריך אחד!",
        'jewish': "מוצר יהודי אותנטי לאירוח ולשמחה. איכות גבוהה ומראה יפה. מתנה מושלמת לכל אירוע!",
        'sports': "ציוד ספורט וטיולים באיכות גבוהה. עמיד, נוח ומקצועי. למגוון רחב של פעילויות חוץ!",
        'car': "אביזר רכב שימושי שיהפוך את הנסיעות שלכם לנוחות יותר. איכותי ועמיד לאורך שנים!",
        'pet': "מוצר לחיות מחמד שכל בעל כלב או חתול צריך. איכותי, בטוח ונוח לשימוש!",
        'office': "מוצר משרדי שימושי שיעזור לארגן את העבודה שלכם. איכותי ועמיד לשימוש יומיומי!",
        'art': "חומרי יצירה איכותיים לאמנים וחובבים. מושלם לפרויקטים יצירתיים בבית או בבית הספר!",
    }
    
    # Find matching template
    for key, template in templates.items():
        if key in category.lower():
            return template
    
    # Default description
    return "מוצר איכותי במחיר מעולה! מושלם לשימוש בבית, בעבודה או כמתנה. עמיד, נוח ואמין. הזמינו עכשיו ותיהנו ממשלוח מהיר!"
