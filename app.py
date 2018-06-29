from flask import Flask, request, redirect, render_template, session, flash, url_for
from mysqlconnection import MySQLConnector
import md5

app = Flask(__name__)
app.secret_key = "dfdfdsfsd.sdf.fsdfg.g.tedg.dt.gdf.gfd.!"
mysql = MySQLConnector(app, 'login')
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
  		flash("Email cannot be empty", 'danger')
	if request.form['name'] == "":
  		valid = False
  		flash("Name cannot be empty", 'danger')
	if request.form['password'] == "":
  		valid = False
    	flash("Password cannot be empty", 'danger')
	if request.form['password'] == request.form['confirm_password']:
  		valid = True
		flash('Passwords Match!', 'success')
	if valid != True:
  		return redirect('/')
	else:
  		query = "INSERT INTO `login`.`users` (`email`, `password`, `name`, `created_at`, `updated_at`) VALUES (:email, :password, :name, now(), now());"
		data = {
			"email": request.form['email'],
			"password": md5.new(request.form['password']).hexdigest(),
			"name": request.form['name']
		}
		mysql.query_db(query, data)
		flash("Successfully Registered. Login now", 'success')
		return redirect(url_for('login_now'))
  	return "got registered"


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    valid = True
    if request.form['email'] == "":
        valid = False
        flash("Email cannot be empty", 'danger')
    if request.form['password'] == "":
        valid = False
        flash("Password cannot be empty", 'danger')
    if not valid:
        return redirect("/")
    else:
        query = "SELECT * FROM users WHERE email = :email AND password = :password"
        data = {
            "email":request.form['email'],
            "password": md5.new(request.form['password']).hexdigest()
        }
        user = mysql.query_db(query, data)
        if len(user) != 0:
            session['id'] = user[0]['id']
            session['name'] = user[0]['name']
            return redirect(url_for('dashboard'))
    return redirect('/')
	
@app.route('/dashboard')
def dashboard():
  	return render_template('dashboard.html')


app.run(debug=True)