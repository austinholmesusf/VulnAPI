from flask import Flask
from flask_cors import CORS

import api.repository.DBConnector as DB
from api.controller.ControllerAdvice import configure_controller_advice
from api.controller.AuthController import configure_auth_routes


# Configure endpoints
app = Flask(__name__)
CORS(app)
configure_auth_routes(app)

# Controller Error Handler
configure_controller_advice(app)

# Initialize database
DB.create_tables()

if __name__ == '__main__':
    app.run(debug=True)
