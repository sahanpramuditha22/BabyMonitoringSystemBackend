"""
Flask application factory and setup
"""
from flask import Flask
from routes import register_routes


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Register routes
    register_routes(app)
    
    return app
