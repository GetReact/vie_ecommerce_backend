from flask import Flask
from flask_restful import Api

import os
from dotenv import load_dotenv

from config import DevelopmentConfig
from extensions import sess, jwt, cors

from resources.token_resources import (
    TokenResource,
    RefreshToken,
    RevokeResource,
    RevokeRefreshResource,
    black_list
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
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list

def register_resources(app):
    api = Api(app)

    api.add_resource(TokenResource, '/signin')
    api.add_resource(RefreshToken, '/refresh')
    api.add_resource(RevokeResource, '/revoke/access')
    api.add_resource(RevokeRefreshResource, '/revoke/refresh')

    api.add_resource(UserCollectionResource, '/users')
    api.add_resource(UserResource, '/users/<string:user_id>')
    
    api.add_resource(ShoesCollectionResource, '/shoes')
    api.add_resource(ShoesResource, '/shoes/<string:shoes_id>')

    api.add_resource(StripeResource, '/payment')

if __name__ == "__main__": # sudo lsof -i:5000
    app = create_app()
    app.run(debug = True)