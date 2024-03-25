from flask import Flask, render_template
from flask_cors import CORS
from .routes import main as main_blueprint

def create_app():
    app = Flask(__name__, template_folder='../../frontend/templates')
    app.register_blueprint(main_blueprint)
    
    CORS(app)

    return app