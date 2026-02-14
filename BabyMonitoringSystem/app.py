"""
Flask application factory and setup
"""
from flask import Flask
from flask_cors import CORS
from routes import register_routes


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5004",  # Flutter web
    "http://localhost:51977/",  # (if you still need this)
    "http://127.0.0.1:5004",   # (optional, for 127.0.0.1)
]}})
    
    # Register routes
    register_routes(app)
    
    return app
