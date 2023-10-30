from flask import make_response, jsonify
from projectapp.config import app
from projectapp.models import User
from flask_restful import Resource, Api

api = Api(app)

class GetUsers(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        resp = make_response(
            jsonify(users),
            200,
        )       
        return resp
api.add_resource(GetUsers, '/users')

