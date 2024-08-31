from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ss@9035933616@sS'  # Replace with your own secure key


    # Register blueprints
    app.register_blueprint(main)

    return app
