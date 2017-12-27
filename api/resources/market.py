# TODO: Only require market stats that are being used by ML models
# TODO: Allow storage/retrieval of multiple markets
from api import api, db
from flask_restful import Resource
from api.models.market import Data
from webargs import fields
from webargs.flaskparser import use_kwargs

@api.resource('/api/private/market/')
class Data(Resource):
    """ Market data of an instance in time """
    def get(self):
        return {'foo': 'bar'}

    def post(self):
        return {'foo': 'bar'}

    def put(self):
        return {'foo': 'bar'}

    def delete(self):
        return {'foo': 'bar'}
