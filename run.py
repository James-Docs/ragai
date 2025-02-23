from flask import Flask
from app.api.routes import api
from app.config import UPLOAD_FOLDER
import logging

def create_app():
    app = Flask(__name__, 
                static_folder='app/static',
                template_folder='app/templates'
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.register_blueprint(api)  # No url_prefix needed now
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(debug=True) 