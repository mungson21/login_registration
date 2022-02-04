from flask import render_template, request, redirect, session, flash, session
from flask_app import app

from flask_app.models.login_model import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# Create User
@app.route('/create_user', methods=['POST'])
def create_user():
    if User.validate_user(request.form) == False:
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.create_user(data)
    session['user_id'] = user_id

    return redirect ('/dashboard')

    # Old Code:
    # valid = User.validate_user(data)
    # if valid:
    #     results = User.create_user(data)
    #     return redirect(f'/dashboard/{results}')
    # return redirect('/')

# Dashboard:
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data ={
        'id': session['user_id']
    }

    users = User.get_one(data)

    return render_template('dashboard.html', users=users)


# -OLD CODE - Displays user info if successful -OLD CODE-
# @app.route('/dashboard/<int:user_id>')
# def get_one(user_id):
#     data = {
#         'id' : user_id
#     }
#     user = User.get_one(data)
#     return render_template('dashboard.html', user=user)

# Login Section:
@app.route('/login', methods=['POST'])
def login():

    data = {
        'email' : request.form['email']
    }

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect("/dashboard")



# Logout Section:
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')