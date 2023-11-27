# app/views/user_view.py
from flask import jsonify
from app.controllers.chat_controller import ChatController
from bson import ObjectId 

chat_controller = ChatController() 

class ChatView:
    def __init__(self, chat_controller):
        self.chat_controller = chat_controller

    def chat(self, user_id, request):
        request_data = request.get_json()
        question = request_data.get('question')

        response_data = self.chat_controller.chat(user_id, question)

        # Convert ObjectId to string before returning the response
        if '_id' in response_data and isinstance(response_data['_id'], ObjectId):
            response_data['_id'] = str(response_data['_id'])

        return jsonify(response_data), 201

    
    # def get_chats(self, user_id):
    #  return jsonify(self.chat_controller.get_chats(user_id)), 200

    def get_chats(self, user_id):
        
        return jsonify(self.chat_controller.get_chats(user_id)), 200
    

    


    