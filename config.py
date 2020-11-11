import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    RATELIMIT_HEADERS_ENABLED = True
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_CSRF_IN_COOKIES = True
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_COOKIE_PATH = [
        '/signout',
        '/users/<string:user_id>',
        '/payment'
    ]
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    CORS_RESOURCES = r"/*"

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = 'http://localhost:5000'
    CORS_ORIGINS = [
        'http://localhost:3000',
    ]
    JWT_COOKIE_SECURE = False
    JWT_SECRET_KEY = os.urandom(24)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=10)