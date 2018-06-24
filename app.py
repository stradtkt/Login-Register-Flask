from flask import Flask, request, redirect, render_template, session, flash, url_for
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "dfdfdsfsd.sdf.fsdfg.g.tedg.dt.gdf.gfd.!"
mysql = MySQLConnector(app, 'airbnb')
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_now')
def login_now():
  	return render_template('login.html')

@app.route('/register_now')
def register_now():
  	return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
  	valid = True
  	print request.form
	if request.form['email'] == "":
  		valid = False
  		flash("Email cannot be empty")
	if request.form['name'] == "":
  		valid = False
  		flash("Name cannot be empty")
	if request.form['password'] == "":
  		valid = False
    	flash("Password cannot be empty")
	if valid != True:
  		return redirect('/')
	else:
  		query = "INSERT INTO `airbnb`.`users` (`email`, `password`, `name`, `created_at`, `updated_at`) VALUES (:email, :password, :name, now(), now());"
		data = {
			"email": request.form['email'],
			"password": bcrypt.generate_password_hash(request.form['password']),
			"name": request.form['name']
		}
		mysql.query_db(query, data)
		flash("Successfully Registered. Login now")
		return redirect(url_for('login_now'))
  	return "got registered"


@app.route('/login', methods=['POST'])
def login():
  	return "got logged in"
app.run(debug=True)