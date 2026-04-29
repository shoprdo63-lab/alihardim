import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-coded-secret-key'
    # Use /tmp for Vercel (read-only file system), local file otherwise
    if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/ali_store.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ali_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AliExpress API
    ALI_APP_KEY = os.environ.get('ALI_APP_KEY')
    ALI_APP_SECRET = os.environ.get('ALI_APP_SECRET')
    ALI_TRACKING_ID = os.environ.get('ALI_TRACKING_ID')
    
    # Supabase Configuration (User Authentication)
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or 'https://otymgaukfdhugnygnxbr.supabase.co'
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90eW1nYXVrZmRodWdueWdueGJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0NjA5MjQsImV4cCI6MjA5MzAzNjkyNH0.g8OPxI-9rG_GCdCyRwLt3IGcQ1HPUSK0KLipGMUUN_E'
    
    # App Settings
    PRODUCTS_PER_PAGE = 24
    MAX_PRODUCTS_TO_SYNC = 5000
    
    # Categories (modest categories only)
    SAFE_CATEGORIES = {
        'electronic': 'גאדג\'טים ואלקטרוניקה',
        'toys': 'צעצועים לילדים',
        'home_garden': 'בית וגן',
        'tools': 'כלי עבודה וDIY',
        'jewish': 'אביזרי יהדות',
        'sports': 'ספורט וקמפינג',
        'car': 'רכב ואביזרים',
        'pet': 'חיות מחמד',
        'office': 'כלי כתיבה ומשרד',
        'art': 'אמנות ויצירה'
    }
