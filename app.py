import os
from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db, User

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db/innerwork.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
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
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(payments_bp)
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
