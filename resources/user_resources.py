import json

from flask import request, g
from flask_restful import Resource
from flask_login import login_required, current_user

from http import HTTPStatus

from extensions import db

from models.user import User

class UserCollectionResource(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            email = json_data.get('email')
            if 'users' not in db.list_collection_names():
                db.create_collection('users')
            
            if db['users'].find_one({ 'email' : email }):
                return {'message' : 'This Email has been registered already'}, HTTPStatus.BAD_REQUEST
        
            user_id = User(**json_data).save()
        
            return {
                'id' : user_id,
                'status' : 'Successfully registered'
            }, HTTPStatus.OK
            
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST

class MeResource(Resource):
    @login_required
    def get(self):
        try:
            user = db['users'].find_one({ '_id' : g.user.get_id() })
            user_json = json.dumps(user)
            
            if not user_json:
                return {'error' : 'user not found'}, HTTPStatus.NOT_FOUND

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

#     @jwt_required
#     def patch(self):
#         try:
#             if not db['users'].find_one({ '_id' : get_jwt_identity() }):
#                 return {'error' : 'user not found'}, HTTPStatus.NOT_FOUND
            
#             json_data = request.get_json()
#             new_hashed_password = hash_password(json_data['newPassword'])

#             db['users'].find_one_and_update(
#                 { '_id' : get_jwt_identity() },
#                 {
#                     '$set' : { 'password' : new_hashed_password }
#                 }
#             )
            
#             return {
#                 'status' : 'Profile successfully updated'
#             }, HTTPStatus.OK

#         except Exception as e:
#             return {'error': e}, HTTPStatus.BAD_REQUEST
