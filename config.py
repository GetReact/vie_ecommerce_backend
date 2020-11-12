import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    RATELIMIT_HEADERS_ENABLED = True
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_RESOURCES= r'/*'
    REMEMBER_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = 'http://127.0.0.1:5000'
    CORS_ORIGINS = [
        'http://localhost:3000'
    ]
    REMEMBER_COOKIE_DURATION = timedelta(minutes=1)
    REMEMBER_COOKIE_SECURE = None
