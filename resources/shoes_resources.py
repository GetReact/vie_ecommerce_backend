import json
import os
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource
from flask_login import login_required

from http import HTTPStatus

from extensions import db

from models.shoes import Shoes

load_dotenv()

class ShoesCollectionResource(Resource): # /shoes
    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            shoes = Shoes(**json_data)
            document_id = shoes.save()
            return {
                'shoesCollection' : {
                    'id' : document_id,
                    'title' : 'shoes',
                    'new_item' : {
                        **shoes.to_json(),
                        'created_at': str(shoes.to_json().get('created_at')),
                    },
                },
            }, HTTPStatus.OK
        
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST
        
    def get(self):
        try:
            json_data = request.get_json()
            doc_encryped = json.dumps(db['shop_data'].find_one(
                { '_id' : json_data[os.environ['SHOES_MONGODB_DOCUMENT_ID']] }
            ))

            if not doc_encryped:
                return { 'error' : 'not found in database' }, HTTPStatus.NOT_FOUND

            shoes_collection_doc_json = json.loads(doc_encryped)
            return { 'message' : shoes_collection_doc_json }, HTTPStatus.OK
            
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST

class ShoesResource(Resource):
    def get(self, shoes_id):
        try:
            json_data = request.get_json()
            doc_encryped = json.dumps(db['shop_data'].find_one(
                { '_id' : json_data[os.environ['SHOES_MONGODB_DOCUMENT_ID']] }
            ))

            if not doc_encryped:
                return { 'error' : 'not found in database' }, HTTPStatus.NOT_FOUND

            shoes_collection_doc_json = json.loads(doc_encryped)
            items = shoes_collection_doc_json['items']
        
            shoes = [item for item in items if item['_id'] == shoes_id ]

            if shoes:
                return { 'message' : shoes }, HTTPStatus.OK
            else:
                return { 'error' : 'item not found' }, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST
        
