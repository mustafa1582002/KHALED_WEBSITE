import os
from datetime import timedelta

class Config:
    """Base configuration class - FORCED MySQL with ROOT user."""
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    
    # CORRECT: Use root user with your actual password
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GGTAHAEHt.1@localhost/color_and_craft'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'painting_service:'
    PERMANENT_SESSION_LIFETIME = 3600 * 4  # 4 hours

    # Contact Info (Updated!)
    CONTACT_EMAIL = "Colour&craft@gmail.com"
    CONTACT_PHONE = "+447592977155"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # CORRECT: Use root user for development
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GGTAHAEHt.1@localhost/color_and_craft'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    # CORRECT: Use root user for production (change in real production)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GGTAHAEHt.1@localhost/color_and_craft'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:GGTAHAEHt.1@localhost/color_and_craft'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}