import json

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

import uuid
from http import HTTPStatus

from extensions import db

class ShoesCollectionResource(Resource): # /shoes
    @jwt_required
    def post(self):
        try:
            json_data = request.get_json()
            shoes_collection_doc_id = json_data['shoesCollectionID'] 

            if 'shop_data' not in db.list_collection_names():
                db.create_collection('shop_data')
                shoes_collection_doc_id = db['shop_data'].insert_one(
                    {
                        '_id' : uuid.uuid4().hex, 
                        'title' : 'shoes',
                        'items' : []
                    }
                ).inserted_id
            
            print(shoes_collection_doc_id)
            new_item_id = str(uuid.uuid4().int)

            shoes_collection_doc = db['shop_data'].update_one(
                { '_id' : shoes_collection_doc_id },
                {
                    '$push' : {
                        'items' : {
                            '_id' : new_item_id, 
                            'name' : json_data['name'],
                            'seller' : json_data['seller'],
                            'price' : json_data['price'],
                            'size' : json_data['size'],
                            'condition' : json_data['condition'],
                            'imageUrl' : json_data['imageUrl']
                        }
                    }
                }
            )

            return {
                'shoesCollection' : {
                    'id' : shoes_collection_doc_id,
                    'title' : 'shoes',
                    'new_item' : {
                        'id' : new_item_id, 
                        'name' : json_data['name'],
                        'seller' : json_data['seller'],
                        'price' : json_data['price'],
                        'size' : json_data['size'],
                        'condition' : json_data['condition'],
                        'imageUrl' : json_data['imageUrl']
                    },
                },
                'status' : 'successfully added item'
            }, HTTPStatus.OK
        
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST
        
    def get(self):
        try:
            json_data = request.get_json()
            
            doc_encryped = json.dumps(db['shop_data'].find_one(
                { '_id' : json_data['shoesCollectionID'] }
            ))

            if not doc_encryped:
                return {
                    'error' : 'not found in database'
                }, HTTPStatus.NOT_FOUND

            shoes_collection_doc_json = json.loads(doc_encryped)

            return {
                'shoesCollection' : shoes_collection_doc_json
            }, HTTPStatus.OK
            
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST

class ShoesResource(Resource):
    def get(self, shoes_id):
        try:
            json_data = request.get_json()
                
            doc_encryped = json.dumps(db['shop_data'].find_one(
                { '_id' : json_data['shoesCollectionID'] }
            ))

            if not doc_encryped:
                return {
                    'error' : 'not found in database'
                }, HTTPStatus.NOT_FOUND

            shoes_collection_doc_json = json.loads(doc_encryped)

            items = shoes_collection_doc_json['items']
        
            shoes = [item for item in items if item['_id'] == shoes_id ]

            if shoes:
                return {
                    'item' : shoes
                }, HTTPStatus.OK
            else:
                return {
                    'error' : 'item not found'
                }, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error' : e}, HTTPStatus.BAD_REQUEST
        
