from flask import Flask
from flask_restx import Api
from api.student import api as students
from db.db import init_db
from flask_cors import CORS
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env file
load_dotenv()
print(environ.get("FRONTEND_URL"))

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [environ.get("FRONTEND_URL")],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    },
)


init_db(app)

# Initialize Flask-RESTx API and register the students namespace
api = Api(app)
api.add_namespace(students)  # Add the students namespace to the API

if __name__ == "__main__":
    app.run(debug=True, port=environ.get("BACKEND_PORT"), host="0.0.0.0")
