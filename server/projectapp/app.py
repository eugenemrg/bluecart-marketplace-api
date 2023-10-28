# from flask import Flask, request, jsonify
# from flask_restful import Resource, Api
# from werkzeug.security import check_password_hash
# from flask_jwt_extended import JWTManager, create_access_token
# import requests
# import sqlite3
# from typing import Dict, List
# from projectapp import app
# from projectapp.models import User

# api = Api(app)
# jwt = JWTManager(app)


# @app.route('/')
# def hello_world():
#     return 'Hello, World welcome to my App!'


# @app.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])

# @app.route('/login', methods=['POST'])
# def login():
#     if not request.is_json:
#         return jsonify({"msg": "Missing JSON in request"}), 400

#     email = request.json.get('email', None)
#     password = request.json.get('password', None)

#     if not email or not password:
#         return jsonify({"msg": "Missing email and/or password parameter"}), 400

#     user = User.query.filter_by(email=email).first()

#     if not user or not check_password_hash(user.password, password):
#         return jsonify({"msg": "Invalid email and/or password"}), 401

#     access_token = create_access_token(identity=user.id)
#     return jsonify(access_token=access_token), 200



# @app.route('/profile', methods=['POST'])
# def create_profile():
#     email = request.json.get('email')
#     password = request.json.get('password')
#     confirm_password = request.json.get('confirm_password')

#     if not email or not password or not confirm_password:
#         return jsonify({"msg": "Missing data"}), 400

#     if password != confirm_password:
#         return jsonify({"msg": "Passwords do not match"}), 400

#     # Connecting to the database
#     connection = sqlite3.connect('app.db')
#     cursor = connection.cursor()

#     # Creating a new profile record
#     cursor.execute("INSERT INTO profiles (email, password) VALUES (?, ?)", (email, password))

    
#     connection.commit()
#     connection.close()

#     return jsonify({"msg": "User profile created successfully"}), 201




# @app.route('/profile', methods=['PATCH'])
# def update_profile():
#     email = request.json.get('email')
#     password = request.json.get('password')

#     if not email and not password:
#         return jsonify({"msg": "No data provided for update"}), 400

#     # Connecting to the database
#     connection = sqlite3.connect('app.db')
#     cursor = connection.cursor()

#     # Updating the profile record
#     cursor.execute("UPDATE profiles SET email=?, password=? WHERE email=?", (email, password, email))

#     # Saving the changes to the database
#     connection.commit()
#     connection.close()

#     return jsonify({"msg": "User profile updated successfully"}), 200




# @app.route('/profile', methods=['DELETE'])
# def delete_profile():
#     email = request.json.get('email')
#     if not email:
#         return jsonify({"msg": "Missing email"}), 400

#     try:
#         #  database connection
#         connection = sqlite3.connect('marketplace.db')
#         cursor = connection.cursor()

#         #  DELETE query to delete the profile with the specified email
#         cursor.execute("DELETE FROM profiles WHERE email=?", (email,))

        
#         connection.commit()
#         connection.close()

#         return jsonify({"msg": "Profile deleted successfully"}), 200

#     except Exception as e:
#         return jsonify({"msg": str(e)}), 500



# #  API keys and  headers or parameters
# amazon_api_key = '355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc'
# ebay_api_key = '355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc'
# shopify_api_key = 'YOUR_SHOPIFY_API_KEY'
# alibaba_api_key = 'YOUR_ALIBABA_API_KEY'

# headers = {
#     'Content-Type': 'application/json'
# }

# # Making the requests to each platform's API
# amazon_response = requests.get('https://amazon23.p.rapidapi.com/product-search', headers=headers, params={'Authorization': f'Bearer {amazon_api_key}'})
# ebay_response = requests.get('https://amazon23.p.rapidapi.com/product-search', headers=headers, params={'Authorization': f'Bearer {ebay_api_key}'})
# shopify_response = requests.get('https://shopify.com/api/products', headers=headers, params={'Authorization': f'Bearer {shopify_api_key}'})
# alibaba_response = requests.get('https://alibaba.com/api/products', headers=headers, params={'Authorization': f'Bearer {alibaba_api_key}'})

# #  product information from each platform's JSON response
# def extract_product_info(response):
#     if response.status_code == 200:
#         products = response.json()['products']
#         for product in products:
#             print(f"Product Name: {product['name']}, Product Price: {product['price']}")
#     else:
#         print(f"Error: {response.status_code}")

# # Displaying the product information for each platform
# print("Amazon Products:")
# extract_product_info(amazon_response)

# print("\nEbay Products:")
# extract_product_info(ebay_response)

# print("\nShopify Products:")
# extract_product_info(shopify_response)

# print("\nAlibaba Products:")
# extract_product_info(alibaba_response)



# @app.route('/history/<id>', methods=['DELETE'])
# def delete_history(id):
#     connection = sqlite3.connect('app.db')
#     cursor = connection.cursor()

#     # Deleting the history entry with  specified ID
#     cursor.execute("DELETE FROM history WHERE id=?", (id,))

#     # Saved the changes to the database
#     connection.commit()
#     connection.close()

#     return jsonify({"message": "History entry deleted successfully", "id": id}), 200






