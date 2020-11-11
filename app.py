from http import HTTPStatus
from flask import Flask, redirect, make_response
from flask_restful import Api
from flask_jwt_extended import (
    unset_access_cookies,
    unset_jwt_cookies
)

import os
from dotenv import load_dotenv

from config import DevelopmentConfig
from extensions import sess, jwt, cors

from resources.token_resources import (
    TokenResource,
    RefreshToken,
    RevokeResource
)
from resources.user_resources import (
    UserCollectionResource,
    UserResource
)
from resources.shoes_resources import (
    ShoesCollectionResource,
    ShoesResource
)
from resources.stripe_resources import StripeResource

load_dotenv()

def create_app():
    app = Flask(__name__)

    if os.environ['env'] == 'dev':
        app.config.from_object(DevelopmentConfig)
    
    register_extensions(app)
    register_resources(app)

    @app.route("/")
    def index():
        return {"message" : "this is the home page!"}

    return app

def register_extensions(app):
    cors.init_app(app)

    sess.init_app(app)

    jwt.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        # No auth header
        resp = make_response(redirect(app.config['BASE_URL'] + '/signin', HTTPStatus.FOUND))
        return resp

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        # Invalid Fresh/Non-Fresh Access token in auth header
        resp = make_response(redirect(app.config['BASE_URL'] + '/signin', HTTPStatus.FOUND))
        unset_jwt_cookies(resp)
        return resp

    @jwt.expired_token_loader
    def expired_token_callback(callback):
        # Expired auth header
        resp = make_response(redirect(app.config['BASE_URL'] + '/token/refresh', HTTPStatus.FOUND))
        unset_access_cookies(resp)
        return resp

def register_resources(app):
    api = Api(app)

    api.add_resource(TokenResource, '/signin')
    api.add_resource(RefreshToken, '/token/refresh')
    api.add_resource(RevokeResource, '/signout')

    api.add_resource(UserCollectionResource, '/users')
    api.add_resource(UserResource, '/users/<string:user_id>')
    
    api.add_resource(ShoesCollectionResource, '/shoes')
    api.add_resource(ShoesResource, '/shoes/<string:shoes_id>')

    api.add_resource(StripeResource, '/payment')

if __name__ == "__main__": # sudo lsof -i:5000
    app = create_app()
    app.run(debug = True)