import datetime
import uuid
import os

from dotenv import load_dotenv
from extensions import db

load_dotenv()

class Shoes:
    def __init__(
        self, name, seller, price, size, condition, 
        imageUrl, id=str(uuid.uuid4().int), 
        created_at=datetime.datetime.now()):
        
        self.__id = id
        self.__name = name
        self.__seller = seller
        self.__price = price
        self.__size = size
        self.__condition = condition
        self.__imageUrl = imageUrl
        self.__created_at = created_at

    def save(self):
        db['shop_data'].update_one(
            { '_id' : os.environ['SHOES_MONGODB_DOCUMENT_ID'] },
            { '$push' : { 'items' : self.to_json() } }
        )
        return os.environ['SHOES_MONGODB_DOCUMENT_ID']

    def to_json(self):
        return {
            '_id' : self.__id, 
            'name' : self.__name,
            'seller' : self.__seller,
            'price' : self.__price,
            'size' : self.__size,
            'condition' : self.__condition,
            'imageUrl' : self.__imageUrl,
            'created_at' : self.__created_at
        }
