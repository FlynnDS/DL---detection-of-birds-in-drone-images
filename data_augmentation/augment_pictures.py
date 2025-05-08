from image_objects import AllImages
from typing import List
import os
import cv2

import random


from IPython.display import Image
import numpy as np
import random


from IPython.display import Image
import numpy as np
import random

def get_average_bounding_box(label_path: str):
    """label_path is the location to the yoloflow.txt file of the image. takes all the bounding boxes of the image and calculate the average"""
    with open(label_path) as f:
        bounding_boxes = f.readlines()
        
    bounding_boxes = [bounding_box.strip().split(" ") for bounding_box in bounding_boxes]
    #bird_class, x_center_rel, y_center_rel, width_rel, height_rel = map(float, largest_bounding_box.split(" "))
    
    try:
        average_rel_width = sum([float(bounding_box[3]) for bounding_box in bounding_boxes])/len(bounding_boxes)
        average_rel_height = sum([float(bounding_box[4]) for bounding_box in bounding_boxes])/len(bounding_boxes)
    except ZeroDivisionError:
        average_rel_width = 0
        average_rel_height = 0
    return (average_rel_width, average_rel_height)


def add_picture_to_picture(image_path: str, label_path: str, average_rel_width, average_rel_height):
    """file_name is the name of the file to be augmented onto
    folder_path is where the filename is in
    average_rel_width and average_rel_height should come from the function get_average_bounding_box(label_path)
    """        
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    h, w, channels = img.shape
    height_pixels = int(h*average_rel_height)
    width_pixels = int(w*average_rel_width)
        
    cropped_pil = all_images_objects.get_random_cropped_images(width_pixels)
    print(type(cropped_pil))
    
    # Convert PIL to OpenCV format
    cropped_np = np.array(cropped_pil)
    cropped_cv = cv2.cvtColor(cropped_np, cv2.COLOR_RGBA2BGRA)  # Preserve alpha channel
    print(random.randint(3+int(width_pixels*0.5), w-3-int(width_pixels*0.5)))
    # Choose a position to paste. At least 3 pixels from the border and half of the picture size to be added
    x_offset = random.randint(
        int(3 + width_pixels * 0.5),
        int(w - 3 - width_pixels * 0.5)
    )

    y_offset = random.randint(
        int(3 + height_pixels * 0.5),
        int(h - 3 - height_pixels * 0.5)
    )
    
    # Get overlay dimensions
    overlay_h, overlay_w = cropped_cv.shape[:2]
    
    # Make sure the overlay fits within the image bounds
    if y_offset + overlay_h > h:
        overlay_h = h - y_offset
        cropped_cv = cropped_cv[:overlay_h, :, :]
    
    if x_offset + overlay_w > w:
        overlay_w = w - x_offset
        cropped_cv = cropped_cv[:, :overlay_w, :]
    
    # Get the ROI from the original image
    roi = img[y_offset:y_offset+overlay_h, x_offset:x_offset+overlay_w]
    
    # Check channels
    ch = cropped_cv.shape[2]

    # Proper alpha blending
    if ch == 4:  # If we have an alpha channel
        # Extract the alpha channel and normalize to [0, 1]
        alpha = cropped_cv[:, :, 3] / 255.0
        
        # Create a 3-channel alpha mask
        alpha_3d = np.dstack((alpha, alpha, alpha))
        
        # Extract BGR channels from overlay
        overlay_bgr = cropped_cv[:, :, :3]
        
        # Calculate blended image
        blended = (1.0 - alpha_3d) * roi + alpha_3d * overlay_bgr
        
        # Replace the ROI with the blended image
        img[y_offset:y_offset+overlay_h, x_offset:x_offset+overlay_w] = blended.astype(np.uint8)
    else:
        # Just copy if no alpha
        img[y_offset:y_offset+overlay_h, x_offset:x_offset+overlay_w] = cropped_cv
    
    # below we are adding the newly generated image that is augmented with one extra bird
    # we add the label as well to the dataset
    x_offset_rel = x_offset/w
    y_offset_rel = y_offset/h
    x_rel = overlay_w/w
    y_rel = overlay_h/h
    new_yolo_label_str = f"0 {x_offset_rel+0.5*x_rel} {y_offset_rel+0.5*y_rel} {x_rel} {y_rel}"
    with open(label_path, "a") as f:
        f.write(f"\n{new_yolo_label_str}")
    cv2.imwrite(image_path, img)


def get_all_images_objects():
    all_images = AllImages()
    repo_path = "/notebooks/DL---detection-of-birds-in-drone-images"
    test_images = all_images.get_files_in_data_folder(f"{repo_path}/data/Harmful Birds Detection.v1i.yolov11/test")
    train_images = all_images.get_files_in_data_folder(f"{repo_path}/data/Harmful Birds Detection.v1i.yolov11/train")
    valid_images = all_images.get_files_in_data_folder(f"{repo_path}/data/Harmful Birds Detection.v1i.yolov11/valid")
    all_images.load_removed_background_pictures(f"{repo_path}/data/Subject images crows/Subjects not pixelated")
    return all_images

all_images_objects = get_all_images_objects()
