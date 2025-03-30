import numpy as np
from PIL import Image

def save_npy_as_image(npy_file, output_file="output.png"):
    """
    Loads an image from a .npy file and saves it as a PNG.

    Args:
        npy_file (str): Path to the .npy file.
        output_file (str): Path where the image will be saved.
    """
    # Load the image
    image = np.load(npy_file)

    # # Normalize if needed (scale to 0-255 for uint8 format)
    # if image.dtype != np.uint8:
    #     image = (image - image.min()) / (image.max() - image.min()) * 255
    #     image = image.astype(np.uint8)

    # Convert to PIL Image
    if len(image.shape) == 2:  # Grayscale
        img = Image.fromarray(image, mode="L")
    else:  # RGB
        img = Image.fromarray(image)

    img.save(output_file)
#     print(f"Image saved as {output_file}")

# # Example usage
npy_file = "/home/paperspace/Documents/nika_space/main_dataset/ade/images/ADE_train_00000683.npy"  # Change path as needed
# save_npy_as_image(npy_file, "visualized_image.png")

import numpy as np
import matplotlib.pyplot as plt
import argparse
def visualize_npy_image(npy_path):
    """Load and visualize an .npy image file explicitly."""
    img = np.load(npy_path)

    print(f"Image shape: {img.shape}, dtype: {img.dtype}, min: {img.min()}, max: {img.max()}")

    # If grayscale, show in cmap='gray'
    if img.ndim == 2 or (img.ndim == 3 and img.shape[-1] == 1):
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(img)  # Assume RGB

    plt.axis("off")
    plt.show()


import torch
def raw_to_rgb(raw_path, normalize: bool = True) -> Image.Image:

    raw_input = np.load(raw_path)
    if isinstance(raw_input, torch.Tensor):
        raw_np = raw_input.detach().cpu().numpy()
    else:
        raw_np = raw_input

    if raw_np.ndim == 3 and raw_np.shape[0] == 1:
        raw_np = raw_np[0]

    if normalize:
        raw_np = (raw_np - raw_np.min()) / (raw_np.max() - raw_np.min() + 1e-8) * 255.0
        raw_np = raw_np.astype(np.uint8)

    rgb_image = cv2.cvtColor(raw_np, cv2.COLOR_GRAY2RGB)

    return Image.fromarray(rgb_image)


import numpy as np
import cv2
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Visualize an .npy image file")
#     parser.add_argument("npy_path", type=str, help="Path to the .npy image file")
    
#     args = parser.parse_args()
#     visualize_npy_image(args.npy_path)

import numpy as np
from PIL import Image
import torch

def save_image_from_npy(npy_file, save_path):
    """
    Loads an image tensor from a .npy file, converts it to a PIL image, 
    and saves it to a file.

    Args:
        npy_file (str): Path to the .npy file containing the image tensor.
        save_path (str): Path where the image will be saved.
    """
    
    img_tensor = np.load(npy_file)

    print(img_tensor)

    img_tensor = torch.from_numpy(img_tensor)

    # (C, H, W)
    if img_tensor.dim() == 3:
        img_tensor = img_tensor.unsqueeze(0) 

    # (H, W, C)
    img_pil = Image.fromarray((img_tensor.squeeze().permute(1, 2, 0).numpy()).astype(np.uint8))


    if img_pil.mode == 'RGBA':
        img_pil = img_pil.convert('RGB')

    img_pil.save(save_path)
    print(f"Image saved as {save_path}")

# Example usage:
# save_image_from_npy(npy_file, 'output_image.png')

import numpy as np
from PIL import Image
import os
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm

def raw_to_rgb(raw_data):
    
    if raw_data.shape[0] != 4 and raw_data.shape[2] == 4:
        raw_data = np.transpose(raw_data, (2, 0, 1))
    

    _, h, w = raw_data.shape
    

    rgb_image = np.zeros((h*2, w*2, 3), dtype=np.float32)
    

    r_channel = raw_data[0]  
    g1_channel = raw_data[1]
    g2_channel = raw_data[2]
    b_channel = raw_data[3]
    

    def normalize_channel(channel):
        min_val = channel.min()
        max_val = channel.max()
        if max_val > min_val:
            return (channel - min_val) / (max_val - min_val)
        return channel
    
    r_channel = normalize_channel(r_channel)
    g1_channel = normalize_channel(g1_channel)
    g2_channel = normalize_channel(g2_channel)
    b_channel = normalize_channel(b_channel)
    

    rgb_image[0::2, 0::2, 0] = r_channel 
    rgb_image[0::2, 1::2, 1] = g1_channel
    rgb_image[1::2, 0::2, 1] = g2_channel
    rgb_image[1::2, 1::2, 2] = b_channel

    rgb_image = (rgb_image * 255).astype(np.uint8)
    
    return rgb_image

def demosaic(raw_image):
    h, w, _ = raw_image.shape
    rgb_image = np.copy(raw_image).astype(np.float32)
    
   
    for i in range(h):
        for j in range(w):
            if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1):
                count = 0
                total = 0
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w and ni % 2 == 0 and nj % 2 == 0:
                        total += rgb_image[ni, nj, 0]
                        count += 1
                
                if count > 0:
                    rgb_image[i, j, 0] = total / count
    

    for i in range(h):
        for j in range(w):
            if not ((i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0)):
                count = 0
                total = 0
                for di, dj in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w:
                        if (ni % 2 == 0 and nj % 2 == 1) or (ni % 2 == 1 and nj % 2 == 0):
                            total += rgb_image[ni, nj, 1]
                            count += 1
                
                if count > 0:
                    rgb_image[i, j, 1] = total / count
    

    for i in range(h):
        for j in range(w):
            if not (i % 2 == 1 and j % 2 == 1):  
                count = 0
                total = 0
                for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w and ni % 2 == 1 and nj % 2 == 1:
                        total += rgb_image[ni, nj, 2]
                        count += 1
                
                if count > 0:
                    rgb_image[i, j, 2] = total / count
    
    return np.clip(rgb_image, 0, 255).astype(np.uint8)

def process_npy_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    npy_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.npy')]
    
    for npy_file in tqdm(npy_files, desc="Converting RAW to RGB"):

        input_path = os.path.join(input_dir, npy_file)
        raw_data = np.load(input_path)
        
        print(f"Loaded RAW data with shape: {raw_data.shape}")
        
 
        rgb_image = raw_to_rgb(raw_data)
        

        output_base = os.path.splitext(npy_file)[0]
        bayer_output_path = os.path.join(output_dir, f"{output_base}_bayer.png")
        Image.fromarray(rgb_image).save(bayer_output_path)
        print(f"Saved Bayer pattern image to: {bayer_output_path}")
        

        demosaiced = demosaic(rgb_image)
        

        demosaic_output_path = os.path.join(output_dir, f"{output_base}_rgb.png")
        Image.fromarray(demosaiced).save(demosaic_output_path)
        print(f"Saved demosaiced RGB image to: {demosaic_output_path}")

def process_single_npy(input_path):
    raw_data = np.load(input_path)
    # print(raw_data.shape)
    
    rgb_image = raw_to_rgb(raw_data)
    
    file_base = os.path.splitext(os.path.basename(input_path))[0]
    

    bayer_output_path = f"{file_base}_bayer.png"
    Image.fromarray(rgb_image).save(bayer_output_path)
     
    demosaiced = demosaic(rgb_image)

    demosaic_output_path = f"{file_base}_rgb.png"
    Image.fromarray(demosaiced).save(demosaic_output_path)
    print(demosaic_output_path)
    


if __name__ == "__main__":

    # input_dir = "/path/to/your/npy/files"
    # output_dir = "/path/to/save/rgb/images"
    # process_npy_files(input_dir, output_dir)
    
    input_path = "/home/paperspace/Documents/nika_space/main_dataset/ade/images/ADE_train_00000683.npy"
    output_dir = ""
    process_single_npy(input_path, output_dir)
