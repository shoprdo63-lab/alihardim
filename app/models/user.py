#!/usr/bin/env python
"""
User model for authentication
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

from app.models.database import db


class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Profile info
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), default='Israel')
    postal_code = db.Column(db.String(20), nullable=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Wishlist (JSON field)
    wishlist = db.Column(db.Text, default='[]')  # JSON array of product IDs
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches."""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Return full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.email.split('@')[0]
    
    def to_dict(self):
        """Convert user to dictionary (safe for JSON)."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Order(db.Model):
    """Order model for tracking user orders."""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Product info (snapshot at order time)
    product_id = db.Column(db.String(50), nullable=False)
    product_title = db.Column(db.String(255), nullable=False)
    product_image = db.Column(db.String(500), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    # Order status
    status = db.Column(db.String(50), default='pending')  # pending, paid, shipped, delivered, cancelled
    payment_method = db.Column(db.String(50), nullable=True)
    
    # Shipping info
    shipping_address = db.Column(db.String(255), nullable=True)
    shipping_city = db.Column(db.String(100), nullable=True)
    tracking_number = db.Column(db.String(100), nullable=True)
    
    # AliExpress info
    aliexpress_order_id = db.Column(db.String(100), nullable=True)
    aliexpress_tracking = db.Column(db.String(200), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'product_title': self.product_title,
            'product_image': self.product_image,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.total,
            'status': self.status,
            'tracking_number': self.tracking_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
