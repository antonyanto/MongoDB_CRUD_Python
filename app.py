from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from flask_pymongo import pymongo
from crud_app_routes.routes import crud_app_api


def create_crud_app():
    crud_app = Flask(__name__)
    CORS(crud_app)

    api_blueprint = Blueprint('crud_api_blueprint', __name__)
    api_blueprint = crud_app_api(api_blueprint)
    crud_app.register_blueprint(api_blueprint, url_prefix='/api')

    return crud_app


app = create_crud_app()

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
