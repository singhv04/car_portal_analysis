import os
import io
import shutil
import base64
import subprocess
import pytesseract
from PIL import Image

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
                "classes": ['back_bumper', 'back_door', 'back_glass', 'back_left_door', 'back_left_light', 'back_light', 'back_right_door', 'back_right_light', 'front_bumper', 'front_door', 'front_glass', 'front_left_door', 'front_left_light', 'front_light', 'front_right_door', 'front_right_light', 'hood', 'left_mirror', 'object', 'right_mirror', 'tailgate', 'trunk', 'wheel'],
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


def car_extraction(image):
    """
    Extract car, given a full view.
    Run the segmentation prediction script with specified arguments.
    Set the working directory and run a specified Python program.

    Args:
        directory (str): The path to the directory to set as the working directory.
        program (str): The name of the Python program to run (should include .py extension).
    """
    working_directory = '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/'
        
    # Define the command and its arguments
    command = [
        'python3', 'segment/predict_segment_extract_mask.py',
        '--data', '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/data/data.yaml',
        '--weights', 'yolov5s-seg.pt',
        '--source', '/home/singhv04/work/code/projects/car_portal_analysis/car_extraction.png',
        '--img', '640',
        '--project', '/home/singhv04/work/code/projects/car_portal_analysis/results',
        '--class', '2',
        '--name', 'car_extraction'
    ]

    result_dir_path = "/home/singhv04/work/code/projects/car_portal_analysis/results/car_extraction"
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

        result_image_path = result_dir_path+"/car_extraction.png"
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
                "classes": ['car'],
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }

            os.remove("/home/singhv04/work/code/projects/car_portal_analysis/car_extraction.png")
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
                "classes": ['PAN_Number', 'dob', 'father_name', 'name', 'sign'],
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

    


def process_image(image, source_img_path = '/home/singhv04/work/code/projects/car_portal_analysis/car_damage.png',result_dir_path="/home/singhv04/work/code/projects/car_portal_analysis/results/car_damage", save_img_name="car_damage.png"):

    """
    Run the segmentation prediction script with specified arguments.
    Set the working directory and run a specified Python program.

    Args:
        directory (str): The path to the directory to set as the working directory.
        program (str): The name of the Python program to run (should include .py extension).
    """
    working_directory = '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/'

    project_dir_path = "/".join(result_dir_path.split("/")[:-1])
    project_name_path = result_dir_path.split("/")[-1]
        
    # Define the command and its arguments
    command = [
        'python3', 'segment/predict_segment.py',
        '--data', '/home/singhv04/work/code/projects/segmentation_yolo_v5/yolov5/data/data.yaml',
        '--weights', 'car_damage_01/myrun/weights/best.pt',
        '--source', source_img_path,
        '--img', '640',
        '--project', project_dir_path,
        '--name', project_name_path
        # '--conf-thres', '0.15'
    ]

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

        # result_image_path = result_dir_path+"/"+save_img_name
        print("checking save_img_name: ", save_img_name)
        if save_img_name=="car_damage_full_view.png":
            result_image_path = result_dir_path+"/car_extraction.png"        
        else:
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
                "classes":['Car-Damage'],
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }

            if save_img_name=="car_damage.png":
                os.remove("/home/singhv04/work/code/projects/car_portal_analysis/"+save_img_name)
            return f"data:image/png;base64,{base64_img}", metadata

        if result.stderr:
            print("Errors:\n", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")



"""
designation
long term growth
esops
"""