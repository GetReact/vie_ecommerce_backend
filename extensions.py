from flask_session import Session
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from pymongo import MongoClient
import stripe

import os
from dotenv import load_dotenv

load_dotenv()

# login_manager = LoginManager()
jwt = JWTManager()

sess = Session()

client = MongoClient(os.environ['MONGODB_URI'])
db = client['appdb']

cors = CORS()

stripe.api_key = os.environ['STRIPE_SECRET_KEY']