from abc import ABC
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

class HTTP_CODES(ABC):
    """ Constants for HTTP status codes """
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422

def query_to_dict(query):
    return dict((col, getattr(query, col)) for col in query.__table__.columns.keys())

def validate_db(sqlalchemy_bind, is_enabled=True):
    """ Checks if a DB is authorized and responding before executing the function """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def is_db_responsive():
                try:
                    sqlalchemy_bind.session.query('1').first_or_404()
                except:
                    return False
                else:
                    return True
            if is_enabled and is_db_responsive():
                return func(*args, **kwargs)
            else:
                abort(HTTP_CODES.UNAUTHORIZED)
        return wrapper
    return decorator
