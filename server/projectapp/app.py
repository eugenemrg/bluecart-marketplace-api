
#from flask import make_response, jsonify, request,Flask
#from projectapp.config import app
#from typing import Dict, List
#from projectapp.models import SearchHistory, User, db
#0from flask_restx import Api, Resource
#from flask_httpauth import HTTPBasicAuth
#from flask_restful import Resource, reqparse
#import datetime 
#app = Flask(__name__)
#api = Api(app)




# class GetUsers(Resource):
#     def get(self):
#         users = [user.to_dict() for user in User.query.all()]
#         resp = make_response(
#             jsonify(users),
#             200,
#         )       
#         return resp
# api.add_resource(GetUsers, '/users')

# class GetDescription(Resource):
#     def get(self):
#         with open('db.json', 'r') as json_file:
#             data = json.load(json_file)
        
#         offers = []

#         for offer_data in data["data"]:
#             price = offer_data["offer"]["price"]
#             description = offer_data['product_description']
#             rating = offer_data['product_rating']
#             product_image = offer_data['product_photos']
#             title = offer_data['product_title']
#             link = offer_data['offer']['offer_page_url']
#             offers.append({'price': price, 'description': description, 'rating': rating, 'images': product_image, 'name': title, 'links': link})

#         return jsonify({'offers': offers})

# api.add_resource(GetDescription, '/products')

    



# from flask import make_response, jsonify, request
# from projectapp.config import app
# from projectapp.models import User
# from flask_restful import Resource, Api
# # import requests
# import json
# # import time
# app = Flask(__name__)
# api = Api(app)
# auth = HTTPBasicAuth()





# class GetUsers(Resource):
#     def get(self):
#         users = [user.to_dict() for user in User.query.all()]
#         resp = make_response(
#             jsonify(users),
#             200,
#         )       
#         return resp
# api.add_resource(GetUsers, '/users')

# class GetDescription(Resource):
#     def get(self):
#         with open('db.json', 'r') as json_file:
#             data = json.load(json_file)
        
#         offers = []

#         for offer_data in data["data"]:
#             price = offer_data["offer"]["price"]
#             description = offer_data['product_description']
#             rating = offer_data['product_rating']
#             product_image = offer_data['product_photos']
#             title = offer_data['product_title']
#             link = offer_data['offer']['offer_page_url']
#             offers.append({'price': price, 'description': description, 'rating': rating, 'images': product_image, 'name': title, 'links': link})

#         return jsonify({'offers': offers})

# api.add_resource(GetDescription, '/products')
from flask_restx import Resource, Namespace,reqparse
from projectapp.models import SearchHistory, User, db
from .api_models import User_model
import datetime






ns = Namespace('api')




def get_user_data(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return {"username": user.username, "email": user.email}
    else:
        return None
    

# namespace for profiles (create, update, delete)
#profile_ns = api.namespace('profiles', description='User profile related operations')

# namespace for history
#history_ns = api.namespace('history', description='User browsing history related operations')

# namespace for log in
#login_ns = api.namespace('login', description='User login related operations')






@ns.route('/')
class Profile(Resource):
    @ns.marshal_list_with(User_model)
    def post (self, id):
        """"
         Create a new user profile
        """ 


        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        user = User.query.filter(User.email ==  args['email']).first()

        if user:
            return {'message': 'User already exists.'}, 422

        profile = User(username=args['username'], email=args['email'])
        db.session.add(profile)
        db.session.commit()

        return {'message': 'User profile created successfully.'}, 200


@ns.route('/<int:id>')
class ProfileUpdate(Resource):
    @ns.marshal_list_with(User_model)
    def put(self, id):
        """
        Update user profile
        """
        data = request.get_json()
        profile = User.query.get(id)

        if profile is None:
            return {"message": "User profile not found."}, 404

        profile.username = data['username']
        profile.email = data['email']
      

        db.session.commit()

        return {"message": "User profile updated successfully."}, 200

    def delete(self, id):
        """
        Delete a user profile
        """
        profile = User.query.get(id)

        if profile is None:
            return {"message": "User profile not found."}, 404

        db.session.delete(profile)
        db.session.commit()

        return {"message": "User profile deleted successfully."}, 200

api.add_resource(ProfileUpdate, '/profile/<int:id>')

@ns.route('/')
class Login(Resource):
    @ns.marshal_list_with(User_model)
    def post(self, id):
        """
        Login user, send back JWT token
        """
        user = User.find_by_id(id)
        if not user:
            return {"message": "User not found"}, 404

        password = request.json.get('password')
        if not user.check_password(password):
            return {"message": "Invalid password"}, 400

        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = user.generate_auth_token(exp).decode('utf-8')

        return {"token": token, "expiration": exp}, 200
    
@ns.route('/')
class HistoryList(Resource):
    @ns.marshal_list_with(SearchHistory_model)
    def get(self):
        """
        Get entire user search history
        """
        # get the user_id from the token
        user_id = User.get_user_id_from_token(request)

        # retrieve the user's search history from the database
        history = User.get_history(user_id)

        # return the search history as a response
        return jsonify(history), 200
    
        

    def post(self):
        """
        Add search query to history
        """
        # get the user_id from the token
        user_id = User.get_user_id_from_token(request)

        # get the search query from the request data
        query = request.json.get('query')

        # add the search query to the user's search history in the database
        User.add_to_history(user_id, query)

        # return a success message as a response
        return {"message": "Search query added to history"}, 201
       

@ns.route('/<id>')
class History(Resource):
    @ns.marshal_list_with(User_model)
    def delete(self, id):
        """
        Delete search item from history by id
        """
        history_item = SearchHistory.query.get(id)

        
        if not history_item:
            return {}, 204
        
        db.session.delete(history_item)
        db.session.commit()
        return {}, 204


# api = Api(app)
# api.add_resource(Profile, '/profiles/<int:id>')
api.add_resource(HistoryList, '/history')
api.add_resource(History, '/history/<id>')
api.add_resource(Login, '/login')
api.add_resource(Profile, '/profile')
api.add_resource(ProfileUpdate, '/profile/<id>')

