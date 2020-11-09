import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    RATELIMIT_HEADERS_ENABLED = True
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    CORS_ORIGINS = [
        'http://localhost:3000',
    ]
    CORS_RESOURCES = r"/*"

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    JWT_SECRET_KEY = os.urandom(24)
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=10)