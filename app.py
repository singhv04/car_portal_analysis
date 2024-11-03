import sys
import io
import shutil
import base64
import subprocess
import pytesseract
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

#############################################################################################
##################################### API CORE FUNCTIONS ####################################
#############################################################################################


def car_parts_segregation(image):
    """
    Run the segmentation prediction script with specified arguments.
    Set the working directory and run a specified Python program.

    Args:
        directory (str): The path to the directory to set as the working directory.
        program (str): The name of the Python program to run (should include .py extension).
    """
    working_directory = '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/'
        
    # Define the command and its arguments
    command = [
        'python3', 'segment/predict_segment.py',
        '--data', '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/data/data_carparts.yaml',
        '--weights', 'car_parts_01/myrun/weights/best.pt',
        '--source', '/home/singhv04/work/code/projects/car_portal_analysis/car_parts_segregation.png',
        '--img', '320',
        '--project', '/home/singhv04/work/code/projects/car_portal_analysis/results',
        '--name', 'car_parts'
    ]

    result_dir_path = "/home/singhv04/work/code/projects/car_portal_analysis/results/car_parts"
    if os.path.exists(result_dir_path):
        shutil.rmtree(result_dir_path)

    
    try:
        # Change to the working directory
        os.chdir(working_directory)
        print(f"Changed working directory to: {working_directory}")
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        # Print the output and errors, if any
        print("Output:\n", result.stdout)

        result_image_path = result_dir_path+"/car_parts_segregation.png"
        with Image.open(result_image_path) as image:
            # Create a BytesIO object to hold the image data
            buffered = io.BytesIO()
            # Save the image to the BytesIO object in PNG format
            image.save(buffered, format="PNG")
            # Get the byte data from the BytesIO object
            img_bytes = buffered.getvalue()
            # Encode the byte data to Base64
            base64_img = base64.b64encode(img_bytes).decode('utf-8')
            # Generate some sample metadata
            metadata = {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }

            os.remove("/home/singhv04/work/code/projects/car_portal_analysis/car_parts_segregation.png")
            return f"data:image/png;base64,{base64_img}", metadata

        if result.stderr:
            print("Errors:\n", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")


def document_analysis(image):
    # This is a placeholder for your image processing logic
    # For demonstration, we'll just draw a red rectangle on the image
    """
    python3 detect.py --weights pancard_detection/myrun2/weights/best.pt --img 320 --conf 0.5 --source /home/singhv04/work/demo_projects/id/pancard/Multi-Doc-OCR-PAN-v2i-yolov5pytorch/valid/images/ --project /home/singhv04/work/code/projects/segmentation_yolo_v5/testing --name pancard_det --hide-labels
    """

    working_directory = '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/'
        
    # Define the command and its arguments
    command = [
        'python3', 'detect.py',
        '--data', '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/data/data_pandcard.yaml',
        '--weights', 'pancard_detection/myrun2/weights/best.pt',
        '--source', '/home/singhv04/work/code/projects/car_portal_analysis/document_analysis.png',
        '--img', '320',
        '--project', '/home/singhv04/work/code/projects/car_portal_analysis/results',
        '--name', 'document_analysis'
    ]


    result_dir_path = "/home/singhv04/work/code/projects/car_portal_analysis/results/document_analysis"
    if os.path.exists(result_dir_path):
        shutil.rmtree(result_dir_path)

    try:
        # Change to the working directory
        os.chdir(working_directory)
        print(f"Changed working directory to: {working_directory}")
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        # Print the output and errors, if any
        print("Output:\n", result.stdout)

        result_image_path = result_dir_path+"/document_analysis.png"
        with Image.open(result_image_path) as image:
            # Create a BytesIO object to hold the image data
            buffered = io.BytesIO()
            # Save the image to the BytesIO object in PNG format
            image.save(buffered, format="PNG")
            # Get the byte data from the BytesIO object
            img_bytes = buffered.getvalue()
            # Encode the byte data to Base64
            base64_img = base64.b64encode(img_bytes).decode('utf-8')
            # Generate some sample metadata
            metadata = {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }

            os.remove("/home/singhv04/work/code/projects/car_portal_analysis/document_analysis.png")
            return f"data:image/png;base64,{base64_img}", metadata

        if result.stderr:
            print("Errors:\n", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

    


def process_image(image):

    """
    Run the segmentation prediction script with specified arguments.
    Set the working directory and run a specified Python program.

    Args:
        directory (str): The path to the directory to set as the working directory.
        program (str): The name of the Python program to run (should include .py extension).
    """
    working_directory = '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/'
        
    # Define the command and its arguments
    command = [
        'python3', 'segment/predict_segment.py',
        '--data', '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/data/data.yaml',
        '--weights', 'car_damage_01/myrun/weights/best.pt',
        '--source', '/home/singhv04/work/code/projects/car_portal_analysis/car_damage.png',
        '--img', '320',
        '--project', '/home/singhv04/work/code/projects/car_portal_analysis/results',
        '--name', 'car_damage'
    ]

    result_dir_path = "/home/singhv04/work/code/projects/car_portal_analysis/results/car_damage"
    if os.path.exists(result_dir_path):
        shutil.rmtree(result_dir_path)

    
    try:
        # Change to the working directory
        os.chdir(working_directory)
        print(f"Changed working directory to: {working_directory}")
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        # Print the output and errors, if any
        print("Output:\n", result.stdout)

        result_image_path = result_dir_path+"/car_damage.png"
        with Image.open(result_image_path) as image:
            # Create a BytesIO object to hold the image data
            buffered = io.BytesIO()
            # Save the image to the BytesIO object in PNG format
            image.save(buffered, format="PNG")
            # Get the byte data from the BytesIO object
            img_bytes = buffered.getvalue()
            # Encode the byte data to Base64
            base64_img = base64.b64encode(img_bytes).decode('utf-8')
            # Generate some sample metadata
            metadata = {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }

            os.remove("/home/singhv04/work/code/projects/car_portal_analysis/car_damage.png")
            return f"data:image/png;base64,{base64_img}", metadata

        if result.stderr:
            print("Errors:\n", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")



#############################################################################################
######################################## API ROUTE ##########################################
#############################################################################################

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


if __name__ == '__main__':
    app.run(debug=True)



"""
/home/singhv04/work/demo_projects/damage/car_damage/car-damage-coco-v9i-v1i-yolov5pytorch/samples/

/home/singhv04/work/demo_projects/damage/car_parts/car-seg-v4i-yolov5pytorch/samples/

/home/singhv04/work/demo_projects/id/pancard/Multi-Doc-OCR-PAN-v2i-yolov5pytorch/samples
"""