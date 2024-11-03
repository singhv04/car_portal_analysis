import sys
import io
import base64
import subprocess
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw


from flask import Flask, render_template, request, jsonify
import os

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
    result_data = process_image(file_path)
    
    return jsonify({"result": result_data, "image_path": file_path})



def car_parts_segregation(image):
    # This is a placeholder for your image processing logic
    # For demonstration, we'll just draw a red rectangle on the image
    image.save("car_parts_segregation.png", format="PNG")

    draw = ImageDraw.Draw(image)
    draw.rectangle([20, 20, 100, 100], outline="green", width=5)
    
    # Convert the processed image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Generate some sample metadata
    metadata = {
        "width": image.width,
        "height": image.height,
        "format": image.format,
        "mode": image.mode
    }
    return f"data:image/png;base64,{img_str}", metadata

def document_analysis(image):
    # This is a placeholder for your image processing logic
    # For demonstration, we'll just draw a red rectangle on the image
    image.save("document_analysis.png", format="PNG")

    draw = ImageDraw.Draw(image)
    draw.rectangle([30, 30, 100, 100], outline="blue", width=5)
    
    # Convert the processed image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Generate some sample metadata
    metadata = {
        "width": image.width,
        "height": image.height,
        "format": image.format,
        "mode": image.mode
    }
    return f"data:image/png;base64,{img_str}", metadata


def process_image(image):
    # This is a placeholder for your image processing logic
    # For demonstration, we'll just draw a red rectangle on the image
    image.save("car_damage.png", format="PNG")

    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, 100, 100], outline="red", width=5)
    
    # Convert the processed image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Generate some sample metadata
    metadata = {
        "width": image.width,
        "height": image.height,
        "format": image.format,
        "mode": image.mode
    }
    return f"data:image/png;base64,{img_str}", metadata



@app.route('/car_analysis', methods=['POST'])
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
        processed_image, metadata = car_parts_segregation(image)
        
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
        processed_image, metadata = document_analysis(image)
        
        return jsonify({
            "processed_image": processed_image,
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
        processed_image, metadata = process_image(image)
        
        return jsonify({
            "processed_image": processed_image,
            "metadata": metadata
        })
    except Exception as e:
        print(f"Error processing image: {str(e)}", file=sys.stderr)
        return jsonify({"error": "Error processing image"}), 500


if __name__ == '__main__':
    app.run(debug=True)