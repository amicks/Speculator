from api import api
from flask_restful import Resource

@api.resource('/api/private/db/market_list')
class MarketList(Resource):
    """ List[List] of Market Json Items

    Allows the modification/storage of multiple market JSON data sets.

    Args:
        id: Sub-list ID of MarketJsonItems to access

    Structure:
        [
          [MarketJson11, MarketJson12, ..., MarketJson1N],
          [MarketJson21, MarketJson22, ..., MarketJson2N],
          ...,
          [MarketJsonM1, MarketJsonM2, ..., MarketJsonMN]
        ]

    """
    def get(self):
        return {"foo": "bar"}

    def delete(self):
        return {"foo": "bar"}

@api.resource('/api/private/db/market_list/item')
class MarketJsonItem(Resource):
    """ Contains raw market data for one instance """
    def get(self):
        return {"foo": "bar"}

    def post(self):
        return {"foo": "bar"}

    def put(self):
        return {"foo": "bar"}

    def delete(self):
        return {"foo": "bar"}
