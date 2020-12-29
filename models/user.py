import datetime
from extensions import db

class User:
    def __init__(self, _id, displayName, email, created_at=datetime.datetime.now()):
        self.__id = _id
        self.__displayName = displayName 
        self.__email = email
        self.__created_at = created_at

    def save(self):
        return db['users'].insert_one(self.to_json()).inserted_id

    def to_json(self):
        return {
            '_id' : self.__id, 
            'displayName' : self.__displayName,
            'email' : self.__email,
            'created_at' : self.__created_at
        }