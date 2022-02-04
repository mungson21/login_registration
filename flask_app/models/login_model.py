from flask_app import app
from flask import flash
import re

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.config.mysqlconnection import connectToMySQL

db = 'login_registration_db'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO logins (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = " SELECT * FROM logins WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query='Select * FROM logins WHERE email = %(email)s;'
        results=connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(data):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        is_valid = True

        query = "SELECT * FROM logins WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)

        if len(results) >=1:
            flash('Email is already taken')
            is_valid = False

        # OLD CODE - Did not work w/out adding results variable.
        # Still adding users email w/ duplicate emails
        # if User.get_by_email({'email': data['email']}):
        #     flash('Email is already in use')
        #     is_valid=False

        if not EMAIL_REGEX.match(data['email']):
            flash('Email is not valid!')
            is_valid = False

        if len(data['first_name']) < 3:
            flash('First Name must be longer than 3 characters')
            is_valid = False

        if len(data['last_name']) < 3:
            flash('Last name must be longer than 3 characters')
            is_valid = False

        if len(data['password']) < 8:
            flash('Password must be longer than 8 characters')
            is_valid = False
        
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match')
            is_valid = False

        # -OLD CODE - Did not work for some reason
        # if user['password'] != user['confirm_password']:
        #     flash('Password and confirm password do not match')
        #     is_valid = False
        
        return is_valid

