from flask import Flask,render_template,request,redirect,url_for,jsonify,session
from flask_wtf.csrf import CSRFProtect,CSRFError
from flask_pymongo import PyMongo,pymongo
from config import secret_key, dburi, dbname

app = Flask(__name__)

##### csrf protection

csrf = CSRFProtect()
csrf.init_app(app)


#######################

app.config['SECRET_KEY'] = secret_key
app.config["MONGO_DBNAME"] = dbname
app.config["MONGO_URI"] = dburi

mongo = PyMongo(app)


@app.route('/')
def home():
	# rendering the home page
	if 'user' in session:
			return render_template('message.html',username=session['user'])		
	return redirect(url_for('login_func'))

@app.route('/redirected')
def redirected_req():
	return "your request has been redirected"

@app.route('/login',methods = ['GET','POST'])
def login_func():
	if request.method == "GET":
		message = 'hello there'
		return render_template('login.html',message=message)

	username = request.form['username']
	password = request.form['password']

	mongo.db.users.insert({'username':username,'password':password})

	print ("username is {} and password is {}".format(username,password))
	session['user'] = username
	return render_template('message.html',username=session['user'])

@app.route('/logout')
def logout():
	session.pop('user',None)
	return render_template('logout.html')

if __name__ == '__main__':
	app.run(debug=True,host='mykb.stanford.edu')
