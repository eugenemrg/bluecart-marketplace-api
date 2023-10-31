from flask import make_response, jsonify, request
from projectapp.config import app
from projectapp.models import User
from flask_restful import Resource, Api
import requests
import time
api = Api(app)




# url = "https://real-time-product-search.p.rapidapi.com/search"

# querystring = {"q":"Nike shoes","country":"us","language":"en"}

# headers = {
# 	"X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
#     # 'x-rapidapi-key': os.environ.get("X_RAPIDAPI_KEY"),
# 	"X-RapidAPI-Host": "real-time-product-search.p.rapidapi.com"
#     # 'x-rapidapi-host': os.environ.get("X_RAPIDAPI_HOST_500_MO")

# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())


@app.route("/", methods=["GET"])
def get_products():
    url = "https://real-time-product-search.p.rapidapi.com/search"
    
    search_term = request.args.get('search_term', '').replace(' ', '+')
    query = request.args.get("q")
    # querystring = {"q": search_term}
    # description = responce.json()['data'][0]['product_description']
    querystring = {"q":"iphone","country":"us","language":"en"}


    headers = {
    "X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
	"X-RapidAPI-Host": "real-time-product-search.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params=querystring)
    
    data = r.json().get('data', [])
    if data:
            # description = responce.json()['data'][0]['product_description']
            description = data[0].get('product_description')
            return jsonify({"descrition": description})
    else:
         return jsonify({"am dead":"six months wasted"})
    # if r.status_code == 200:
    #     # print (r.json())
    #     return jsonify(r.json())
    # else:
    #     return jsonify({"error":"Request failed"})
    
time.sleep(60)


# url = "https://amazon23.p.rapidapi.com/product-search"

# querystring = {"query":"xbox","country":"US"}

# headers = {
# 	"X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
# 	"X-RapidAPI-Host": "amazon23.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# class Amazon_api(Resource):
#     def get(self):
#         url = "https://amazon23.p.rapidapi.com/product-search"
#         search_term = request.args.get('search_term', '').replace(' ', '+')
#         querystring = {"q": search_term}

#         headers = {
#             "X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
#             "X-RapidAPI-Host": "amazon23.p.rapidapi.com"
#         }
        
#         r = requests.get(url, headers=headers, params=querystring)
        
#         if r.status_code == 200:
#             return jsonify(r.json())
#         else:
#             return jsonify({"error": "Request failed"})

# api.add_resource(Amazon_api, "/products")




class GetUsers(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        resp = make_response(
            jsonify(users),
            200,
        )       
        return resp
api.add_resource(GetUsers, '/users')

