# TODO: Only require market stats that are being used by ML models
# TODO: Allow storage/retrieval of multiple markets
""" Allows storage/retrieval for custom market data instead of automatic gathering """
from api import api, db
from api.helpers import HTTP_CODES, query_to_dict, validate_db
from api.models.market import Data as DataModel
from flask import abort
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs

data_kwargs = {
    'id': fields.Integer(required=True),
    'low': fields.Float(missing=None),
    'high': fields.Float(missing=None),
    'close': fields.Float(missing=None),
    'volume': fields.Float(missing=None)
}

@api.resource('/api/private/market/')
class Data(Resource):
    """ Market data at an instance in time """
    @use_kwargs({'id': fields.Integer(missing=None)})
    @validate_db(db)
    def get(self, id):
        if id is None:
            return [query_to_dict(q) for q in DataModel.query.all()]
        else:
            return query_to_dict(DataModel.query.get_or_404(id))

    @use_kwargs(data_kwargs)
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

    @use_kwargs(data_kwargs)
    @validate_db(db)
    def put(self, id, low, high, close, volume):
        """ Loop through function args, only change what is specified
        NOTE: Arg values of -1 clears since each must be >= 0 to be valid
        """
        query = DataModel.query.get_or_404(id)
        for arg, value in locals().items():
            if arg is not 'id' and arg is not 'self' and value is not None:
                if value == -1:
                    setattr(query, arg, None)
                else:
                    setattr(query, arg, value)
        db.session.commit()
        return query_to_dict(query)

    @use_kwargs({'id': fields.Integer(missing=None)})
    @validate_db(db)
    def delete(self, id):
        try:
            if id is None:
                DataModel.query.delete()
                db.session.commit()
            else:
                db.session.delete(DataModel.query.get_or_404(id))
                db.session.commit()
        except:
            return {'status': 'failed'}
        else:
            return {'status': 'successful'}
