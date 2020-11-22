from flask import Flask, g
from flask_restful import Api
from flask_login import current_user

import os
from dotenv import load_dotenv

from config import Config, DevelopmentConfig, ProductionConfig
from extensions import login_manager, cors

from resources.token_resources import TokenResource, RevokeResource
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
    
    print(app.config['CORS_ORIGINS'])

    register_extensions(app)
    register_resources(app)

    @app.route("/")
    def index():
        return {"message" : "this is the home page!"}

    @app.before_request
    def before_request():
        g.user = current_user
    
    return app

def register_extensions(app):
    cors.init_app(app)
    login_manager.init_app(app)

def register_resources(app):
    api = Api(app)

    api.add_resource(TokenResource, '/signin')
    api.add_resource(RevokeResource, '/signout')

    api.add_resource(UserCollectionResource, '/users')
    api.add_resource(MeResource, '/me')
    
    api.add_resource(ShoesCollectionResource, '/shoes')
    api.add_resource(ShoesResource, '/shoes/<string:shoes_id>')

    api.add_resource(StripeResource, '/payment')

if __name__ == "__main__": # sudo lsof -i:5000
    app = create_app()
    app.run(debug = True)