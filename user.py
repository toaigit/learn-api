from flask import Flask,render_template,request,redirect,url_for,jsonify,session
from flask_wtf.csrf import CSRFProtect,CSRFError
from flask_pymongo import PyMongo,pymongo
from config import secret_key, dburi, dbname
from flask_restful import Resource, Api
from passlib.hash import pbkdf2_sha256

import uuid
import datetime
import json

app = Flask(__name__)


#######################

app.config['SECRET_KEY'] = secret_key
app.config["MONGO_DBNAME"] = dbname
app.config["MONGO_URI"] = dburi

api = Api(app)
mongo = PyMongo(app)

class Home(Resource):
   def get(self):
       return jsonify({'message': 'Your API is running'})

class Users(Resource):

#       list users with GET method  /api/v1/users
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

#       delete the user with DELETE method /api/v1/users
	def delete(self):
		nameJson = request.get_json(force=True)
		if nameJson is None:
			return jsonify({'message':'please provide a valid username'})
		try:
			name = nameJson['username']
			doc = mongo.db.users.find_one({"username":name})
			if doc is None or len(doc) == 0:
				return (jsonify ({"message":"Not Found. Nothing to delete."}) )
                        
			mongo.db.users.delete_one(nameJson)
			return (jsonify ({"message":"Found.  Deleted user."}) )
		except Exception as e:
			print (str(e))
			return (jsonify ({"message":"Error finding"}) )

#       create user with POST method /api/v1/users
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

class User(Resource):

#       Search username /api/v1/search/username GET method
	def get(self,username):
                name = username
                try:
                      doc = mongo.db.users.find_one({"username":name})
                      if doc is None or len(doc) == 0:
                          return (jsonify ({"message":"No UserName in the database."}) )
                      return (jsonify ({"message":"Found"}) )
                except Exception as e:
                      print (str(e))
                      return (jsonify ({"message":"Error finding"}) )


api.add_resource(Home,'/api/v1')
api.add_resource(Users,'/api/v1/users')
api.add_resource(User,'/api/v1/user/<string:username>')

if __name__ == '__main__':
	app.run(debug=True,host='mykb.stanford.edu')


#(myflask) toaivo@debtest4:~/api/restapibooksource$ curl http://debtest4:5000/api/v1 (GET)
#{
#  "message": "Your API is running"
#}

#(myflask) toaivo@debtest4:~/api/restapibooksource$ ./crlogin.sh  (POST)
#{
#  "message": "user created"
#}
#{
#  "message": "user created"
#}

#(myflask) toaivo@debtest4:~/api/restapibooksource$ curl http://debtest4:5000/api/v1/users  (GET)
#{
#  "Total users": 2, 
#  "users list": [
#    {
#      "active": "yes", 
#      "password": "$pbkdf2-sha256$29000$KYVwTimF8D6HcC6lFGIMYQ$MJfxhWMYdSmAu18rPO549hUuec/BT3Qg0TqtkSD0xww", 
#      "public_id": "92f6f828-68e2-4539-8658-373b73a5fbc2", 
#      "username": "toai1"
#    }, 
#    {
#      "active": "yes", 
#      "password": "$pbkdf2-sha256$29000$XutdizHGeE8JgVDKWYvx3g$/3MxCFLfzxAiGrhIe5lPuKXu4KTUKoOBMmCAWLxnJcI", 
#      "public_id": "72faff8e-eda4-4f96-b21f-7e56feafe06d", 
#      "username": "toai2"
#    }
#  ]
#}
