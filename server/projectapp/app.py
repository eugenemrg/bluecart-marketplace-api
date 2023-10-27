from projectapp.config import db, app
from flask_restful import Api, Resource
from flask import make_response
import requests



url = "https://amazon23.p.rapidapi.com/product-search"

querystring = {"query":"xbox","country":"US"}

headers = {
	"X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
	"X-RapidAPI-Host": "amazon23.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

class GetProducts(Resource):
    def get(self):
        amazon_url = "https://amazon23.p.rapidapi.com/product-search"

        