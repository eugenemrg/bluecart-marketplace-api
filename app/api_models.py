from flask_restx import fields

from .extensions import api

user_history_model = api.model("UserHistory", {
    "name": fields.String,
    "search_date": fields.DateTime
})

user_profile_model = api.model("UserProfile", {
    "username": fields.String,
    "email": fields.String,
    "search_history": fields.List(fields.Nested(user_history_model))
})