from flask import request
from flask_restful import Resource

from http import HTTPStatus
from dotenv import load_dotenv

from auth_decorators import register_required, login_required
from models.user import User

load_dotenv()

class UserCollectionResource(Resource):
    @register_required
    def post(self):
        try:
            new_user = request.new_user
        
            user = User(**new_user)
            _ = user.save()
                
            return { 'user' : {
                **user.to_json(),
                'created_at': str(user.to_json()['created_at'])
            } }, HTTPStatus.OK
        except Exception as e:
            return { 'error': e }, HTTPStatus.BAD_REQUEST

class MeResource(Resource):
    @login_required
    def get(self):
        try:
            user = request.user
            return { 'user' : {
                **user.to_json(),
                'created_at': str(user.to_json()['created_at'])
            } }, HTTPStatus.OK
        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST
