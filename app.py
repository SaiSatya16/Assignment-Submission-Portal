from flask import Flask
from flask_restful import Api

import os
import logging
from logging.handlers import RotatingFileHandler
from extensions import mongo, bcrypt, jwt
from config import DevelopmentConfig
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Load environment variables


# Configure logging
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

def create_app():
    app = Flask(__name__)
    app.logger.addHandler(handler)
    app.config.from_object(DevelopmentConfig)


    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import resources
    from resources.user import UserRegister, UserLogin, UploadAssignment, AdminList
    from resources.admin import AdminRegister, AdminLogin, AssignmentList, AcceptAssignment, RejectAssignment

    api = Api(app)

    # Add resources to API
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UploadAssignment, '/upload')
    api.add_resource(AdminList, '/admins')

    api.add_resource(AdminRegister, '/admin/register')
    api.add_resource(AdminLogin, '/admin/login')
    api.add_resource(AssignmentList, '/assignments')
    api.add_resource(AcceptAssignment, '/assignments/<string:id>/accept')
    api.add_resource(RejectAssignment, '/assignments/<string:id>/reject')

    return app

app = create_app()
CORS(app)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/openapi.json' 
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)

@app.route("/")
def home():
    try:
        # Try to fetch the server info to check the connection
        server_info = mongo.db.client.server_info()
        return f"Connected successfully to MongoDB Atlas! Server version: {server_info.get('version', 'unknown')}"
    except Exception as e:
        return f"Failed to connect to MongoDB Atlas. Error: {str(e)}"



if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')