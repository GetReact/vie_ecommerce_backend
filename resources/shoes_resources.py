from flask import request
from flask_restful import Resource

import uuid
import os
from dotenv import load_dotenv
from http import HTTPStatus

from extensions import db
from models.shoes import Shoes
from auth_decorators import login_required

load_dotenv()

class ShoesCollectionResource(Resource): # /shoes
    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            shoes = Shoes(**json_data, id=str(uuid.uuid4().int))
            _ = shoes.save()
            shoes_json = shoes.to_json()
            return {
                'shoes' : {
                    'id': shoes_json['_id'],
                    'name': shoes_json['name'],
                    'seller': shoes_json['seller'],
                    'price': shoes_json['price'],
                    'size': shoes_json['size'],
                    'condition': shoes_json['condition'],
                    'imageUrl': shoes_json['imageUrl'],
                },
            }, HTTPStatus.OK
        
        except Exception as e:
            return { 'error' : e }, HTTPStatus.BAD_REQUEST
        
    def get(self):
        try:            
            doc_encryped = db['shop_data'].find_one(
                { '_id' : os.environ['SHOES_MONGODB_DOCUMENT_ID'] }
            )
            if not doc_encryped:
                return { 'error' : 'not found in database' }, HTTPStatus.NOT_FOUND

            def create_shoes(item):
                return {
                    'id': item['_id'],
                    'name': item['name'],
                    'seller': item['seller'],
                    'price': item['price'],
                    'size': item['size'],
                    'condition': item['condition'],
                    'imageUrl': item['imageUrl'],
                }

            shoes_collection = list(map(
                create_shoes, 
                doc_encryped['items']
            ))

            return { 'collection' : shoes_collection }, HTTPStatus.OK
            
        except Exception as e:
            return { 'error' : e }, HTTPStatus.BAD_REQUEST

class ShoesResource(Resource):
    def get(self, shoes_id):
        try:
            doc_encryped = db['shop_data'].find_one(
                { '_id' : os.environ['SHOES_MONGODB_DOCUMENT_ID'] }
            )
            if not doc_encryped:
                return { 'error' : 'not found in database' }, HTTPStatus.NOT_FOUND

            def create_shoes(item):
                return {
                    'id': item['_id'],
                    'name': item['name'],
                    'seller': item['seller'],
                    'price': item['price'],
                    'size': item['size'],
                    'condition': item['condition'],
                    'imageUrl': item['imageUrl'],
                }
                
            shoes_collection = list(map(
                create_shoes, 
                doc_encryped['items']
            ))
        
            shoes = [item for item in shoes_collection if item['id'] == shoes_id]

            if shoes:
                return { 'shoes' : shoes[0] }, HTTPStatus.OK
            else:
                return { 'error' : 'item not found' }, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST
        
