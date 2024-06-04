from flask import Flask
from flask_cors import CORS

import api.repository.DBConnector as DB
from api.controller.ControllerAdvice import configure_controller_advice


# Configure endpoints
app = Flask(__name__)
CORS(app)


# Controller Error Handler
configure_controller_advice(app)

# Initialize database
DB.create_tables()

if __name__ == '__main__':
    app.run(debug=True)
