from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()
        
        # Seed products if database is empty (for Vercel)
        from app.models.database import Product
        if Product.query.count() == 0:
            print("Database empty - seeding products...")
            from app.utils.seed_products import seed_products
            seed_products()
    
    return app
