from flask_restx import Resource, Namespace
from .api_models import user_profile_model, user_history_model, user_updated_profile_model
from .models import SearchHistory, User
from .extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt

profile_ns = Namespace('profile', description='Create, update or delete user profile')
login_ns = Namespace('login', description='Handle user log in')
search_ns = Namespace('search', description='Search for items and products')
history_ns = Namespace('history', description='Get, update or delete user history')

@profile_ns.route('')
class Profile(Resource):
    def post(self):
        data = profile_ns.payload
        
        username = data["username"]
        email = data["email"]
        password = data["password"]
        
        user = User.query.filter_by(email = data['email']).first()

        if not user:
            new_user = User(username=username, email=email, password_hash = password)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'New user added successfully.'}, 201
        else:
            return {'message': 'User already exists.'}, 422
    
    @jwt_required()
    @profile_ns.marshal_with(user_updated_profile_model)
    def put(self):
        """
        Update a user account
        """
        user_details = get_jwt_identity()
        user = User.query.filter_by(id = user_details["id"]).first()
        
        # Update account details for the user
        user.username = profile_ns.payload["username"]
        user.password = profile_ns.payload["password"]
        db.session.commit()
        return user
    
    @jwt_required()
    def delete(self):
        """
        Delete a user account
        """
        user_details = get_jwt_identity()
        user = User.query.filter_by(email = user_details["email"]).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        # Delete all history data for the user
        search_items = SearchHistory.query.filter_by(user_id = user.id).all()
        for item in search_items:
            db.session.delete(item)
        db.session.commit()
        
        # Delete user account
        db.session.delete(instance=user)
        db.session.commit()
        return {}, 204
    
@login_ns.route('')
class LogIn(Resource):
    def post(self):
        data = login_ns.payload
        
        email = data["email"]
        password = data["password"]
        
        user = User.query.filter_by(email = email).first()
        
        if user and user.authenticate(password):
            access_token = create_access_token(identity={'id': user.id, 'email': email})
            return {'access_token': access_token}, 200
        else:
            return {"message": "Invalid email or password"}, 401

@history_ns.route('')
class History(Resource):
    
    @jwt_required()
    @history_ns.marshal_list_with(user_history_model)
    def get(self):
        user_details = get_jwt_identity()
        user = User.query.filter_by(email = user_details["email"]).first()
        return SearchHistory.query.filter_by(user_id = user.id).all()
    
    @jwt_required()
    @history_ns.marshal_with(user_history_model)
    def post(self):
        user_details = get_jwt_identity()
        user = User.query.filter_by(email = user_details["email"]).first()
        
        new_search_query = SearchHistory(
            user_id = user.id,
            name = history_ns.payload['query']
        )
        db.session.add(new_search_query)
        db.session.commit()
        
        return new_search_query, 201
    
@history_ns.route('/<int:id>')
class History(Resource):
    
    @jwt_required()
    def delete(self, id):
        """
        Delete a search history item from history using the id
        """
        user_details = get_jwt_identity()
        user = User.query.filter_by(email = user_details["email"]).first()
        search_item = SearchHistory.query.filter_by(id = id, user_id = user.id).first()
        
        if not search_item:
            return {"message": "Not Found. The resource does not exist or may have been deleted."}, 404
        
        db.session.delete(search_item)
        db.session.commit()
        return {}, 204

@search_ns.route('')
class Search(Resource):
    
    @jwt_required(optional=True)
    def get(self):
        
        search_query = history_ns.payload['query']
        
        # Save search query to history if user is authenticated
        if get_jwt_identity():
            user_details = get_jwt_identity()
            user = User.query.filter_by(email = user_details["email"]).first()
            
            new_search_query = SearchHistory(
                user_id = user.id,
                name = history_ns.payload['query']
            )
            db.session.add(new_search_query)
            db.session.commit()
        
        # TODO: KEN - Handle products and item search below
        pass
                    