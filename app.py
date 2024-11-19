import cv2
import os
import sys
import io
import shutil
import base64
import subprocess
import pytesseract
from PIL import Image
from flask import Flask, render_template, request, jsonify

from car_base_modules import car_extraction, car_parts_segregation, document_analysis, process_image

app = Flask(__name__)


# Set the folder to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<section>', methods=['POST'])
def upload(section):
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Process the image (implement your logic in this function)
    # result_data = process_image(file_path)
    result_data = {"result": "", "image_path": file_path}
    
    return jsonify({"result": result_data, "image_path": file_path})



#############################################################################################
######################################## API ROUTE ##########################################
#############################################################################################

@app.route('/car_parts_segregation', methods=['POST'])
def car_parts_segregation_route():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    # Check if the file has a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file is allowed (you can add more allowed extensions)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        image = Image.open(file.stream)
        print("saving the uploaded image...")
        image.save("/home/singhv04/work/code/projects/car_portal_analysis/car_parts_segregation.png", format="PNG")
        print("completed saving the uploaded image.")

        processed_image, metadata = car_parts_segregation(image)
        
        return jsonify({
            "processed_image": processed_image,
            "metadata": metadata
        })
    except Exception as e:
        print(f"Error processing image: {str(e)}", file=sys.stderr)
        return jsonify({"error": "Error processing image"}), 500
    

@app.route('/car_extraction', methods=['POST'])
def car_extraction_route():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    # Check if the file has a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file is allowed (you can add more allowed extensions)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        image = Image.open(file.stream)
        print("saving the uploaded image...")
        image.save("/home/singhv04/work/code/projects/car_portal_analysis/car_extraction.png", format="PNG")
        print("completed saving the uploaded image.")

        print(type(image), image)
        # processed_image, metadata = car_extraction(image)
        # processed_image, metadata = process_image(image)

        temp_processed_image, temp_metadata = car_extraction(image)
        
        img_name = "car_damage_full_view.png"
        processed_image, metadata = process_image(image, source_img_path = '/home/singhv04/work/code/projects/car_portal_analysis/results/car_extraction/car_extraction.png', result_dir_path="/home/singhv04/work/code/projects/car_portal_analysis/results/car_damage_full_view", save_img_name=img_name)
        
        bg_img  = cv2.imread("/home/singhv04/work/code/projects/car_portal_analysis/results/car_extraction/bg_car_extraction.png")
        fg_img = cv2.imread("/home/singhv04/work/code/projects/car_portal_analysis/results/car_damage_full_view/car_extraction.png")

        result_img = cv2.bitwise_or(fg_img,bg_img)
        _, buffer = cv2.imencode('.png', result_img)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        fimage_base64 = f"data:image/png;base64,{image_base64}"



        print("processed image : ", type(image_base64))
        return jsonify({
            "processed_image": fimage_base64,
            "metadata": metadata
        })
    except Exception as e:
        print(f"Error processing image: {str(e)}", file=sys.stderr)
        return jsonify({"error": "Error processing image"}), 500
    

@app.route('/process_image', methods=['POST'])
def process_image_route():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    # Check if the file has a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file is allowed (you can add more allowed extensions)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        image = Image.open(file.stream)
        print("saving the uploaded image...")
        image.save("/home/singhv04/work/code/projects/car_portal_analysis/car_damage.png", format="PNG")
        print("completed saving the uploaded image.")

        processed_image, metadata = process_image(image)

        return jsonify({
            "processed_image": processed_image,
            "metadata": metadata
        })
    except Exception as e:
        print(f"Error processing image: {str(e)}", file=sys.stderr)
        return jsonify({"error": "Error processing image"}), 500


@app.route('/document_analysis', methods=['POST'])
def document_analysis_route():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    # Check if the file has a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file is allowed (you can add more allowed extensions)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        image = Image.open(file.stream)
        print("saving the uploaded image...")
        image.save("/home/singhv04/work/code/projects/car_portal_analysis/document_analysis.png", format="PNG")
        print("completed saving the uploaded image.")

        processed_image, metadata = document_analysis(image)
        
        return jsonify({
            "processed_image": processed_image,
            "metadata": metadata
        })
    except Exception as e:
        print(f"Error processing image: {str(e)}", file=sys.stderr)
        return jsonify({"error": "Error processing image"}), 500


#############################################################################################
######################################## Chatbot ############################################
#############################################################################################

# @app.route("/chatbot")
# def chatbot():
#     return render_template("chatbot.html")

# @app.route("/chatbot", methods=["POST"])
# def chatbot_response():
#     data = request.get_json()
#     question = data.get("message")
#     response = question
#     return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)