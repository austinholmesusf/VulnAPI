from flask import jsonify
from werkzeug.exceptions import BadRequest

from api.exception import EndpointException


def configure_controller_advice(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        code = 503
        if isinstance(error, EndpointException.EndpointException):
            code = error.http_code
        elif isinstance(error, BadRequest) or isinstance(error, ValueError):
            code = 400

        response = {
            'error': {
                'code': code,
                'description': str(error)
            }
        }

        return jsonify(response), code
