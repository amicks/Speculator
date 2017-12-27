# TODO: Only require market stats that are being used by ML models
# TODO: Allow storage/retrieval of multiple markets
from api import api, db
from api.helpers import HTTP_CODES, query_to_dict, validate_db
from api.models.market import Data as DataModel
from flask import abort
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

@api.resource('/api/private/market/')
class Data(Resource):
    """ Market data at an instance in time """
    @use_kwargs({
        'id': fields.Integer(required=True)
    })
    @validate_db(db)
    def get(self, id):
        return query_to_dict(DataModel.query.get_or_404(id))

    @use_kwargs({
        'id': fields.Integer(required=True),
        'low': fields.Float(missing=None),
        'high': fields.Float(missing=None),
        'close': fields.Float(missing=None),
        'volume': fields.Float(missing=None)
    })
    @validate_db(db)
    def post(self, id, low, high, close, volume):
        try:
            post_request = DataModel(id, low, high, close, volume)
            db.session.add(post_request)
            db.session.commit()
        except: # ID already exists, use PUT
            abort(HTTP_CODES.UNPROCESSABLE_ENTITY)
        else:
            return query_to_dict(post_request)

    def put(self):
        return {'foo': 'bar'}

    def delete(self):
        return {'foo': 'bar'}
