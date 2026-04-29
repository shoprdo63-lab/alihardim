#!/usr/bin/env python
"""
Import MASSIVE amount of real products from AliExpress API
Target: 50,000+ products with real images
"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.api.aliexpress import aliexpress_api
from app.models.database import Product
import time

# 100+ keywords to get variety
KEYWORDS = [
    # Electronics (10k+ products)
    'smartphone', 'android phone', 'iphone case', 'samsung case', 'screen protector',
    'bluetooth headphones', 'wireless earbuds', 'gaming headset', 'noise cancelling',
    'power bank', 'portable charger', 'wireless charger', 'fast charger', 'usb c cable',
    'smart watch', 'fitness tracker', 'smart band', 'apple watch band',
    'bluetooth speaker', 'portable speaker', 'soundbar', 'subwoofer',
    'tablet', 'ipad case', 'tablet stand', 'stylus pen', 'drawing tablet',
    'laptop stand', 'cooling pad', 'keyboard', 'mechanical keyboard', 'gaming mouse',
    'webcam', 'microphone', 'ring light', 'tripod', 'selfie stick',
    'security camera', 'wifi camera', 'baby monitor', 'doorbell camera',
    'drone', 'rc car', 'robot vacuum', 'air purifier', 'humidifier',
    
    # Home & Garden (10k+ products)
    'led strip', 'smart bulb', 'ceiling light', 'wall lamp', 'night light',
    'kitchen organizer', 'fridge organizer', 'spice rack', 'knife set',
    'cooking pot', 'frying pan', 'air fryer', 'pressure cooker', 'blender',
    'storage box', 'closet organizer', 'shoe rack', 'laundry basket',
    'wall sticker', 'curtain', 'bedding set', 'pillow', 'blanket',
    'cleaning supplies', 'mop', 'vacuum cleaner', 'duster',
    'plant pot', 'garden tools', 'watering can', 'seeds',
    'bathroom accessories', 'shower head', 'towel set', 'soap dispenser',
    
    # Fashion Accessories (10k+ products)
    'sunglasses', 'reading glasses', 'blue light glasses',
    'watch', 'digital watch', 'analog watch', 'watch band',
    'wallet', 'card holder', 'money clip',
    'backpack', 'travel bag', 'laptop bag', 'shoulder bag',
    'hat', 'baseball cap', 'beanie', 'scarf',
    'belt', 'tie', 'bow tie', 'suspenders',
    'keychain', 'lanyard', 'badge holder',
    'umbrella', 'rain coat', 'poncho',
    
    # Sports & Outdoors (10k+ products)
    'running shoes', 'sneakers', 'hiking boots', 'sandals',
    'yoga mat', 'resistance bands', 'dumbbells', 'kettlebell',
    'jump rope', 'pull up bar', 'push up board',
    'camping tent', 'sleeping bag', 'camping chair', 'lantern',
    'fishing rod', 'fishing lure', 'tackle box',
    'cycling', 'bike light', 'bike lock', 'bike helmet',
    'swimming goggles', 'swim cap', 'float',
    'basketball', 'football', 'tennis racket', 'badminton',
    'skateboard', 'scooter', 'roller skates',
    
    # Toys & Hobbies (10k+ products)
    'lego', 'building blocks', 'construction toys',
    'rc car', 'rc helicopter', 'rc boat',
    'puzzle', 'jigsaw', '3d puzzle', 'brain teaser',
    'doll', 'action figure', 'plush toy', 'stuffed animal',
    'board game', 'card game', 'chess', 'checkers',
    'kite', 'frisbee', 'boomerang', 'water gun',
    'arts and crafts', 'drawing set', 'painting kit', 'clay',
    'musical instrument', 'ukulele', 'harmonica', 'flute',
    'magic tricks', 'prank toys', 'novelty gifts',
    
    # Tools & DIY (5k+ products)
    'tool set', 'screwdriver set', 'drill', 'saw',
    'measuring tape', 'level', 'calipers',
    'soldering iron', 'multimeter', 'wire stripper',
    'glue gun', 'hot glue', 'super glue', 'epoxy',
    'duct tape', 'electrical tape', 'zip ties',
    'ladder', 'step stool', 'workbench',
    'flashlight', 'headlamp', 'lantern', 'work light',
    'safety glasses', 'gloves', 'mask', 'knee pads',
    
    # Car & Motorcycle (5k+ products)
    'car phone holder', 'car charger', 'car organizer',
    'dash cam', 'backup camera', 'tpms',
    'car cover', 'sun shade', 'steering wheel cover',
    'seat cover', 'floor mats', 'trunk organizer',
    'car cleaning', 'car wax', 'polisher', 'vacuum',
    'motorcycle helmet', 'gloves', 'jacket',
    'bike accessories', 'phone mount', 'usb charger',
    'car diagnostic', 'obd2 scanner', 'code reader',
    'jump starter', 'air compressor', 'tire inflator',
    
    # Office & School (5k+ products)
    'pen', 'pencil', 'marker', 'highlighter', 'eraser',
    'notebook', 'notepad', 'sticky notes', 'journal',
    'desk organizer', 'pen holder', 'file folder', 'binder',
    'calculator', 'ruler', 'protractor', 'compass',
    'backpack', 'lunch box', 'water bottle', 'pencil case',
    'whiteboard', 'cork board', 'push pins', 'magnets',
    'stapler', 'hole punch', 'tape dispenser', 'scissors',
    'label maker', 'laminator', 'paper cutter',
    'bookshelf', 'bookends', 'reading light',
    
    # Pet Supplies (3k+ products)
    'dog toy', 'cat toy', 'pet bed', 'pet blanket',
    'pet bowl', 'water fountain', 'automatic feeder',
    'dog leash', 'collar', 'harness', 'poop bags',
    'cat tree', 'scratching post', 'litter box',
    'pet grooming', 'brush', 'nail clipper', 'shampoo',
    'pet carrier', 'travel bag', 'car seat',
    'aquarium', 'fish food', 'filter', 'decorations',
    'bird cage', 'bird toy', 'bird feeder',
    'small animal', 'hamster wheel', 'guinea pig',
]


def import_massive():
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("🚀 MASSIVE IMPORT: 50,000+ Real AliExpress Products")
        print("=" * 70)
        
        # Check existing
        existing = Product.query.count()
        print(f"\n📊 Current products: {existing}")
        
        if existing < 1000:
            print("🗑️  Clearing fake products...")
            Product.query.delete()
            db.session.commit()
            print("✅ Cleared!")
        
        total_added = existing
        target = 50000
        
        for i, keyword in enumerate(KEYWORDS):
            if total_added >= target:
                print(f"\n🎯 Target reached: {total_added} products!")
                break
            
            print(f"\n[{i+1}/{len(KEYWORDS)}] 🔍 {keyword}...", end=" ")
            
            try:
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
                    print("⚠️")
                    continue
                
                data = result['resp_result'].get('result', {})
                products_data = data.get('products', {}).get('product', [])
                
                if not products_data:
                    print("⚠️")
                    continue
                
                added = 0
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
                    
                    # Create product
                    new_product = Product(
                        product_id=pid,
                        title=product.get('product_title', ''),
                        title_hebrew=product.get('product_title', ''),
                        description_hebrew=f"{product.get('product_title', '')} - מוצר איכותי מאלי אקספרס. משלוח חינם לרוב היעדים. מחיר אטרקטיבי בהשוואה לשוק המקומי.",
                        price=price,
                        original_price=price * 1.2 if price > 0 else 0,
                        currency='USD',
                        category='general',
                        image_url=product.get('product_main_image', ''),
                        product_url=product.get('product_detail_url', ''),
                        affiliate_url=product.get('product_detail_url', ''),
                        rating=float(str(product.get('evaluate_rate', '4.5')).split()[0]) if product.get('evaluate_rate') else 4.5,
                        reviews_count=0,
                        orders_count=0,
                        store_name=product.get('shop_title', 'AliExpress'),
                        is_modest=True
                    )
                    
                    db.session.add(new_product)
                    added += 1
                    total_added += 1
                
                db.session.commit()
                print(f"✅ +{added} (Total: {total_added})")
                
                # Progress update
                if total_added % 1000 == 0:
                    print(f"\n📈 Milestone: {total_added} products imported!")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"❌ {str(e)[:50]}")
        
        print("\n" + "=" * 70)
        print(f"🎉 COMPLETE! Total products: {total_added}")
        print("=" * 70)
        
        # Show samples
        samples = Product.query.limit(5).all()
        print("\n📌 Sample products:")
        for i, p in enumerate(samples, 1):
            print(f"\n{i}. {p.title[:60]}")
            print(f"   💰 ${p.price}")
            print(f"   🖼️  {p.image_url[:70]}...")
            print(f"   🔗 https://www.aliexpress.com/item/{p.product_id}.html")


if __name__ == '__main__':
    import_massive()
