from flask_cors import CORS

import os
import json
from dotenv import load_dotenv

from pymongo import MongoClient
import stripe
import firebase_admin
from firebase_admin import credentials

load_dotenv()

client = MongoClient(os.environ['MONGODB_URI'])
db = client['appdb']

cors = CORS()

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

cred = credentials.Certificate(json.loads(os.environ['FIREBASE_CONFIG']))
firebase_admin.initialize_app(cred)