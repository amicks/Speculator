# TODO: Add private API with Redis Cache and PostgreSQL (or any SQL DB with SQLAlchemy)
from api import api, cache, db
from flask import abort, Flask
from flask_restful import Resource
from os import getenv
from resources.json import JsonItem, JsonList
from resources.test import Test
from resources.trend import Predict

def setup_app():
    db_uri = getenv('SQLALCHEMY_DATABASE_URI') # format: postgresql://user:pw@host:port/db
    if not db_uri:
        abort(401)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = setup_app()
    app.run(debug=True)
