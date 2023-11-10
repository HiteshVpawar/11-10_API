# # app/controllers/user_controller.py
# from app.models.user import User

# class UserController:
#     def __init__(self):
#         self.users = []

#     def create_user(self, username, email):
#         user_id = len(self.users) + 1
#         user = User(user_id, username, email)
#         self.users.append(user)
#         return user

#     def get_users(self):
#         return [user.to_dict() for user in self.users]




# app/controllers/user_controller.py
from app.models.user import User  # Import the User class
from app import mongo_db
from bson import ObjectId
import bcrypt


class UserController:
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def create_user(self, username, email, password):
        hashed_password = self.hash_password(password)
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        # Insert user data into the 'users' collection
        user_id = mongo_db.users.insert_one(user_data).inserted_id
        # user= User(username, email, hashed_password, user_id) # To maintaine schema structure of response data
        user = {
            'user_id': str(user_id),
            'username':username,
            'email': email,
        }  # Create a User instance with the inserted user data
        return user  # Return the User instance representing the newly created user

    def get_users(self):
        # Retrieve all users from the 'users' collection as a list of dictionaries
        users_cursor = mongo_db.users.find({}, {'_id': 1, 'username': 1, 'email': 1})
        users_list = list(users_cursor)
        users = [User(user['username'], user['email'], "None" , user['_id']) for user in users_list]
        return users
    
    def update_user(self, user_id, new_username, new_email):
        # Update user data in the 'users' collection based on user_id
        result = mongo_db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'username': new_username, 'email': new_email}})
        if result.modified_count > 0:
            updated_user_data = {'_id': user_id, 'username': new_username, 'email': new_email}
            updated_user = User(new_username, new_email, user_id)
            return updated_user
        else:
            return None  # Return None if user with given user_id was not found

    def delete_user(self, user_id):
        # Delete user from the 'users' collection based on user_id
        result = mongo_db.users.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0