from flask import make_response, jsonify, request
from projectapp.config import app
from projectapp.models import User
from flask_restful import Resource, Api
import requests
import time
api = Api(app)





@app.route("/", methods=["GET"])
def get_products():
    url = "https://real-time-product-search.p.rapidapi.com/search"
    
    search_term = request.args.get('search_term', '').replace(' ', '+')
    query = request.args.get("q")
    # querystring = {"q": query, "search_text": search_term}
    querystring = {"q":search_term,"country":"us","language":"en"}


    headers = {
    "X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
	"X-RapidAPI-Host": "real-time-product-search.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params=querystring)
    
    if r.status_code == 200:
        # print (r.json())
        return jsonify(r.json())
    else:
        return jsonify({"error":"Request failed"})
    
time.sleep(60)

class GetUsers(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        resp = make_response(
            jsonify(users),
            200,
        )       
        return resp
api.add_resource(GetUsers, '/users')

