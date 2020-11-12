import json
import datetime
import uuid

from utils import hash_password
from extensions import db, login_manager

class User:
    def __init__(
        self, displayName, email, password, 
        id=uuid.uuid4().hex, is_active=True, 
        created_at=datetime.datetime.now()):

        self.__id = id
        self.__displayName = displayName 
        self.__email = email
        self.__password = hash_password(password)
        self.__is_active = is_active
        self.__created_at = created_at

    def save(self):
        return db['users'].insert_one(self.to_json()).inserted_id

    def to_json(self):
        return {
            '_id' : self.__id, 
            'displayName' : self.__displayName,
            'email' : self.__email,
            'password' : self.__password,
            'is_active' : self.__is_active,
            'created_at' : self.__created_at
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.__is_active == True

    def get_id(self):
        return self.__id

    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    user_json = db['users'].find_one({ '_id' : user_id })
    return User(**user_json)