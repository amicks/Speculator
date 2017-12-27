from flask_caching import Cache
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

cache = Cache(config={'CACHE_TYPE': 'simple'})
api = Api()
db = SQLAlchemy()

ENABLE_DB = True
