from flask import request
from http import HTTPStatus
from functools import wraps
from dotenv import load_dotenv
from firebase_admin import auth

# import os
# import time
# import requests
# from jose import jwt

from extensions import db

load_dotenv()

def register_required(view):
    @wraps(view)
    def wrap(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')
        if not jwt_token: return { 'error' : 'session token not found' }, HTTPStatus.NOT_FOUND

        try:
            payload = auth.verify_id_token(jwt_token)
        except Exception as e:
            return { 'error': e }, HTTPStatus.BAD_REQUEST

        user = auth.get_user(payload['user_id'])

        new_user = {
            '_id': user.uid,
            'email': user.email,
            'displayName': user.display_name
        }

        request.new_user = new_user
        return view(*args, **kwargs)
    return wrap

def login_required(view):
    @wraps(view)
    def wrap(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')
        if not jwt_token: return { 'error' : 'session token not found' }, HTTPStatus.NOT_FOUND

        try:
            payload = auth.verify_id_token(jwt_token)
        except Exception as e:
            return { 'error': e }, HTTPStatus.BAD_REQUEST

        print(payload)

        user = db['users'].find_one({ '_id' : payload['user_id'] })

        if user:
            request.user = user
            return view(*args, **kwargs)
        else: return { 'error' : 'user not found' }, HTTPStatus.NOT_FOUND
    return wrap

# def token_validated(payload):
#     expected_iss = f"https://securetoken.google.com/{os.environ['FIREBASE_PROJECT_ID']}"

#     if payload['exp'] < time.time():
#         print('expired')
#         return False
    
#     if payload['aud'] != os.environ['FIREBASE_PROJECT_ID']:
#         print('aud')
#         return False

#     if payload['iss'] != expected_iss:
#         print('iss')
#         return False

#     return True
    
# def decode_token(jwt_token):
#     # print(jwt_token)
#     certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'    
#     jwks = requests.get(certificate_url)
    
#     key=jwks.content
#     issuer = f"https://securetoken.google.com/{os.environ['FIREBASE_PROJECT_ID']}"
#     audience = os.environ['FIREBASE_PROJECT_ID']

#     payload = jwt.decode(
#         token=jwt_token,
#         key=key,
#         algorithms=['RS256'],
#         audience=audience,
#         issuer=issuer,
#         options={'verify_at_hash': False}
#     )
#     return payload