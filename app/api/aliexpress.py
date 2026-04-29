"""
AliExpress API Integration
"""

from typing import List, Dict, Optional
from config import Config
from app.services.content_filter import is_modest_product, translate_to_hebrew, generate_hebrew_description

import requests
import hashlib
import time
import urllib.parse


class AliExpressAPI:
    def __init__(self):
        self.app_key = Config.ALI_APP_KEY
        self.app_secret = Config.ALI_APP_SECRET
        self.tracking_id = Config.ALI_TRACKING_ID
        self.base_url = "https://api-sg.aliexpress.com/sync"
        
    def _generate_sign(self, params: Dict) -> str:
        """Generate API signature for AliExpress API v1."""
        # Sort parameters by key
        sorted_params = sorted(params.items())
        
        # Concatenate key-value pairs
        sign_str = self.app_secret
        for key, value in sorted_params:
            sign_str += key + str(value)
        sign_str += self.app_secret
        
        # MD5 hash
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    
    def _make_request(self, method: str, params: Dict) -> Dict:
        """Make a request to AliExpress API."""
        # Add common parameters
        params.update({
            'app_key': self.app_key,
            'timestamp': str(int(time.time() * 1000)),
            'sign_method': 'md5',
            'format': 'json',
            'v': '2.0',
            'partner_id': 'top-sdk-python-20230701',
        })
        
        # Generate signature
        params['sign'] = self._generate_sign(params)
        
        # Make request
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return {}
    
    def search_products(self, 
                        keywords: str, 
                        category_id: Optional[str] = None,
                        page_no: int = 1, 
                        page_size: int = 20,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None) -> List[Dict]:
        """Search for products by keywords."""
        params = {
            'method': 'aliexpress.affiliate.product.query',
            'keywords': keywords,
            'page_no': page_no,
            'page_size': min(page_size, 50),  # Max 50
            'target_currency': 'USD',
            'target_language': 'EN',
            'tracking_id': self.tracking_id,
            'fields': 'product_id,product_title,product_main_image,sale_price,target_sale_price,product_detail_url,evaluate_rate,shop_title,discount',
        }
        
        if category_id:
            params['category_ids'] = category_id
        
        if min_price:
            params['min_sale_price'] = int(min_price * 100)  # In cents
        if max_price:
            params['max_sale_price'] = int(max_price * 100)
        
        result = self._make_request('GET', params)
        
        products = []
        if result and 'resp_result' in result:
            data = result['resp_result'].get('result', {})
            products_data = data.get('products', {}).get('product', [])
            
            for product in products_data:
                title = product.get('product_title', '')
                
                # Filter non-modest products
                if not is_modest_product(title):
                    continue
                
                # Get prices
                sale_price = product.get('target_sale_price', product.get('sale_price', '0'))
                original_price = product.get('original_price', sale_price)
                
                # Clean price strings
                try:
                    sale_price_val = float(str(sale_price).replace('$', '').replace(',', ''))
                    original_price_val = float(str(original_price).replace('$', '').replace(',', '')) if original_price else sale_price_val
                except:
                    sale_price_val = 0.0
                    original_price_val = 0.0
                
                # Generate affiliate link
                product_url = product.get('product_detail_url', '')
                affiliate_url = self.generate_affiliate_link(product_url) if product_url else ''
                
                # Translate to Hebrew
                hebrew_title, _ = translate_to_hebrew(title)
                hebrew_desc = generate_hebrew_description({'title': title, 'category': category_id or 'general'})
                
                products.append({
                    'product_id': product.get('product_id', ''),
                    'title': title,
                    'title_hebrew': hebrew_title,
                    'description_hebrew': hebrew_desc,
                    'price': sale_price_val,
                    'original_price': original_price_val,
                    'image_url': product.get('product_main_image', ''),
                    'product_url': product_url,
                    'affiliate_url': affiliate_url,
                    'rating': product.get('evaluate_rate', ''),
                    'store_name': product.get('shop_title', ''),
                    'discount': product.get('discount', '0%'),
                })
        
        return products
    
    def generate_affiliate_link(self, product_url: str) -> str:
        """Generate an affiliate link for a product."""
        params = {
            'method': 'aliexpress.affiliate.link.generate',
            'promotion_link_type': '0',  # Product link
            'source_values': product_url,
            'tracking_id': self.tracking_id,
        }
        
        result = self._make_request('GET', params)
        
        if result and 'resp_result' in result:
            links_data = result['resp_result'].get('result', {}).get('promotion_links', {}).get('promotion_link', [])
            if links_data:
                return links_data[0].get('promotion_link', product_url)
        
        return product_url
    
    def get_hot_products(self, category_id: Optional[str] = None, page_size: int = 20) -> List[Dict]:
        """Get hot/trending products."""
        params = {
            'method': 'aliexpress.affiliate.hotproduct.query',
            'page_size': min(page_size, 50),
            'target_currency': 'USD',
            'target_language': 'EN',
            'tracking_id': self.tracking_id,
        }
        
        if category_id:
            params['category_id'] = category_id
        
        result = self._make_request('GET', params)
        
        products = []
        if result and 'resp_result' in result:
            data = result['resp_result'].get('result', {})
            products_data = data.get('products', {}).get('product', [])
            
            for product in products_data:
                title = product.get('product_title', '')
                
                # Filter non-modest products
                if not is_modest_product(title):
                    continue
                
                sale_price = product.get('sale_price', '0')
                try:
                    sale_price_val = float(str(sale_price).replace('$', '').replace(',', ''))
                except:
                    sale_price_val = 0.0
                
                hebrew_title, _ = translate_to_hebrew(title)
                hebrew_desc = generate_hebrew_description({'title': title, 'category': category_id or 'general'})
                
                products.append({
                    'product_id': product.get('product_id', ''),
                    'title': title,
                    'title_hebrew': hebrew_title,
                    'description_hebrew': hebrew_desc,
                    'price': sale_price_val,
                    'original_price': sale_price_val * 1.2,  # Estimate
                    'image_url': product.get('product_main_image', ''),
                    'product_url': product.get('product_detail_url', ''),
                    'rating': product.get('evaluate_rate', ''),
                    'store_name': product.get('shop_title', ''),
                })
        
        return products
    
    def get_categories(self) -> List[Dict]:
        """Get product categories."""
        # AliExpress doesn't have a direct category API
        # We'll use our predefined categories with IDs
        categories = [
            {'id': '3', 'name': 'Electronics', 'hebrew': 'גאדג\'טים ואלקטרוניקה'},
            {'id': '26', 'name': 'Toys & Hobbies', 'hebrew': 'צעצועים לילדים'},
            {'id': '15', 'name': 'Home & Garden', 'hebrew': 'בית וגן'},
            {'id': '1420', 'name': 'Tools', 'hebrew': 'כלי עבודה וDIY'},
            {'id': '18', 'name': 'Sports & Entertainment', 'hebrew': 'ספורט וקמפינג'},
            {'id': '34', 'name': 'Automobiles & Motorcycles', 'hebrew': 'רכב ואביזרים'},
            {'id': '66', 'name': 'Home Improvement', 'hebrew': 'שיפוץ הבית'},
        ]
        return categories


# Global API instance
aliexpress_api = AliExpressAPI()
