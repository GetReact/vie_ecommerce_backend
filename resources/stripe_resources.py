from flask import request
from flask_restful import Resource
from flask_login import login_required

from http import HTTPStatus

from extensions import stripe

class StripeResource(Resource): # /payment
    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            print(json_data['token']['id'])
            response = stripe.Charge.create(
                amount=json_data['amount'],
                currency='usd',
                source=json_data['token']['id']
            )

            return {
                'status' : response['status'],
                'response' : response
            }, HTTPStatus.ACCEPTED

        except Exception as e:
            return {'error': e}, HTTPStatus.BAD_REQUEST