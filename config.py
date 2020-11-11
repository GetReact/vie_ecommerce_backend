import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    RATELIMIT_HEADERS_ENABLED = True
    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_SESSION_COOKIE = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
    JWT_ACCESS_COOKIE_PATH = [
        '/signout',
        '/me',
        '/payment',
        '/refresh'
    ]
    JWT_REFRESH_COOKIE_PATH = ['/refresh']
    JWT_CSRF_CHECK_FORM = True
    JWT_CSRF_IN_COOKIES = True
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_RESOURCES = r'/api/*'
    # CORS_EXPOSE_HEADERS = [
    #     'Set-Cookie'
    # ]

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = 'http://127.0.0.1:5000'
    CORS_ORIGINS = [
        'http://localhost:3000'
    ]
    JWT_COOKIE_SECURE = False
    JWT_SECRET_KEY = os.urandom(24)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=1)