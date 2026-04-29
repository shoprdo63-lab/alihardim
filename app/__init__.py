from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'אנא התחבר כדי לגשת לדף זה'
    login_manager.login_message_category = 'info'
    
    from app.routes import main
    app.register_blueprint(main)
    
    # Register auth blueprint (Supabase)
    from app.routes_auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Add context processor for current_user (from Supabase session)
    @app.context_processor
    def inject_user():
        from flask import session
        user = session.get('user')
        # Create a mock user object for templates
        class CurrentUser:
            def __init__(self, user_data):
                self.id = user_data.get('id') if user_data else None
                self.email = user_data.get('email') if user_data else None
                self.first_name = user_data.get('first_name') if user_data else None
                self.last_name = user_data.get('last_name') if user_data else None
                self.is_authenticated = user_data is not None
            
            def get_full_name(self):
                if self.first_name and self.last_name:
                    return f"{self.first_name} {self.last_name}"
                return self.first_name or self.email or 'אורח'
        
        return dict(current_user=CurrentUser(user))
    
    with app.app_context():
        db.create_all()
        
        # Seed products if database is empty (for Vercel)
        from app.models.database import Product
        if Product.query.count() == 0:
            print("Database empty - seeding products...")
            from app.utils.seed_products import seed_products
            seed_products()
    
    return app


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    from app.models.user import User
    return User.query.get(int(user_id))
