from exceptiongroup import catch
from flask_restx import Resource, Namespace
from .api_models import profile_details_model ,user_profile_model, user_history_model, user_updated_profile_model, req_signup_model, req_login_model, res_login_model, req_search_model, req_history_model
from .models import SearchHistory, User
from .extensions import db, api
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
import requests

profile_ns = Namespace('profile', description='Create, update or delete user profile')
login_ns = Namespace('login', description='Handle user log in')
search_ns = Namespace('search', description='Search for items and products')
history_ns = Namespace('history', description='Get, update or delete user history')

@profile_ns.route('')
class Profile(Resource):
    
    @jwt_required()
    @profile_ns.marshal_with(profile_details_model)
    def get(self):
        """
        Get the user account details
        """
        user_details = get_jwt_identity()
        user = User.query.filter_by(id = user_details["id"]).first()
        
        return user
    
    @profile_ns.expect(req_signup_model)
    def post(self):
        """
        Create a user account
        """
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
    @profile_ns.expect(user_updated_profile_model)
    @profile_ns.marshal_with(user_updated_profile_model)
    def put(self):
        """
        Update a user account
        """
        user_details = get_jwt_identity()
        user = User.query.filter_by(id = user_details["id"]).first()
        
        # Update account details for the user
        user.username = profile_ns.payload["username"]
        user.password_hash = profile_ns.payload["password"]
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
    
    @login_ns.expect(req_login_model)
    def post(self):
        """
        Log In user and return a JWT token
        """
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
        """
        Get search history for a user
        """
        user_details = get_jwt_identity()
        user = User.query.filter_by(email = user_details["email"]).first()
        return SearchHistory.query.filter_by(user_id = user.id).all()
    
    @jwt_required()
    @history_ns.expect(req_history_model)
    @history_ns.marshal_with(user_history_model)
    def post(self):
        """
        Add search query to the search history database
        """
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
    @search_ns.expect(req_search_model)
    def post(self):
        """
        Search for a products or items requested in the query
        """
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
        products = get_all(search_query)
        return products, 200


# class CallProducts(Resource):
#     def get(self, query):
#         products = get_all(query)
#         return jsonify({'products': products})

# api.add_resource(CallProducts, "/products/<query>")


def get_aliexpress(search_query):
        url = f"https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword?keyword={search_query}&page=1&sortBy=best_match"
        headers = {
            "X-RapidAPI-Key": "187882b51bmshe44dfc8172e8e0ep160f0djsn9e44e22eb233",
        }
        r = requests.get(url, headers=headers)
        
        # if r.status_code != 200:
        #       return []

        data = r.json()
        results = []
        # print(data['item']['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items'])

        try:
            for result_data in data['item']['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']:
                description = result_data.get('shortDescription', None)
                # price = result_data['priceInfo']['linePrice', None]
                # rating = result_data['rating']['averageRating']
                product_image = result_data.get('image', None)
                title = result_data.get('name', None)
                review = result_data.get('numberOfReviews',None)

                # results.append({'description': description,'price': price,'rating': rating,'image': product_image,'name': title,'review': review})
                results.append({'description': description, 'image': product_image, "title": title, 'review': review,})
        except KeyError:
            if r.status_code == 429 or int(r.status_code) == 429:
                print(data)
                print('(get_aliexpress) - Rate limit likely exceeded, results not included')
            else:
                print("(get_aliexpress) - Encountered an error while processing your query")
        
        results = sortProducts(results)
        return results[:4]
        # return results
  
def get_amazon(search_query):
        url = f"https://amazon-price1.p.rapidapi.com/search?keywords={search_query}&marketplace=ES"
        headers = {
            "X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
        }
        r = requests.get(url, headers=headers)
        data = r.json()
        results = []

        try:
            for result_data in data:
                price = result_data["listPrice"]
                rating = result_data['rating']
                product_image = result_data['imageUrl']
                title = result_data['title']
                link = result_data['detailPageURL']
                review = result_data['totalReviews']
                results.append({'price': price, 'rating': rating, 'image': product_image, 'name': title, 'review': review, 'link':link})
        except Exception as e:
            print(e)
            print('(get_amazon) experienced an error')
        results = sortProducts(results)
        return results[:4]
        # return results
        
def get_ebay(search_query):
        url = f"https://ebay-search-result.p.rapidapi.com/search/{search_query}"
        headers = {
            "X-RapidAPI-Key": "355db28ab7msh93f4cc83a76dbbcp154e0cjsn5279bcdc45dc",
        }
        r = requests.get(url, headers=headers)
        data = r.json()
        offers = []

        try:
            for result_data in data["results"]:
                price = result_data["price"]
                rating = result_data['rating']
                product_image = result_data['image']
                title = result_data['title']
                link = result_data['url']
                offers.append({'price': price, 'rating': rating, 'image': product_image, 'name': title, 'link': link})
        except Exception as e:
            print(e)
            print("(get_ebay) experienced an error")
        
        offers = sortProducts(offers)
        return offers[:4]
        # return offers
        
def get_real_time(search_query):
         
        url = f"https://real-time-product-search.p.rapidapi.com/search?q={search_query}&country=us&language=en"
        headers = {
            "X-RapidAPI-Key": "8f9c5d2a43msh04d0a3420c2e09bp156401jsn9667246efdc5",

        }
        r = requests.get(url, headers=headers)
        data = r.json()
        # if r.status_code != 200:
        #       return []
        offers = []

        try:
            for offer_data in data["data"]:
                price = offer_data["offer"]["price"]
                description = offer_data['product_description']
                rating = offer_data['product_rating']
                product_image = offer_data['product_photos'][0]
                title = offer_data['product_title']
                link = offer_data['offer']['offer_page_url']
                offers.append({'price': price, 'description': description, 'rating': rating, 'image': product_image, 'name': title, 'link': link})
        except Exception as e:
            print(e)
            print("(get_real_time) experienced an error")
        
        offers = sortProducts(offers)
        return offers[:4]
        # return offers


def get_all(search_query):
        amazon_results = get_amazon(search_query=search_query)
        aliexpress_results = get_aliexpress(search_query=search_query)
        ebay_results = get_ebay(search_query=search_query)
        real_time_results = get_real_time(search_query=search_query)
        results = amazon_results  + ebay_results + real_time_results + aliexpress_results
        id = 1
        for product in results:
              product.update({"id": id})
              id += 1

        # result = sortProducts(results)
        # MB = marginalBenefit(availableProducts(results))
        # currency = defaultCurrency(sortProducts(results))
        # MB = marginalBenefit(currency)
    

        # return   currency, MB
        result = defaultCurrency(results)
        return result

def availableProducts(products):
      results = []
      
      for product in products:
          if product["price"] == "" or product["price"] == None or product["price"].count("$") > 1:
              continue
          
        #   if product["description"] == "" or product["description"] == None:
        #       continue
          
          if product["rating"] == "" or product["rating"] == None:
              continue
          
          if product["image"] == "" or product["image"] == None:
              continue
          
        #   if product["title"] == "" or product["title"] == None:
        #       continue
          
          if product["link"] == "" or product["link"] == None:
              continue
          
          
          results.append(product)
          
      return results

def sortProducts(products):
        available_products = availableProducts(products)
        sorted_products = sorted(available_products, key=lambda data: (data["price"].replace(',', '')), reverse=True)
        return sorted_products

def defaultCurrency(products):
    for i in products:
        original_currency = i["price"]
        if "€" in original_currency:
            if original_currency.startswith("€"):
                new_price = float(original_currency.replace(",", ".").replace("\xa0", "")) * 1.07
                i["price"] =  str(new_price)
            elif original_currency.endswith("€"):
                without_symbol = original_currency[:-1]
                new_price = float(without_symbol.replace(",", ".").replace("\xa0", "")) * 1.07
                i["price"] = str(new_price)
    return products





# def marginalBenefit(products):
#     #  marginal_benefits = []
#      for i in range(1, len(products)):

#         if ' ' in products[i]["rating"]:
#             rating = float(products[i]["rating"].rsplit(' ')[0])
#         else:
#             rating = float(products[i]["rating"])

#         try:
#             review = float(products[i]["review"])
#         except Exception as e:
#             review = 1

         
#         min_price = float(products[i - 1]["price"].replace("$", "").replace(".", "").replace(",", "").replace("\xa0", "").replace("€", ""))
#         current_price = float(products[i]["price"].replace("$", "").replace(".", "").replace(",", "").replace("\xa0", "").replace("€", ""))
#         change_in_price = current_price - min_price
#         rating = float(products[i]["rating"].rsplit(' ')[0])
#         change_in_quantity = rating * review
#         marginal_benefit = change_in_price / change_in_quantity
#         # marginal_benefits.append(marginal_benefit)

#      return marginal_benefit

# def marginalBenefit(products):
#     for i in products:
#         if ' ' in products.keys[i]["rating"]:
#             rating = float(products[i]["rating"].rsplit(' ')[0])
#         else:
#             rating = float(products[i]["rating"])
#         try:
#             review = float(products[i]["review"])
#         except Exception as e:
#             review = 1

#         min_price = float(products[list(products())[i - 1]]["price"].replace("$", "").replace(".", "").replace(",", "").replace("\xa0", "").replace("€", ""))
#         current_price = float(products[i]["price"].replace("$", "").replace(".", "").replace(",", "").replace("\xa0", "").replace("€", ""))
#         change_in_price = current_price - min_price
#         rating = float(products[i]["rating"].rsplit(' ')[0])
#         change_in_quantity = rating * review
#         marginal_benefit = change_in_price / change_in_quantity

#         return marginal_benefit






          
# =======
#                i["price"] = "$" + str(new_price)
#            elif original_currency.endswith("€"):
#                without_symbol = original_currency[:-1]
#                new_price = float(without_symbol.replace(",", ".").replace("\xa0", "")) * 1.07
#                i["price"] = "$" + str(new_price)
#    return products
#
#def marginalBenefit(products):
#     marginal_benefits = []
#     for i in range(1, len(products)):
#
#        if ' ' in products[i]["rating"]:
#            rating = float(products[i]["rating"].rsplit(' ')[0])
#        else:
#            rating = float(products[i]["rating"])
#
#        try:
#            review = float(products[i]["review"])
#        except Exception as e:
#            review = 1
#
#         
#        min_price = float(products[i - 1]["price"].replace("$", "").replace(".", "").replace(",", ""))
#        current_price = float(products[i]["price"].replace("$", "").replace(".", "").replace(",", ""))
#        change_in_price = current_price - min_price
#        rating = float(products[i]["rating"].rsplit(' ')[0])
#        # review = float(products[i]['review'])
#        # change_in_quantity = sum(rating) / len(rating)
#        change_in_quantity = rating * review
#        marginal_benefit = change_in_price / change_in_quantity
#        marginal_benefits.append(marginal_benefit)
#
#     return marginal_benefits
