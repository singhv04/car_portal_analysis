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

def process_image(file_path):
    # This is a placeholder for your image processing logic
    # You can implement your actual processing here
    return "Processed data about the image."

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


def process_image(image):
    # This is a placeholder for your image processing logic
    # For demonstration, we'll just draw a red rectangle on the image
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


# def process_image(image):
#     """
#     Set the working directory and run a specified Python program.

#     Args:
#         directory (str): The path to the directory to set as the working directory.
#         program (str): The name of the Python program to run (should include .py extension).
#     """
#     """
#     Run the segmentation prediction script with specified arguments.
#     """
#     # Set the working directory where the segment/predict.py script is located
#     working_directory = '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/'
    
#     # Define the command and its arguments
#     command = [
#         'python3', 'segment/predict.py',
#         '--data', '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/data/data.yaml',
#         '--weights', 'car_damage_01/myrun/weights/best.pt',
#         '--source', '/home/singhv04/work/demo_projects/damage/car_damage/car-damage-coco-v9i-v1i-yolov5pytorch/samples/severe_587_JPEG_jpg.rf.52b29727a6f8afcbc57589ba0af243ff.jpg',
#         '--img', '320',
#         '--project', '/home/singhv04/work/code/projects/segmentation_yolo_v5/testing',
#         '--name', 'tx'
#     ]
    
#     try:
#         # Change to the working directory
#         os.chdir(working_directory)
#         print(f"Changed working directory to: {working_directory}")

#         # Run the command
#         result = subprocess.run(command, capture_output=True, text=True)

#         # Print the output and errors, if any
#         print("Output:\n", result.stdout)


#         result_image_path = "/home/singhv04/work/code/projects/segmentation_yolo_v5/testing/tx/severe_587_JPEG_jpg.rf.52b29727a6f8afcbc57589ba0af243ff.jpg"
#         with Image.open(result_image_path) as image:
#             # Create a BytesIO object to hold the image data
#             buffered = io.BytesIO()
#             # Save the image to the BytesIO object in PNG format
#             image.save(buffered, format="PNG")
#             # Get the byte data from the BytesIO object
#             img_bytes = buffered.getvalue()
#             # Encode the byte data to Base64
#             base64_img = base64.b64encode(img_bytes).decode('utf-8')
#             # Generate some sample metadata
#             metadata = {
#                 "width": image.width,
#                 "height": image.height,
#                 "format": image.format,
#                 "mode": image.mode
#             }
#             return f"data:image/png;base64,{base64_img}", metadata

#         if result.stderr:
#             print("Errors:\n", result.stderr)
#     except Exception as e:
#         print(f"An error occurred: {e}")


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
