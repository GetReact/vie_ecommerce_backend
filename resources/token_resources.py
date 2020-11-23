import os

from flask_restful import Resource
from flask import request, redirect, make_response
from flask_login import login_user, logout_user, login_required

from http import HTTPStatus
from dotenv import load_dotenv

from utils import check_password
from extensions import db

from models.user import User

load_dotenv()

class TokenResource(Resource): # /signin
    def post(self):
        json_data = request.get_json()
        email = json_data.get('email')
        password = json_data.get('password')
        
        user_json = db['users'].find_one({ 'email' : email })

        if not user_json or not check_password(password, user_json['password']): 
            return { 'error' : 'email or password is incorrect' }, HTTPStatus.UNAUTHORIZED

        user = User(**user_json)        # {k:v for k,v in user_json.items() if k not in ['']}
        login_user(user)

        return {
            'message' : {
                '_id' : user_json['_id'],
                'displayName' : user_json['displayName'],
                'email' : user_json['email'],
                'is_active' : user_json['is_active']
            },
        }, HTTPStatus.OK

class RevokeResource(Resource): # /signout
    @login_required
    def post(self):
        try:
            logout_user()
            return { 'message' : 'Successfully logged out' }, HTTPStatus.OK
        except Exception as e:
            return { 'error': e }, HTTPStatus.BAD_REQUEST
