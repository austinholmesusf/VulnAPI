from flask import jsonify, Flask

from api.annotation.TokenRequired import token_required
from api.service import UserService


def configure_user_routes(app: Flask):
    @app.route('/get_user_data', methods=['POST'])
    @token_required
    def handle_get_user_data(token):
        user_id = token.user_id
        user_data = UserService.get_user(user_id)
        users_serial = vars(user_data)
        return jsonify({'user': users_serial})

