from flask_login import LoginManager
from flask_cors import CORS

from pymongo import MongoClient
import stripe

import os
from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()

client = MongoClient(os.environ['MONGODB_URI'])
db = client['appdb']

cors = CORS()

stripe.api_key = os.environ['STRIPE_SECRET_KEY']