from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    title_hebrew = db.Column(db.String(500))
    description = db.Column(db.Text)
    description_hebrew = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    category = db.Column(db.String(50), nullable=False, index=True)
    subcategory = db.Column(db.String(100))
    image_url = db.Column(db.String(500))
    product_url = db.Column(db.String(500))
    affiliate_url = db.Column(db.String(500))
    rating = db.Column(db.Float)
    reviews_count = db.Column(db.Integer)
    orders_count = db.Column(db.Integer)
    store_name = db.Column(db.String(200))
    shipping_price = db.Column(db.Float)
    is_modest = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.title[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title_hebrew or self.title,
            'description': self.description_hebrew or self.description,
            'price': self.price,
            'original_price': self.original_price,
            'currency': self.currency,
            'category': self.category,
            'image_url': self.image_url,
            'product_url': self.affiliate_url or self.product_url,
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'orders_count': self.orders_count,
            'store_name': self.store_name,
            'discount': round(((self.original_price or self.price) - self.price) / (self.original_price or self.price) * 100, 0) if self.original_price else 0
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    name_hebrew = db.Column(db.String(100), nullable=False)
    name_english = db.Column(db.String(100))
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    product_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Category {self.name_hebrew}>'

class SearchQuery(db.Model):
    __tablename__ = 'search_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))
    results_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
