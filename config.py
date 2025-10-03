"""
Configuration management for SQL Scanner Dashboard
"""
import os
from typing import Optional

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    
    # Server
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5050))
    
    # Scanner defaults
    START_URL = os.environ.get('START_URL', 'http://localhost:8000')
    MAX_DEPTH = int(os.environ.get('MAX_DEPTH', 2))
    CONCURRENCY = int(os.environ.get('CONCURRENCY', 10))
    DELAY = float(os.environ.get('DELAY', 0.2))
    
    # Security
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value"""
        return os.environ.get(key, default)
    
    @staticmethod
    def is_production() -> bool:
        """Check if running in production"""
        return os.environ.get('FLASK_ENV') == 'production'
    
    @staticmethod
    def is_development() -> bool:
        """Check if running in development"""
        return os.environ.get('FLASK_ENV') != 'production'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get current configuration"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
