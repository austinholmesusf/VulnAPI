from functools import wraps

from flask import request

from api.entity.AuthJWT import AuthJWT
from api.exception.AuthException import AuthException


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_json = None
        if 'token' in request.headers:
            token_json = request.headers['token']
        if not token_json:
            raise AuthException('Authentication token missing.')
        token = AuthJWT().decode(token_json)
        if token is None:
            raise AuthException('Authentication failed.')
        return f(token, *args, **kwargs)
    return decorated
