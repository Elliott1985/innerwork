import os
import stripe
from flask import Flask, render_template
from flask_login import LoginManager
from flask_session import Session
from flask_mail import Mail
from dotenv import load_dotenv
from models import db, User
import redis

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # Database configuration
    database_url = os.getenv('DATABASE_URL', 'sqlite:///db/innerwork.db')
    # Fix Render's postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Flask-Session configuration for chatbot conversation memory
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        # Production: Use Redis for sessions
        app.config['SESSION_TYPE'] = 'redis'
        app.config['SESSION_REDIS'] = redis.from_url(redis_url)
    else:
        # Development: Use filesystem
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), 'flask_session')
    
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@innerwork.demo')
    
    # Stripe configuration
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    app.config['STRIPE_PUBLIC_KEY'] = os.getenv('STRIPE_PUBLIC_KEY')
    
    # Initialize extensions
    db.init_app(app)
    Session(app)
    Mail(app)
    
    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.modules import modules_bp
    from routes.chatbot import chatbot_bp
    from routes.payments import payments_bp
    from routes.courses import courses_bp
    from routes.lessons import lessons_bp
    from routes.dashboard import dashboard_bp
    from routes.stripe_payments import stripe_bp
    from routes.booking import booking_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(stripe_bp)
    app.register_blueprint(booking_bp)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Virtual Elliott Demo
    @app.route('/demo/elliott')
    def elliott_demo():
        return render_template('elliott_demo.html')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
