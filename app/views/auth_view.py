# app/views/user_view.py
from flask import jsonify
from app.controllers.user_controller import UserController
import jwt
from app.models.user import User

user_controller = UserController()  # Pass mongo_db object during instantiation

class AuthView:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller

    def login(self, username, password):
        return self.auth_controller.login(username , password)
    
    def get_all_users(self, request):
        # Get the JWT token from the Authorization header
        jwt_token = request.headers.get('Authorization')

        # Call the method in AuthController to verify and decode the token
        decoded_token = self.auth_controller.verify_token(jwt_token)

        if decoded_token:
            # Token is valid, proceed to get all users
            users = self.auth_controller.get_all_users()
            return jsonify(users), 200
        else:
            # Invalid token, return unauthorized status
            return jsonify({'message': 'Unauthorized'}), 401
        
    def verify_token(self, token):
        return self.auth_controller.verify_token(token)