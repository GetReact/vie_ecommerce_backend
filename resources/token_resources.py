import json

from flask import request, jsonify, redirect, url_for
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_raw_jwt,
    get_jwt_identity, 
    jwt_required,
    jwt_refresh_token_required
)
from http import HTTPStatus
from bson.json_util import dumps

from utils import check_password
from extensions import db


class TokenResource(Resource): # /signin
    def post(self):
        try:
            json_data = request.get_json()

            email = json_data['email']
            password = json_data['password']
            
            user = json.dumps(db['users'].find_one({ 'email' : email }))
            user_json = json.loads(user)

            if not user:
                return {
                    'error' : 'email address not found!'
                }, HTTPStatus.NOT_FOUND

            if not check_password(password, user_json['password']): 
                return {
                    'error' : 'email or password is incorrect'
                }, HTTPStatus.UNAUTHORIZED

            currentUser = {
                'id' : user_json['_id'],
                'displayName' : user_json['displayName'],
                'email' : user_json['email'],
                'is_active' : user_json['is_active']
            }
            
            return {
                'currentUser' : currentUser,
                'tokens' : {
                    'access_token' : create_access_token(identity=user_json['_id'], fresh=True),
                    'refresh_token' : create_refresh_token(identity=user_json['_id'])
                }
            }, HTTPStatus.OK

        except Exception as e:
            return {
                'error': e
            }, HTTPStatus.BAD_REQUEST

class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            return {
                'access_token' : create_access_token(identity=get_jwt_identity())
            }, HTTPStatus.OK
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST


black_list = set()
class RevokeResource(Resource): # /revoke/access
    @jwt_required
    def delete(self):
        try:
            jti = get_raw_jwt()['jti']
            black_list.add(jti)
            return {
                'status': 'Successfully revoked access token'
            }, HTTPStatus.OK
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST

class RevokeRefreshResource(Resource): # /revoke/refresh
    @jwt_refresh_token_required
    def delete(self):
        try:
            jti = get_raw_jwt()['jti']
            black_list.add(jti)
            return {
                'status': 'Successfully revoked refresh token'
            }, HTTPStatus.OK
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST
