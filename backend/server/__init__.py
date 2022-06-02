from flask import (
    Flask
)
from flask_cors import CORS, cross_origin
from models import setup_db

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    
    return app