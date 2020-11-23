import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    SESSION_COOKIE_HTTPONLY = True
    BASE_URL = os.environ['BASE_URL']
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_RESOURCES = r'/*'
    CORS_ORIGINS = [
        os.environ['FRONTEND_URL'],
        os.environ['FRONTEND_URL_DEV']
    ]
    CORS_EXPOSE_HEADERS = [
        'Set-Cookie'
    ]

class DevelopmentConfig(Config):
    DEBUG = True
    RATELIMIT_HEADERS_ENABLED = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    RATELIMIT_HEADERS_ENABLED = True
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True