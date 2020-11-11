import json

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus
import uuid

from extensions import db
from utils import hash_password

class UserCollectionResource(Resource):
    def post(self): # register user
        try:
            json_data = request.get_json()
            email = json_data.get('email')
            display_name = json_data.get('displayName')
            password = hash_password(json_data.get('password'))

            if 'users' not in db.list_collection_names():
                db.create_collection('users')
            
            if db['users'].find_one({ 'email' : email }):
                return {'message' : 'This Email has been registered already'}, HTTPStatus.BAD_REQUEST
        
            new_user_id = db['users'].insert_one({
                '_id' : uuid.uuid4().hex, 
                'displayName' : display_name,
                'email' : email,
                'password' : password,
                'is_active' : True
            }).inserted_id
        
            return {
                'id' : new_user_id,
                'status' : 'Successfully registered'
            }, HTTPStatus.OK
            
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST

class MeResource(Resource):
    @jwt_required
    def get(self):
        try:
            # print(get_jwt_identity())

            user = db['users'].find_one({ '_id' : get_jwt_identity() })
            user_json = json.dumps(user)
            
            if not user_json:
                return {'error' : 'user not found'}, HTTPStatus.NOT_FOUND

            # print(json.loads(user_json))

            return {
                'currentUser' : {
                    'id' : json.loads(user_json)['_id'],
                    'displayName' : json.loads(user_json)['displayName'],
                    'email' : json.loads(user_json)['email'],
                    'is_active' : json.loads(user_json)['is_active']
                },
                'status' : 'verified'
            }, HTTPStatus.OK
            
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST

    @jwt_required
    def patch(self):
        try:
            if not db['users'].find_one({ '_id' : get_jwt_identity() }):
                return {'error' : 'user not found'}, HTTPStatus.NOT_FOUND
            
            json_data = request.get_json()
            new_hashed_password = hash_password(json_data['newPassword'])

            db['users'].find_one_and_update(
                { '_id' : get_jwt_identity() },
                {
                    '$set' : { 'password' : new_hashed_password }
                }
            )
            
            return {
                'status' : 'Profile successfully updated'
            }, HTTPStatus.OK

        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST
