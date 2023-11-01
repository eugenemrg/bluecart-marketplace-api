from flask import make_response, jsonify, request
from projectapp.config import app
from projectapp.models import User
from flask_restful import Resource, Api
# import requests
import json
# import time
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

class GetDescription(Resource):
    def get(self):
        with open('db.json', 'r') as json_file:
            data = json.load(json_file)
        
        offers = []

        for offer_data in data["data"]:
            price = offer_data["offer"]["price"]
            description = offer_data['product_description']
            rating = offer_data['product_rating']
            product_image = offer_data['product_photos']
            title = offer_data['product_title']
            link = offer_data['offer']['offer_page_url']
            offers.append({'price': price, 'description': description, 'rating': rating, 'images': product_image, 'name': title, 'links': link})

        return jsonify({'offers': offers})

api.add_resource(GetDescription, '/products')

    



