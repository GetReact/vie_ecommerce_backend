import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_RESOURCES = r'/*'
    BASE_URL = os.environ['BASE_URL']
    CORS_ORIGINS = [
        os.environ['FRONTEND_URL'],
        'http://localhost:3000',
    ]
    REMEMBER_COOKIE_NAME = 'remember-me-token'

class DevelopmentConfig(Config):
    DEBUG = True
    RATELIMIT_HEADERS_ENABLED = False
    REMEMBER_COOKIE_DURATION = timedelta(minutes=1)
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True

class ProductionConfig(Config):
    DEBUG = False
    RATELIMIT_HEADERS_ENABLED = True
    REMEMBER_COOKIE_DURATION = timedelta(minutes=15)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True