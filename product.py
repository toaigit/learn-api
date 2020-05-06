from flask import Flask,request,jsonify
from flask_pymongo import PyMongo,pymongo
from flask_restful import Resource, Api
from functools import wraps
import jwt
import uuid
import datetime
import json
from config import secret_key,dburi,dbname
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

#### configure the app starts
app.config['SECRET_KEY'] = secret_key
app.config["MONGO_DBNAME"] = dbname
app.config["MONGO_URI"] = dburi

### app configuration ends here


api = Api(app)
mongo = PyMongo(app)

class Products(Resource):
#       list all active products curl httpd://localhost:5000/api/v1/products using GET method
	def get(self):		

		product_list = []
		
		try:
			items = mongo.db.products.find()
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to fetch products, please try later'})

		if items.count() == 0:
			return jsonify({'message':"Products list empty, please add products"})

		for item in items:
			productdict = {}
			for k,v in item.items():
				
				if k == '_id':
					continue
				else:
					productdict[k] = v

			if productdict['active'] == 'yes':
				product_list.append(productdict)
			else:
				continue		

		return jsonify({"Total products":len(product_list),"product list":product_list})

#       create a new product /api/v1/products using POST method
	def post(self):
		
		product = request.get_json(force=True)

		try:
			prodid = product['productid']
			
			doc = mongo.db.products.find({'productid':prodid})

			if doc.count() != 0:
				return jsonify({'message':'product already exists'})

			mongo.db.products.insert_one(product)
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to add this product now, please try later'})


		return jsonify({'message':'product added !!'})


class Product(Resource):

#       list a particular product id with GET method /api/v1/product/<productid>
	def get(self,productid):
		pid = productid
		productdict = {}
		product_list = []
		try:
			doc = mongo.db.products.find_one({'productid':pid})
			if doc is None or len(doc) == 0:
				return jsonify({'message':'product with the id passed , does not exist'})
			for k,v in doc.items():				
				if k == '_id':
					continue
				else:
					productdict[k] = v
			product_list.append(productdict)
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to fetch the product now, please try later'})

		return jsonify(product_list)

#       update a particular product id with PUT method /api/v1/product/<productid>
#       and create if the product doesn't exist using upsert=True

	def put(self,productid):
		pid = productid
		product = request.get_json(force=True)

		try:
			doc = mongo.db.products.find_one({"productid":pid})
			mongo.db.products.update({"productid":pid},product,upsert=True)
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to update the product now, please try later'})
		return jsonify({"message":"product updated","productid":pid})


#       update a particular product id with PATCH method /api/v1/product/<productid>
#       If the productid doesn't exist, it just exist w/o creating the product as in the PUT method
#       It also validate to ensure all keys are valid.

	def patch(self,productid):
		pid = productid
		try:
			
			doc = mongo.db.products.find_one({'productid':pid})
			patches = request.get_json(force=True)
			status = []
			if doc is None or len(doc) == 0:
				return jsonify({'message':'product with the id passed , does not exist'})
			for k in patches.keys():
				if k in doc.keys():
					status.append(1)
				else:
					status.append(0)
			if 0 in status:
				return jsonify({'message':'one or more keys in the patch is not valid'})
			mongo.db.products.update_one({'productid':pid},{'$set':patches},upsert=True)
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to patch the product now, please try later'})
		return jsonify({"message":"product patched","productid":pid})

#       delete a particular product by setting active status to no
	def delete(self,productid):
		pid = productid
		try:
			doc = mongo.db.products.find_one({"productid":pid})
			if doc is None or len(doc) == 0:
				return jsonify({'message':'product with the id passed , does not exist'})
			mongo.db.products.update_one({'productid':pid},{"$set":{"active":"no"}},upsert=True)
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to delete the product now, please try later'})
		return jsonify({"message":"product removed","productid":pid})




api.add_resource(Products, '/api/v1/products')
api.add_resource(Product, '/api/v1/product/<string:productid>')


if __name__ == '__main__':
    app.run(debug=True,port=5000)



# curl http://localhost:5000/api/v1/product/6a789
#[
#  {
#    "active": "yes", 
#    "manufacturer": "APPL", 
#    "productcategory": "PHONE", 
#    "productdescription": "Apple iphone 11 White", 
#    "productid": "6a789", 
#    "productname": "iPhone 11"
#  }
#]

# curl -X DELETE http://localhost:5000/api/v1/product/6a789
#{
#  "message": "product removed", 
#  "productid": "6a789"
#}

# curl http://localhost:5000/api/v1/products
#{
#  "Total products": 3, 
#  "product list": [
#    {
#      "active": "yes", 
#      "manufacturer": "APPL", 
#      "productcategory": "PHONE", 
#      "productdescription": "Apple iphone 9 Black", 
#      "productid": "3a3dc", 
#      "productname": "iPhone 9"
#    }, 
#    {
#      "active": "yes", 
#      "manufacturer": "SAMS", 
#      "productcategory": "PHONE", 
#      "productdescription": "Samsung Galaxy s20 BLue", 
#      "productid": "281b4", 
#      "productname": "Samsung s20"
#    }, 
#    {
#      "active": "yes", 
#      "manufacturer": "GOOL", 
#      "productcategory": "PHONE", 
#      "productdescription": "Google Pixel 4 Gray", 
#      "productid": "19ab7", 
#      "productname": "Pixel 4"
#    }
#  ]
#}

# curl http://localhost:5000/api/v1/products
#{
#  "Total products": 4, 
#  "product list": [
#    {
#      "active": "yes", 
#      "manufacturer": "APPL", 
#      "productcategory": "PHONE", 
#      "productdescription": "Apple iphone 9 Black", 
#      "productid": "3a3dc", 
#      "productname": "iPhone 9"
#    }, 
#    {
#      "active": "yes", 
#      "manufacturer": "APPL", 
#      "productcategory": "PHONE", 
#      "productdescription": "Apple iphone 11 White", 
#      "productid": "6a789", 
#      "productname": "iPhone 11"
#    }, 
#    {
#      "active": "yes", 
#      "manufacturer": "SAMS", 
#      "productcategory": "PHONE", 
#      "productdescription": "Samsung Galaxy s20 BLue", 
#      "productid": "281b4", 
#      "productname": "Samsung s20"
#    }, 
#    {
#      "active": "yes", 
#      "manufacturer": "GOOL", 
#      "productcategory": "PHONE", 
#      "productdescription": "Google Pixel 4 Gray", 
#      "productid": "19ab7", 
#      "productname": "Pixel 4"
#    }
#  ]
#}
