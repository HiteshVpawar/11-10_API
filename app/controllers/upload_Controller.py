from app.models.user import User  # Import the User class
from app import mongo_db
from bson import ObjectId
import bcrypt
from flask import request, jsonify

class UploadController:
    def upload_file(self, pdf_file):
        # Assuming pdf_file is a binary PDF file
        file_data = {
            "file_content": pdf_file  # Save the binary data of the PDF
        }
        user_file = mongo_db.files.insert_one(file_data)
        print("**************************************************************")
        print(user_file)
        print("**************************************************************")
        return str(user_file.inserted_id)
    

    def get_text(self):
        texts = mongo_db.files.find({},{})
        texts_list=[]
        for x in texts:
            texts_list.append({
                '_id':str(x['_id']),
                'file_content': x['file_content']
            })
        response_data = {
                'data':texts_list
            }
        return response_data, 200
    

    def upload_Image(self, image_text):
        # Assuming pdf_file is a binary PDF file
        file_data = {
            "file_content": image_text  # Save the binary data of the PDF
        }
        user_file = mongo_db.imgfiles.insert_one(file_data)
        print("**************************************************************")
        print(user_file)
        print("**************************************************************")
        return str(user_file.inserted_id)    