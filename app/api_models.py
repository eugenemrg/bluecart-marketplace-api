from flask_restx import fields

from .extensions import api

user_history_model = api.model("User History", {
    "id": fields.Integer,
    "name": fields.String,
    "search_date": fields.DateTime
})

user_updated_profile_model = api.model("Updated User Profile", {
    "username": fields.String,
    "password": fields.String
})

user_profile_model = api.model("User Profile", {
    "username": fields.String,
    "email": fields.String,
    "search_history": fields.List(fields.Nested(user_history_model))
})

# Expected request formats
req_signup_model = api.model("Sign Up Request", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
})

req_login_model = api.model("Log In Request", {
    "email": fields.String,
    "password": fields.String
})

req_search_model = api.model("Search Request", {
    "query": fields.String
})

req_history_model = api.model("User History Request", {
    "name": fields.String
})

# Expected response formats
res_login_model = api.model("Log In Response", {
    "access_token": fields.String
})
