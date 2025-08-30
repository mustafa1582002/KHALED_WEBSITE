from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # CORRECT MySQL configuration with your actual credentials
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:GGTAHAEHt.1@localhost/color_and_craft'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=4)
    
    # Contact Info
    app.config['CONTACT_EMAIL'] = "Colour&craft@gmail.com"
    app.config['CONTACT_PHONE'] = "+447592977155"
    
    # Debug: Print database URI to verify
    print(f"🔧 MySQL Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    print("✅ App created with CORRECT MySQL configuration")
    
    return app