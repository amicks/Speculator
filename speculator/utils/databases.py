from flask import abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

def validate_db(sqlalchemy_bind):
    """ Checks if a DB is authorized and responding before executing the function """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def is_db_responsive():
                try:
                    sqlalchemy_bind.session.query("1").first_or_404()
                except:
                    return False
                else:
                    return True
            if is_db_responsive():
                return func(*args, **kwargs)
            else:
                abort(401)
        return wrapper
    return decorator
