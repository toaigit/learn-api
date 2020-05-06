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




def accesstokenrequired(f):
	@wraps(f)
	def tokenrequired(*args, **kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']		
		if not token:
			return jsonify({'message':'access token required'})
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			userdata = mongo.db.users.find_one({'public_id':data['public_id']})
			current_user = userdata
		except Exception as e:
			print (str(e))
			return jsonify({'message':'access token failed to be retrieved'})
		return f(current_user,*args,**kwargs)
	return tokenrequired


class Home(Resource):
	def get(self):
		auth = request.authorization

		if not auth or not auth.username or not auth.password:
			return jsonify({'message':'Authorization required'})
		username = auth.username
		password = auth.password
		userdata = mongo.db.users.find_one({'username':username})
		if len(userdata) == 0 or userdata is None:
			return jsonify({'message':'no user'})
		if pbkdf2_sha256.verify(password,userdata['password']):
			token = jwt.encode({'public_id':userdata['public_id'],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},
				app.config['SECRET_KEY'])
			return jsonify({'yourtoken':json.dumps(token.decode("utf-8"))})
		return jsonify({'message':'Authorization required'})



class Users(Resource):

	def get(self):
		users_list = []		
		try:
			items = mongo.db.users.find()
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to fetch users, please try later'})
		if items.count() == 0:
			return jsonify({'message':"users list empty, please add users"})
		for item in items:
			usersdict = {}
			for k,v in item.items():				
				if k == '_id':
					continue
				else:
					usersdict[k] = v
			if usersdict['active'] == 'yes':
				users_list.append(usersdict)
			else:
				continue
		return jsonify({"Total users":len(users_list),"users list":users_list})


	def post(self):
		userJson = request.get_json(force=True)
		if userJson is None:
			return jsonify({'message':'please provide a valid username and password'})
		username = userJson['username']
		password = userJson['password']
		hashed_password = pbkdf2_sha256.hash(password)
		userdata = {'username':username,'password':hashed_password,'public_id':str(uuid.uuid4()),'active':'yes'}
		try:
			mongo.db.users.insert_one(userdata)
		except Exception as e:
			print (str(e))
			return jsonify({'message':'unable to patch the product now, please try later'})
		return jsonify({"message":"user created"})




class Products(Resource):
	@accesstokenrequired
	def get(self,current_user):		

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




api.add_resource(Home,'/api/v1/' ,'/api/v1/login')
api.add_resource(Users,'/api/v1/users')
api.add_resource(Products, '/api/v1/products')
api.add_resource(Product, '/api/v1/product/<string:productid>')


if __name__ == '__main__':
    app.run(debug=True,port=5000)