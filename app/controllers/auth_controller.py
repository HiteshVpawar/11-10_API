from flask import jsonify, request
import bcrypt
import jwt
from datetime import datetime, timedelta
from app import mongo_db
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
load_dotenv()


class AuthController:
      
    def hash_password(self, password):
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password.decode('utf-8')

    def Sign_up(self, username, email, password, confirmPassword):
        secret_key = os.environ['TOKEN_SECRET']
        
        existing_user = mongo_db.userSignup.find_one({'username': username})
        if existing_user:
            return {'message': 'Username is already exist'}, 400  
        existing_email = mongo_db.userSignup.find_one({'email': email})
        if existing_email:
            return {'message': 'Email is already exist'}, 400 

        if password != confirmPassword:
            return {'message': 'Passwords do not match'}, 400  

        hashed_password = self.hash_password(password)
        new_user = {
            'username': username,
            'email': email,
            'password': hashed_password,
        }
        user_id = mongo_db.userSignup.insert_one(new_user).inserted_id

        token_payload = {
            'user_id': str(user_id),
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=1)   
        }
        jwt_token = jwt.encode(token_payload, secret_key, algorithm='HS256')

        return {'token': jwt_token, 'isSuccess': True}, 200  



    # def login(self, username, password):
    #         secret_key = os.environ['TOKEN_SECRET']
    #         user_data = mongo_db.userSignup.find_one({'username': username})

    #         if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
              
    #             token_payload = {
    #                 'user_id': str(user_data['_id']),
    #                 'username': user_data['username'],
    #             }
    #             jwt_token = jwt.encode(token_payload, secret_key, algorithm='HS256')
    #             return {'token': jwt_token, 'isSuccess': True}, 200  
    #         else:
    #             return {'message': 'Invalid credentials'}, 401

    def login(self, username, password):
        secret_key = os.environ['TOKEN_SECRET']
        user_data = mongo_db.userSignup.find_one({'username': username})

        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            token_payload = {
                'user_id': str(user_data['_id']),
                'username': user_data['username'],
            }
            jwt_token = jwt.encode(token_payload, secret_key, algorithm='HS256')
            return {'token': jwt_token, 'user_id': str(user_data['_id']), 'isSuccess': True}, 200  
        else:
            return {'message': 'Invalid credentials'}, 401
    
    def verify_token(self, token):
        secret_key = os.environ['TOKEN_SECRET']
        try:
            token_without_bearer = token[7 : ]
            print(token_without_bearer)
            decoded_token = jwt.decode(token_without_bearer, secret_key, algorithms=['HS256'])
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(decoded_token)
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            return {'isTokenExpired':False,'token':decoded_token,'isTokenInvalid':False}
        except jwt.ExpiredSignatureError:
            return {'isTokenExpired':True,'token':'','isTokenInvalid':False}
        except jwt.InvalidTokenError:
            return {'isTokenExpired':False,'token':'','isTokenInvalid':True}