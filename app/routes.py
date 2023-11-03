
from flask_restx import Resource, Namespace,reqparse
from .api_models import user_profile_model, user_history_model
from .models import SearchHistory, User
from .extensions import db,api
import requests
import datetime

profile_ns = Namespace('profile', description='Create, update or delete user profile')
login_ns = Namespace('login', description='Handle user log in')
history_ns = Namespace('history', description='Get, update or delete user history')


def get_user_data(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return {"username": user.username, "email": user.email}
    else:
        return None
    

# namespace for profiles (create, update, delete)
#profile_ns = api.namespace('profiles', description='User profile related operations')

#namespace for history
#
# history_ns = api.namespace('history', description='User browsing history related operations')

# namespace for log in
#login_ns = api.namespace('login', description='User login related operations')






@profile_ns.route('/')
class Profile(Resource):
     @profile_ns.marshal_list_with(user_profile_model)
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


@login_ns.route('/<int:id>')
class ProfileUpdate(Resource):
    def put(self, id):
        """
        Update user profile
        """
        data = requests.get_json()
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

@login_ns.route('/')
class Login(Resource):
   # @history_ns.marshal_list_with(user_history_model)
    def post(self, id):
        """
        Login user, send back JWT token
        """
        user = User.find_by_id(id)
        if not user:
            return {"message": "User not found"}, 404

        password = requests.json.get('password')
        if not user.check_password(password):
            return {"message": "Invalid password"}, 400

        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = user.generate_auth_token(exp).decode('utf-8')

        return {"token": token, "expiration": exp}, 200
    


@history_ns.route('/')
class HistoryList(Resource):
    @history_ns.marshal_list_with(user_history_model)
    def get(self):
        """
        Get entire user search history
        """
        # get the user_id from the token
        user_id = User.get_user_id_from_token(requests)

        # retrieve the user's search history from the database
        history = SearchHistory.query.filter_by(user_id = user_id)

        # return the search history as a response
        return history, 200
    
        

    def post(self):
        """
        Add search query to history
        """
        # get the user_id from the token
       # user_id = User.get_user_id_from_token(requests) 

        # get the search query from the request data
        query = history_ns.payload
        print (query)
        # add the search query to the user's search history in the database
       # User.add_to_history(user_id, query)

        # return a success message as a response
        return {"message": "Search query added to history"}, 201
       

@history_ns.route('/<id>')
class History(Resource):
    @history_ns.marshal_list_with(user_history_model)
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

