from flask import Flask
from flask_restful import Api

import os
from dotenv import load_dotenv

from config import Config, DevelopmentConfig, ProductionConfig
from extensions import cors

from resources.user_resources import UserCollectionResource, MeResource
from resources.shoes_resources import ShoesCollectionResource, ShoesResource
from resources.stripe_resources import StripeResource

load_dotenv()

def create_app():
    app = Flask(__name__)

    if os.environ['ENV'] == 'dev':
        app.config.from_object(DevelopmentConfig)
    elif os.environ['ENV'] == 'prod':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)
    
    register_extensions(app)
    register_resources(app)
    
    return app

def register_extensions(app):
    cors.init_app(app)

def register_resources(app):
    api = Api(app)

    api.add_resource(UserCollectionResource, '/users')
    api.add_resource(MeResource, '/me')
    
    api.add_resource(ShoesCollectionResource, '/shoes')
    api.add_resource(ShoesResource, '/shoes/<string:shoes_id>')

    api.add_resource(StripeResource, '/payment')

if __name__ == "__main__": # sudo lsof -i:5000
    app = create_app()
    app.run(debug = True)