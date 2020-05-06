from flask import Flask,render_template,request,jsonify, session
app = Flask(__name__)

app.config['SECRET_KEY'] = 'arandomkeyhere'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login_function():
    if request.method == "GET":
       message = 'hello there'
       return render_template('login.html',message=message)
    username = request.form['username']
    password = request.form['password']
    print ("username is {} and password is {}" . format(username,password))
    session['user'] = username
    return render_template('message.html',username=session['user'])

@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('logout.html')

if __name__=='__main__':
    app.run(debug=True,host='mykb.stanford.edu')
