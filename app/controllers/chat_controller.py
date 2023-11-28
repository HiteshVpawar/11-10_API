from flask import jsonify, request
from datetime import datetime, timedelta
from app import mongo_db
from dotenv import load_dotenv
from datetime import datetime
from app.service.chat_service import chat_service
load_dotenv()


class ChatController:
    # def chat(self, request):
    #     data = request.get_json()
    #     question = data.get('question')
    #     answer = chat_service(question)
    #     currentDateAndTime = datetime.now()
    #     currentTime = currentDateAndTime.strftime("%H:%M")
    #     if answer:
    #         mongo_payload = {'question':question, 'answer': answer ,'time': currentTime}
    #     else:
    #         mongo_payload = {'question':question, 'answer': "Sorry! Can you say again?" ,'time': currentTime}
    #     chat_id = mongo_db.chats.insert_one(mongo_payload).inserted_id
    #     chats = mongo_db.chats.find({},{})
    #     chat_list=[]
    #     for x in chats:
    #         chat_list.append({
    #             '_id':str(x['_id']),
    #             'question': x['question'],
    #             'answer':x['answer'],
    #             'time':x['time']
    #         })
    #     response_data = {
    #             'data':chat_list
    #         }
    #     return response_data, 200

    def chat(self, user_id, question):
        # Logic to handle the chat for a specific user ID
        answer = chat_service(user_id,question)
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M")
        if answer:
            mongo_payload = {'user_id': user_id, 'question': question, 'answer': answer, 'time': currentTime}
        else:
            mongo_payload = {'user_id': user_id, 'question': question, 'answer': "Sorry! Can you say again?", 'time': currentTime}
        chat_id = mongo_db.chats.insert_one(mongo_payload).inserted_id
        return mongo_payload
    
    # def get_chats(self, user_id):
    #     chats = mongo_db.chats.find({'user_id': user_id}, {})
    #     chat_list = []
    #     for x in chats:
    #         chat_list.append({
    #             '_id': str(x['_id']),
    #             'question': x['question'],
    #             'answer': x['answer'],
    #             'time': x['time']
    #         })
    #     response_data = {
    #         'data': chat_list
    #     }
    #     return response_data, 200

    def get_chats(self, user_id):
        chats = mongo_db.chats.find({'user_id': user_id}, {})
        chat_list = []
        for x in chats:
            chat_list.append({
                '_id': str(x['_id']),
                'question': x['question'],
                'answer': x['answer'],
                'time': x['time']
            })

        if chat_list: 
            response_data = {
                'data': chat_list
            }
            return response_data, 200
        else:
            return {'message': 'Data not found'}, 404
    

    