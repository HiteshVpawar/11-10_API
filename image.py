from flask import Flask, request, render_template
import cv2
import pytesseract

app = Flask(__name__)

# Configuration for Tesseract OCR (change this based on your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hitesh.Pawar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Function to process the uploaded image
def process_image(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Perform any processing or analysis on the image here
    # For example, let's use Tesseract OCR to extract text from the image
    text = pytesseract.image_to_string(img)
    
    return text

# Route for file upload
@app.route('/image', methods=['GET', 'POST'])
def image_text():
    image_info = None
    if request.method == 'POST':
        file = request.files['file']
        file_path = 'uploaded_image.jpg'  # Save the uploaded image temporarily
        file.save(file_path)
        
        # Process the uploaded image
        image_info = process_image(file_path)
        print(f"The extracted text is: {image_info}")
    
    return image_info

if __name__ == '__main__':
    app.run(debug=True)