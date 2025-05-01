import os
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm
import rawpy
# ADE 20K dataset


image_dir = "/home/paperspace/Documents/nika_space/ADE20K/ADEChallengeData2016/images/training_raw_low/"  # Update with the correct path
output_dir = "/home/paperspace/Documents/nika_space/main_dataset/ade/images"  # Output directory for .npy files

import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm



def convert_rgb_to_bayer_4channel(rgb_image):
    """
    Convert an RGB image to a simulated Bayer RGGB pattern with 4 separate channels.
    
    Returns:
        (H, W, 4) NumPy array with [R, G1, G2, B] channels.
    """
    h, w = rgb_image.shape[:2]
    

    bayer = np.zeros((h, w, 4), dtype=np.uint8)
    

    bayer[0::2, 0::2, 0] = rgb_image[0::2, 0::2, 0]  # R
    bayer[0::2, 1::2, 1] = rgb_image[0::2, 1::2, 1]  # G1
    bayer[1::2, 0::2, 2] = rgb_image[1::2, 0::2, 1]  # G2
    bayer[1::2, 1::2, 3] = rgb_image[1::2, 1::2, 2]  # B
    
    return bayer

def convert_ade_to_bayer_npy(input_folder, output_folder, keep_original=True):
    """
    Convert ADE20K dataset images to simulated Bayer pattern and save as .npy files
    
    Args:
        input_folder: Path to folder containing ADE20K images
        output_folder: Path to save processed files
        keep_original: If True, also save the original RGB data
    """

    os.makedirs(output_folder, exist_ok=True)

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.jpg')]
    
    print(f"Found {len(image_files)} images to process.")

    for image_file in tqdm(image_files, desc="Converting ADE20K images"):
        input_path = os.path.join(input_folder, image_file)
        

        base_name = os.path.splitext(image_file)[0]
        
        try:

            original_img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            
            if original_img is None:
                print(f"Warning: Could not read image {image_file}")
                continue

            bayer_img = convert_rgb_to_bayer_4channel(original_img)
            
            output_path = os.path.join(output_folder, f"{base_name}.npy")
            np.save(output_path, bayer_img)
                
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    print(f"All images converted and saved to {output_folder}")
# convert_ade_to_bayer_npy(image_dir, output_dir, keep_original=False)

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
    raw_img = img_array.astype(np.float32)
    raw_max = raw_img.max()

    normalized_img = (raw_img / raw_max).astype(np.float32)
    
    return normalized_img

def extract_images_and_keywords(csv_file, output_folder):
    """
    Extract images, convert to normalized NumPy arrays, and save keywords.
    
    :param csv_file: Path to the input CSV file
    :param output_folder: Folder to save extracted images and labels
    """

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)

    labels_file_path = os.path.join(output_folder, 'labels.txt')

    with open(csv_file, 'r', encoding='utf-8') as input_file, \
         open(labels_file_path, 'w', encoding='utf-8') as labels_file:
        
        csv_reader = csv.DictReader(input_file)

        for row in csv_reader:
 
            file_id = row['File']
            keywords = row['Keywords']
 
            image_url = row['NEF']
            

            if not image_url or not keywords:
                continue
            
            try:

                response = requests.get(image_url)
                

                if response.status_code == 200:
 
                    with Image.open(io.BytesIO(response.content)) as img:

                        img_array = np.array(img)

                        img_normalized = normalize_image(img_array)

                        npy_filename = f"{file_id}.npy"
                        npy_path = os.path.join(output_folder, 'images', npy_filename)

                        np.save(npy_path, img_normalized)

                    labels_file.write(f"{npy_filename}: {keywords}\n")
                    
                    print(f"Processed: {npy_filename}")
                
            except Exception as e:
                print(f"Error processing {file_id}: {e}")



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

    raw_img = img_array.astype(np.float32)
    
    raw_max = raw_img.max()
    
    normalized_img = (raw_img / raw_max).astype(np.float32)
    
    return normalized_img



import os
import csv
import io
import requests
import rawpy
import numpy as np
from tqdm import tqdm

def extract_images_and_keywords2(csv_file, output_folder):
    """
    Extract NEF images, convert to RGGB NumPy arrays (4, H, W), and save keywords.

    :param csv_file: Path to the input CSV file
    :param output_folder: Folder to save extracted images and labels
    """
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)

    labels_file_path = os.path.join(output_folder, 'labels.txt')

    with open(csv_file, 'r', encoding='utf-8') as input_file, \
         open(labels_file_path, 'w', encoding='utf-8') as labels_file:

        csv_reader = csv.DictReader(input_file)

        for row in tqdm(csv_reader, desc="Loading"):
            file_id = row['File']
            keywords = row['Keywords']
            image_url = row['NEF']

            if not image_url or not keywords:
                continue

            try:
                response = requests.get(image_url)

                if response.status_code == 200:
                    with rawpy.imread(io.BytesIO(response.content)) as raw:
                        raw_image = raw.raw_image_visible.copy()
                        raw_image = raw_image.astype(np.uint16)

                        height, width = raw_image.shape
                        rggb_image = np.zeros((height // 2, width // 2, 4), dtype=np.uint16)


                        rggb_image[:, :, 0] = raw_image[0::2, 0::2]  # Red
                        rggb_image[:, :, 1] = raw_image[0::2, 1::2]  # Green (first)
                        rggb_image[:, :, 2] = raw_image[1::2, 0::2]  # Green (second)
                        rggb_image[:, :, 3] = raw_image[1::2, 1::2]  # Blue

                        # (4, H, W)
                        rggb_image = np.transpose(rggb_image, (2, 0, 1))

                        npy_filename = f"{file_id}.npy"
                        npy_path = os.path.join(output_folder, 'images', npy_filename)
                        np.save(npy_path, rggb_image)

                    labels_file.write(f"{npy_filename} {keywords}\n")
                    print(f"Processed: {npy_filename}")

            except Exception as e:
                print(f"Error processing {file_id}: {e}")



# csv_file_path = 'RAISE_383.csv'
# output_folder = '/home/paperspace/Documents/nika_space/main_dataset/raise/'
# extract_images_and_keywords(csv_file_path, output_folder)


csv_file_path = 'RAISE_383.csv'
output_folder = '/home/paperspace/Documents/nika_space/main_dataset/raise/'
extract_images_and_keywords2(csv_file_path, output_folder)