from flask import jsonify, request
import bcrypt
import jwt
from datetime import datetime, timedelta
from app import mongo_db
from dotenv import load_dotenv
import os
load_dotenv()


class AuthController:
    def login(self, username, password):
            secret_key = os.environ['TOKEN_SECRET']
            # Retrieve user data from the database based on the username
            user_data = mongo_db.users.find_one({'username': username})

            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                # Password is correct, generate JWT token
                token_payload = {
                    'user_id': str(user_data['_id']),
                    'username': user_data['username'],
                    'exp': datetime.utcnow() + timedelta(day=1)  # Token expiration time (1 day)
                }
                jwt_token = jwt.encode(token_payload, secret_key, algorithm='HS256')
                return {'token': jwt_token, 'isSuccess': True}, 200  # Return the JWT token and HTTP status 200 (OK)
            else:
                # Invalid credentials
                return {'message': 'Invalid credentials'}, 401
    
    def verify_token(self, token):
        secret_key = os.environ['TOKEN_SECRET']
        try:
            # Decode the JWT token using the secret key
            token_without_bearer = token[7 : ]
            print(token_without_bearer)
            decoded_token = jwt.decode(token_without_bearer, secret_key, algorithms=['HS256'])
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(decoded_token)
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            return {'isTokenExpired':False,'token':decoded_token,'isTokenInvalid':False}
        except jwt.ExpiredSignatureError:
            # Token has expired
            return {'isTokenExpired':True,'token':'','isTokenInvalid':False}
        except jwt.InvalidTokenError:
            # Invalid token
            return {'isTokenExpired':False,'token':'','isTokenInvalid':True}