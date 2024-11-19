import os
import cv2

image_dir = "demo_images/full_view/"
imgs = os.listdir(image_dir)

for idx,img in enumerate(imgs):
    # Read the input image
    image = cv2.imread(image_dir+img)

    image = cv2.resize(image, (640,640))
    # Validate the input image
    if image is None:
        print("Error: Image not found or invalid format.")
        exit(1)

    # # Apply Gaussian Blur
    # gaussian_kernel = (5, 5)  # Adjustable kernel size
    # gaussian_smoothed = cv2.GaussianBlur(image, gaussian_kernel, 0)

    # # Convert to grayscale for CLAHE
    # gray_image = cv2.cvtColor(gaussian_smoothed, cv2.COLOR_BGR2GRAY)

    # # Apply CLAHE
    # clip_limit = 2.0
    # tile_grid_size = (8, 8)
    # clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    # clahe_image = clahe.apply(gray_image)

    # # Display the images (optional)
    # cv2.imshow('Gaussian Smoothed', gaussian_smoothed)
    # cv2.imshow('CLAHE Enhanced', clahe_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    
    # Step 1: Apply Gaussian smoothing
    smoothed = cv2.GaussianBlur(image, (5, 5), 0)

    # Step 2: Convert to LAB and apply CLAHE
    lab = cv2.cvtColor(smoothed, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    clahe_applied = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    # Step 3: Normalize intensities
    normalized = cv2.normalize(clahe_applied, None, 0, 255, cv2.NORM_MINMAX)
    # Step 4: Apply bilateral filtering
    final_image = cv2.bilateralFilter(normalized, d=9, sigmaColor=75, sigmaSpace=75)


    # Display the images (optional)
    result = cv2.hconcat([image, clahe_applied, normalized, final_image])
    cv2.imshow('result Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if idx==2:
        break

