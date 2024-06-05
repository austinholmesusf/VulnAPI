from flask import request, jsonify, Flask
import api.service.AuthService as AuthService


def configure_auth_routes(app: Flask):
    @app.route('/')
    def index():
        return 'VulnAPI'

    @app.route('/login', methods=['POST'])
    def handle_login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        return jsonify({'token': AuthService.login(username, password)})

    @app.route('/signup', methods=['POST'])
    def handle_signup():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        return jsonify({'token': AuthService.signup(username, password, first_name, last_name)}), 201
