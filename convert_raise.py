import os
import csv
import requests
import io
import numpy as np
import random
import torch
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm


def value_encode(value, max_val, min_val):
    return (value-min_val)/(max_val-min_val)

def value_decode(value, max_val, min_val):
    return value*(max_val-min_val)+min_val

def apply_ccm(image, ccm):
    '''
    The function of apply CCM matrix
    '''
    shape = image.shape
    image = image.view(image.shape[0], -1, 3)
    image = torch.tensordot(image, ccm, dims=[[-1], [-1]])
    return image.view(shape)

def mosaic(img):
    """Extracts RGGB Bayer planes from an RGB image."""
    shape = img.shape
    
    red = img[:, 0::2, 0::2, 0]
    green_red = img[:, 0::2, 1::2, 1]
    green_blue = img[:, 1::2, 0::2, 1]
    blue = img[:, 1::2, 1::2, 2]
    
    raw = torch.stack([red, green_red, green_blue, blue], dim=-1)
    raw = torch.reshape(raw, (img.shape[0], img.shape[1]//2, img.shape[2]//2, 4))
    
    return raw


xyz2cams = [[[1.0234, -0.2969, -0.2266],
              [-0.5625, 1.6328, -0.0469],
              [-0.0703, 0.2188, 0.6406]],
            [[0.4913, -0.0541, -0.0202],
              [-0.613, 1.3513, 0.2906],
              [-0.1564, 0.2151, 0.7183]],
            [[0.838, -0.263, -0.0639],
              [-0.2887, 1.0725, 0.2496],
              [-0.0627, 0.1427, 0.5438]],
            [[0.6596, -0.2079, -0.0562],
              [-0.4782, 1.3016, 0.1933],
              [-0.097, 0.1581, 0.5181]]]
rgb2xyz = [[0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041]]

def Unprocess(img):
    """Convert an RGB image to RAW Bayer format with the same processing as your original code"""
    img1 = img.permute(0,2,3,1) # (B, H, W, C)

    img1 = 0.5 - torch.sin(torch.asin(1.0 - 2.0 * img1) / 3.0)
    

    epsilon = torch.FloatTensor([1e-8]).to(img.device)
    gamma = random.uniform(2.0, 3.5)
    img2 = torch.max(img1, epsilon) ** gamma
    

    xyz2cam = random.choice(xyz2cams)
    rgb2cam = np.matmul(xyz2cam, rgb2xyz)
    rgb2cam = torch.from_numpy(rgb2cam / np.sum(rgb2cam, axis=-1)).to(torch.float).to(img.device)
    img3 = apply_ccm(img2, rgb2cam)
    

    img4 = mosaic(img3).permute(0,3,1,2)
    
    return img4

def load_image_from_url(image_url, device='cpu'):
    """
    Load an image from a URL and convert it to a tensor in the correct format
    
    Args:
        image_url: URL of the image to download
        device: Device to put the tensor on (default: 'cpu')
        
    Returns:
        Tensor of shape [1, 3, H, W]
    """

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    image = Image.open(io.BytesIO(response.content)).convert('RGB')

    width, height = image.size
    if width % 2 != 0:
        width += 1
    if height % 2 != 0:
        height += 1
    image = image.resize((width, height))

    image_array = np.array(image, dtype=np.float32) / 255.0 
    image_tensor = torch.tensor(image_array, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
    
    return image_tensor.to(device)

def extract_images_and_keywords(csv_file, output_folder, device='cpu'):
    """
    Extract images, convert to RAW Bayer format, and save keywords.
    
    Args:
        csv_file: Path to the input CSV file
        output_folder: Folder to save extracted images and labels
        device: Device to use for processing (default: 'cpu')
    """

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)

    labels_file_path = os.path.join(output_folder, 'labels.txt')
    

    with open(csv_file, 'r', encoding='utf-8') as count_file:
        total_rows = sum(1 for _ in csv.DictReader(count_file))
    

    with open(csv_file, 'r', encoding='utf-8') as input_file, \
         open(labels_file_path, 'w', encoding='utf-8') as labels_file:
        
        csv_reader = csv.DictReader(input_file)
        

        for row in tqdm(csv_reader, total=total_rows, desc="Processing images"):

            file_id = row['File']
            keywords = row['Keywords']
            

            image_url = row['NEF']

            if not image_url or not keywords:
                print(f"Skipping {file_id}: Missing URL or keywords")
                continue
            
            try:

                img_tensor = load_image_from_url(image_url, device)

                # print(f"Original image min: {img_tensor.min().item()}, max: {img_tensor.max().item()}")

                img_raw = Unprocess(img_tensor)

                # print(f"Processed RAW min: {img_raw.min().item()}, max: {img_raw.max().item()}")

                npy_filename = f"{file_id}.npy"
                npy_path = os.path.join(output_folder, 'images', npy_filename)

                np.save(npy_path, img_raw.squeeze().cpu().numpy())
                

                labels_file.write(f"{npy_filename} {keywords}\n")
                
                
            except Exception as e:
                print(f"Error processing {file_id}: {str(e)}")
                continue

def test_conversion(image_url, output_path=None, device='cpu'):
    """
    Test the conversion process on a single image and visualize the results
    
    Args:
        image_url: URL of the image to test
        output_path: Path to save the output (optional)
        device: Device to use for processing
    """
    try:
        print(f"Loading image from {image_url}")
        img_tensor = load_image_from_url(image_url, device)
        
        print(f"Original image shape: {img_tensor.shape}")
        print(f"Original image min: {img_tensor.min().item()}, max: {img_tensor.max().item()}")

        img_raw = Unprocess(img_tensor)
        
        print(f"RAW Bayer format shape: {img_raw.shape}")
        print(f"RAW Bayer format min: {img_raw.min().item()}, max: {img_raw.max().item()}")
        

        img_raw_np = img_raw.squeeze().cpu().numpy()

        if output_path:
            np.save(output_path, img_raw_np)
            print(f"Saved RAW Bayer data to {output_path}")

        plt.figure(figsize=(16, 8))
        

        plt.subplot(1, 5, 1)
        plt.title("Original Image")
        plt.imshow(img_tensor.squeeze().permute(1, 2, 0).cpu().numpy())

        channel_names = ["R Channel", "G1 Channel", "G2 Channel", "B Channel"]
        for i in range(4):
            plt.subplot(1, 5, i+2)
            plt.title(channel_names[i])

            channel = img_raw_np[i]
            if channel.max() > channel.min():
                channel = (channel - channel.min()) / (channel.max() - channel.min())
            plt.imshow(channel, cmap='gray')
        
        plt.tight_layout()
        plt.show()
        
        return img_raw_np
        
    except Exception as e:
        print(f"Error in test conversion: {str(e)}")
        return None

if __name__ == "__main__":

    csv_file = "RAISE_383.csv"
    output_folder = "raise_npy"

    extract_images_and_keywords(csv_file, output_folder)
    