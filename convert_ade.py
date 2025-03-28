import os
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm

# ADE 20K dataset


image_dir = "/home/paperspace/Documents/nika_space/ADE20K/ADEChallengeData2016/images/training_raw_low/"  # Update with the correct path
output_dir = "/home/paperspace/Documents/nika_space/ADE20K_npy/training_raw_low/"  # Output directory for .npy files

import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm

def convert_images_to_npy(image_dir, output_dir):
    """
    Converts all images in a directory to .npy format and saves them in the output directory.

    Args:
        image_dir (str): Path to the directory containing images.
        output_dir (str): Path to the directory where .npy files will be stored.
    """
    image_dir = Path(image_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)  # Create output directory if it doesn't exist

    image_paths = sorted(list(image_dir.rglob("*.jpg")) + list(image_dir.rglob("*.JPEG")))

    if not image_paths:
        raise ValueError(f"No images found in directory: {image_dir}")

    print(f"Converting {len(image_paths)} images to .npy format...")

    for image_path in tqdm(image_paths, desc="Processing Images"):
        # Read image using OpenCV
        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        
        if image is None:
            print(f"Warning: Unable to load image {image_path}. Skipping...")
            continue
        
        # Determine the number of channels
        if len(image.shape) == 2:
            # Single-channel image (grayscale or RAW)
            image = image[:, :, np.newaxis]  # Add channel dimension
        elif len(image.shape) == 3 and image.shape[2] == 3:
            # Convert BGR to RGB for standard 3-channel images
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif len(image.shape) == 3 and image.shape[2] == 4:
            # 4-channel image (e.g., RGGB pattern)
            pass  # No conversion needed
        else:
            print(f"Warning: Unexpected number of channels in image {image_path}. Skipping...")
            continue

        raw_img = image.astype(np.float32)

        raw_max = raw_img.max()
        

        normalized_img = (raw_img / raw_max).astype(np.float32)

        # Save the image as a .npy file
        npy_filename = output_dir / f"{image_path.stem}.npy"
        np.save(npy_filename, normalized_img)

    print(f"Conversion complete! Images saved in {output_dir}")

# convert_images_to_npy(image_dir, output_dir)

# Challenge train_raw dataset
import numpy as np
from pathlib import Path
from glob import glob
from tqdm import tqdm
def normalize_image(img_array):
    """
    Normalize image array similar to NPZ conversion method
    
    :param img_array: Input NumPy array
    :return: Normalized image array
    """
    # Convert to float32
    raw_img = img_array.astype(np.float32)
    
    # Find the max value for normalization
    raw_max = raw_img.max()
    
    # Normalize by dividing by max value
    normalized_img = (raw_img / raw_max).astype(np.float32)
    
    return normalized_img

def extract_images_and_keywords(csv_file, output_folder):
    """
    Extract images, convert to normalized NumPy arrays, and save keywords.
    
    :param csv_file: Path to the input CSV file
    :param output_folder: Folder to save extracted images and labels
    """
    # Create output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)
    
    # Path for the labels file
    labels_file_path = os.path.join(output_folder, 'labels.txt')
    
    # Open labels file in write mode
    with open(csv_file, 'r', encoding='utf-8') as input_file, \
         open(labels_file_path, 'w', encoding='utf-8') as labels_file:
        
        csv_reader = csv.DictReader(input_file)
        
        # Process each row in the CSV
        for row in csv_reader:
            # Extract file identifier and keywords
            file_id = row['File']
            keywords = row['Keywords']
            
            # NEF file URL (or TIFF if preferred)
            image_url = row['NEF']
            
            # Skip if no URL or keywords
            if not image_url or not keywords:
                continue
            
            try:
                # Download the image file
                response = requests.get(image_url)
                
                # Ensure successful download
                if response.status_code == 200:
                    # Open image from bytes
                    with Image.open(io.BytesIO(response.content)) as img:
                        # Convert image to NumPy array
                        img_array = np.array(img)
                        
                        # Normalize the image
                        img_normalized = normalize_image(img_array)
                        
                        # Construct NPY filename
                        npy_filename = f"{file_id}.npy"
                        npy_path = os.path.join(output_folder, 'images', npy_filename)
                        
                        # Save normalized NumPy array
                        np.save(npy_path, img_normalized)
                    
                    # Write image filename and its keywords to labels file
                    labels_file.write(f"{npy_filename}: {keywords}\n")
                    
                    print(f"Processed: {npy_filename}")
                
            except Exception as e:
                print(f"Error processing {file_id}: {e}")


# Example usage:
# convert_npz_to_npy("/home/paperspace/Documents/nika_space/npz_raw/train_raw", "train_raw_challenge_npy")

#RAISE dataset
import csv
import os
import requests
import io
from PIL import Image

def normalize_image(img_array):
    """
    Normalize image array by dividing by its maximum value
    
    :param img_array: Input NumPy array
    :return: Normalized image array
    """
    # Convert to float32
    raw_img = img_array.astype(np.float32)
    
    # Find the max value for normalization
    raw_max = raw_img.max()
    
    # Normalize by dividing by max value
    normalized_img = (raw_img / raw_max).astype(np.float32)
    
    return normalized_img


def extract_images_and_keywords(csv_file, output_folder):
    """
    Extract images, convert to normalized NumPy arrays, and save keywords.
    
    :param csv_file: Path to the input CSV file
    :param output_folder: Folder to save extracted images and labels
    """
    # Create output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)
    
    # Path for the labels file
    labels_file_path = os.path.join(output_folder, 'labels.txt')
    
    # Open labels file in write mode
    with open(csv_file, 'r', encoding='utf-8') as input_file, \
         open(labels_file_path, 'w', encoding='utf-8') as labels_file:
        
        csv_reader = csv.DictReader(input_file)
        
        # Process each row in the CSV
        for row in csv_reader:
            # Extract file identifier and keywords
            file_id = row['File']
            keywords = row['Keywords']
            
            # NEF file URL (or TIFF if preferred)
            image_url = row['NEF']
            
            # Skip if no URL or keywords
            if not image_url or not keywords:
                continue
            
            try:
                # Download the image file
                response = requests.get(image_url)
                
                # Ensure successful download
                if response.status_code == 200:
                    # Open image from bytes
                    with Image.open(io.BytesIO(response.content)) as img:
                        # Convert image to NumPy array
                        img_array = np.array(img)
                        
                        # Normalize the image
                        img_normalized = normalize_image(img_array)
                        
                        # Construct NPY filename
                        npy_filename = f"{file_id}.npy"
                        npy_path = os.path.join(output_folder, 'images', npy_filename)
                        
                        # Save normalized NumPy array
                        np.save(npy_path, img_normalized)
                    
                    # Write image filename and its keywords to labels file
                    labels_file.write(f"{npy_filename} {keywords}\n")
                    
                    print(f"Processed: {npy_filename}")
                
            except Exception as e:
                print(f"Error processing {file_id}: {e}")


csv_file_path = 'RAISE_383.csv'
output_folder = '/home/paperspace/Documents/nika_space/main_dataset/raise/'
extract_images_and_keywords(csv_file_path, output_folder)

# Additional notes:
# 1. This script requires the 'requests' library. Install it using:
#    pip install requests
# 2. Ensure you have permission to download and use these images
# 3. Replace 'your_metadata.csv' with the actual path to your CSV file