from flask_session import Session
from flask_jwt_extended import JWTManager

from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

# login_manager = LoginManager()
jwt = JWTManager()

sess = Session()

client = MongoClient(os.environ['MONGODB_URI'])
db = client['appdb']