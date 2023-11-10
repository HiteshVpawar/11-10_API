from flask import jsonify
from app.controllers.user_controller import UserController
from app.controllers.upload_Controller import UploadController
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import fitz  # PyMuPDF]
import base64
import requests
from app.controllers.upload_Controller import UploadController
import io
upload_controller = UploadController()  # Pass mongo_db object during instantiation
import pytesseract as tess 
from PIL import Image 
tess.pytesseract.tesseract_cmd=r'C:\Users\Hitesh.Pawar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'



class UploadView:
    def __init__(self, upload_controller):
        self.upload_controller = upload_controller
  
    def extract_text_from_pdf(self, pdf_file):
        try:
            # Use PdfReader instead of PdfFileReader
            pdf_reader = PdfReader(pdf_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            response = upload_controller.upload_file(pdf_text)
            return {'_id': response,'data':pdf_text}
        except Exception as e:
            # Handle exceptions as needed
            return str(e)
        

    def get_text(self):
        return jsonify(self.upload_controller.get_text()), 200   
        
    def extract_text_from_image(self, image_file):
        try:
            image_text = ""
            if image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                
                image = Image.open(image_file)
                image_text = tess.image_to_string(image)
                print(image_text)
                image = Image.open(image_file)
                response = upload_controller.upload_Image(image_text)

                return {'_id': response, 'data': image_text}
        except Exception as e:
            return str(e)