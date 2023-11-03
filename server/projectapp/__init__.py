from flask import make_response, jsonify, request,Flask
from .extensions import api, db
from .app import ns


def creaate_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)


    return app    
