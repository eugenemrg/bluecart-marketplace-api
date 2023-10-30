from flask import make_response, jsonify
from projectapp.config import app
from projectapp.models import User
from flask_restful import Resource, Api

api = Api(app)



