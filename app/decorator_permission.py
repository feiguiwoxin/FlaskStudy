from functools import wraps
from flask_login import current_user
from flask import abort
from app.models import Permission

def permission_required(permission):
    def func(f):
        @wraps(f)
        def permission_func(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return permission_func
    return func

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)