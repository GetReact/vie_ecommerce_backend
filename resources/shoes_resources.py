import uuid
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
            shoes = Shoes(**json_data, id=str(uuid.uuid4().int))
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
            print('here')
            doc_encryped = db['shop_data'].find_one(
                { '_id' : os.environ['SHOES_MONGODB_DOCUMENT_ID'] }
            )

            if not doc_encryped:
                return { 'error' : 'not found in database' }, HTTPStatus.NOT_FOUND

            def create_shoes(item):
                return {
                    'id': item.get('_id'),
                    'name': item.get('name'),
                    'seller': item.get('seller'),
                    'price': item.get('price'),
                    'size': item.get('size'),
                    'condition': item.get('condition'),
                    'imageUrl': item.get('imageUrl'),
                }

            shoes_collection = list(map(
                create_shoes, 
                doc_encryped.get('items')
            ))

            return { 'message' : shoes_collection }, HTTPStatus.OK
            
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST

    def put(self):
        try:
            doc_encryped = db['shop_data'].find_one(
                { '_id' : os.environ['SHOES_MONGODB_DOCUMENT_ID'] }
            )

            if not doc_encryped:
                return { 'error' : 'not found in database' }, HTTPStatus.NOT_FOUND

            def create_shoes(item):
                return {
                    'name': item.get('name'),
                    'seller': item.get('seller'),
                    'price': item.get('price'),
                    'size': item.get('size'),
                    'condition': item.get('condition'),
                    'imageUrl': item.get('imageUrl'),
                }

            shoes_collection = list(map(
                create_shoes, 
                doc_encryped.get('items')
            ))

            for item in shoes_collection:
                shoes = Shoes(**item, id=str(uuid.uuid4().int))
                shoes.save()

            return { 'message' : 'done' }, HTTPStatus.OK
            
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST

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
                    'id': item.get('_id'),
                    'name': item.get('name'),
                    'seller': item.get('seller'),
                    'price': item.get('price'),
                    'size': item.get('size'),
                    'condition': item.get('condition'),
                    'imageUrl': item.get('imageUrl'),
                }
                
            shoes_collection = list(map(
                create_shoes, 
                doc_encryped.get('items')
            ))
        
            shoes = [item for item in shoes_collection if item['id'] == shoes_id ]

            if shoes:
                return { 'message' : shoes[0] }, HTTPStatus.OK
            else:
                return { 'error' : 'item not found' }, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST
        
