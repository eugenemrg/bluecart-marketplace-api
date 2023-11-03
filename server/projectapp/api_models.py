from flask_restx import fields

from .extensions import api

User_model = api.model("User",{
    "id": fields.Integer
    "username":fields.String
    "email":fields.String
    #"SearchHistory": :fields.Nested(User_model)
}),


SearchHistory_model = api.model("SearchHistory"{
        
      "id": fields.Integer
      "user_id":fields.Integer
      "name": fields.String
      "Search_date": fields.Integer
      "User": fileds_list(fields.Nested(User_model))
})

#SearchHistory_input_model= api.model("SearchInput",{

#})