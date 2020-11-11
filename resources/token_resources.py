import json
from datetime import timedelta

from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    set_access_cookies, 
    set_refresh_cookies, 
    unset_jwt_cookies,
    unset_access_cookies,
    jwt_refresh_token_required,
    verify_jwt_refresh_token_in_request,
    jwt_required,
    get_jwt_identity
)

from http import HTTPStatus

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

            access_token = create_access_token(identity=user_json['_id'], fresh=True, expires_delta=timedelta(seconds=10))
            refresh_token = create_refresh_token(identity=user_json['_id'], expires_delta=timedelta(seconds=1*60))
            
            resp = make_response(
                {
                    'currentUser' : currentUser,
                }, HTTPStatus.OK    
            )
            
            set_access_cookies(response=resp, encoded_access_token=access_token)
            set_refresh_cookies(response=resp, encoded_refresh_token=refresh_token)

            return resp

        except Exception as e:
            return {
                'error': e
            }, HTTPStatus.BAD_REQUEST

class RevokeResource(Resource): # /signout
    @jwt_required
    def post(self):
        try:
            resp = make_response(
                {
                    'status': 'Successfully revoked access token'
                }, HTTPStatus.OK
            )
            unset_jwt_cookies(resp)
            return resp
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST

class RefreshToken(Resource):
    @jwt_refresh_token_required
    def get(self):
        try:
            print(request.headers)
            print(get_jwt_identity())
            access_token = create_access_token(identity=get_jwt_identity(), fresh=False, expires_delta=timedelta(seconds=10))
            resp = make_response({
                'new_access_token': access_token
            }, HTTPStatus.OK)
            set_access_cookies(response=resp, encoded_access_token=access_token)
            return resp
        except Exception as e:
            print(e)
            # return {'error': e}, HTTPStatus.BAD_REQUEST
