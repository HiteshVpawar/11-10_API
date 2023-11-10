# app/views/user_view.py
from flask import jsonify
from app.controllers.user_controller import UserController
from PyPDF2 import PdfFileReader
user_controller = UserController()  # Pass mongo_db object during instantiation

class UserView:
    def __init__(self, user_controller):
        self.user_controller = user_controller

    def create_user(self, username, email, password):
        user = self.user_controller.create_user(username, email, password)
        return jsonify(user), 201
    
    def get_users(self):
        users = self.user_controller.get_users()
        # Convert the list of user objects to a list of dictionaries
        users_data = [user.to_dict() for user in users]
        return users_data, 200
    
    def update_user(self, user_id, new_username, new_email):
        updated_user = self.user_controller.update_user(user_id, new_username, new_email)
        if updated_user:
            return jsonify(updated_user.to_dict()), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    def delete_user(self, user_id):
        user_deleted = self.user_controller.delete_user(user_id)
        if user_deleted:
            return jsonify({'message': 'User deleted successfully', 'delete_count': user_deleted}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
        

