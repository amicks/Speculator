from api import api, cache, db
from api.models.market import Data
from api.helpers import query_to_dict, validate_db
from flask_restful import Resource
from speculator import market
from webargs import fields
from webargs.flaskparser import use_kwargs

@api.resource('/api/public/predict/')
class Predict(Resource):
    """ Predict the next price of a symbol like USDT_BTC """
    # TODO: Add private POST/PUT/DELETE methods

    @use_kwargs({
        'use_db': fields.Boolean(missing=False),
        'model_type': fields.Str(missing='rf'),
        'symbol': fields.Str(missing='USDT_BTC'),
        'unit': fields.Str(missing='month'),
        'count': fields.Int(missing=6),
        'period': fields.Int(missing=86400),
        'partition': fields.Int(missing=14),
        'delta': fields.Int(missing=25),
        'seed': fields.Int(missing=None),
        'trees': fields.Int(missing=10),
        'jobs': fields.Int(missing=1),
        'longs': fields.DelimitedList(fields.Str(), missing=[])
    })
    @cache.memoize(3600)
    def get(self, use_db, model_type, symbol, unit, count, period,
            partition, delta, seed, trees, jobs, longs):

        # If using db then validate db
        if use_db:
            @validate_db(db)
            def get_queries():
                return [query_to_dict(q) for q in Data.query.all()]
            json = get_queries()
        else:
            json = None

        m = market.Market(json=json, symbol=symbol, unit=unit,
                          count=count, period=period)

        features = m.set_features(partition=partition)
        features = m.set_long_features(features,
                                       columns_to_set=longs,
                                       partition=partition)

        targets = market.set_targets(features, delta=delta)
        features = features.drop(['close'], axis=1)

        model = market.setup_model(features[:-1], targets,
                                   model_type=model_type.lower(),
                                   seed=seed,
                                   n_estimators=trees,
                                   n_jobs=jobs)

        next_date = features.tail(1) # Remember the entry we didn't train?  Predict it.

        trend = market.target_code_to_name(model._predict_trends(next_date)[0])
        accuracy = model.accuracy(model.features.test, model.targets.test)
        proba = model._predict_probas(next_date)
        proba_log = model._predict_logs(next_date) # Logarithmic scale

        return {
            'trend': trend,
            'test_set_accuracy': accuracy,
            'probabilities': {
                market.target_code_to_name(code): p for code, p in enumerate(proba[0])
            }
        }
