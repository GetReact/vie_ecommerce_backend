import os

from flask import request, g, redirect
from flask_restful import Resource
from flask_login import login_required

from http import HTTPStatus
from dotenv import load_dotenv

from extensions import db
from utils import hash_password

from models.user import User

load_dotenv()

class UserCollectionResource(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            email = json_data.get('email')
            if 'users' not in db.list_collection_names():
                db.create_collection('users')
            
            if db['users'].find_one({ 'email' : email }):
                return { 'error' : 'This Email has been registered already' }, HTTPStatus.BAD_REQUEST
        
            _ = User(**json_data).save()
        
            return redirect(os.environ['BASE_URL']+'/signin', HTTPStatus.PERMANENT_REDIRECT)
            
        except Exception as e:
            return { 'error': e }, HTTPStatus.BAD_REQUEST

class MeResource(Resource):
    @login_required
    def get(self):
        try:
            print('login_required passed!')
            user_json = db['users'].find_one({ '_id' : g.user.get_id() })

            if not user_json:
                return { 'error' : 'user not found' }, HTTPStatus.NOT_FOUND
            
            return {
                'message' : {
                    '_id' : user_json['_id'],
                    'displayName' : user_json['displayName'],
                    'email' : user_json['email'],
                    'is_active' : user_json['is_active']
                },
            }, HTTPStatus.OK
            
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST

    @login_required
    def post(self):
        try:
            if not db['users'].find_one({ '_id' : g.user.get_id() }):
                return {'error' : 'user not found'}, HTTPStatus.NOT_FOUND
            
            json_data = request.get_json()
            new_hashed_password = hash_password(json_data['newPassword'])

            db['users'].find_one_and_update(
                { '_id' : { '_id' : g.user.get_id() } },
                { '$set' : { 'password' : new_hashed_password } }
            )
            
            return redirect(os.environ['BASE_URL']+'/signout', HTTPStatus.FOUND)

        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST
