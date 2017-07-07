from flask_login import current_user
from .models import Permission
from functools import wrape
from flask import abort 


def permission_required(permission):
    def decorator(f):
        @wraps(f):
        def decorated_func(*args,**kwargs):
            if not current_user.can(permission):
               abort(403)
            return f(*args,**kwargs)
        return decorated_func 
