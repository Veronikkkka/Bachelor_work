import zipfile
import rawpy
import numpy as np
import os
import io
from tqdm import tqdm

def extract_and_save_rggb_from_zip(zip_path, output_folder):
    """
    Extract NEF images from zip, convert to RGGB NumPy arrays (4, H, W), and save.

    :param zip_path: Path to the .zip file containing NEF images
    :param output_folder: Output folder to store images and labels.txt
    """
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'images'), exist_ok=True)

    labels_file_path = os.path.join(output_folder, 'labels.txt')

    with zipfile.ZipFile(zip_path, 'r') as archive, \
         open(labels_file_path, 'w', encoding='utf-8') as labels_file:

        nef_files = [f for f in archive.namelist() if f.lower().endswith('.nef')]

        for file_name in tqdm(nef_files, desc="Processing"):
            try:
                with archive.open(file_name) as nef_file:
                    raw_data = nef_file.read()
                    with rawpy.imread(io.BytesIO(raw_data)) as raw:
                        raw_image = raw.raw_image_visible.astype(np.uint16)
                        height, width = raw_image.shape

                        black_level = np.array(raw.black_level_per_channel).reshape((2, 2))
                        corrected = raw_image.astype(np.int32).copy()
                        corrected[0::2, 0::2] -= black_level[0, 0]  # R
                        corrected[0::2, 1::2] -= black_level[0, 1]  # G1
                        corrected[1::2, 0::2] -= black_level[1, 0]  # G2
                        corrected[1::2, 1::2] -= black_level[1, 1]  # B
                        corrected = np.clip(corrected, 0, None).astype(np.uint16)

                        # Convert to RGGB (4, H, W)
                        rggb_image = np.zeros((height // 2, width // 2, 4), dtype=np.uint16)
                        rggb_image[:, :, 0] = corrected[0::2, 0::2]  # Red
                        rggb_image[:, :, 1] = corrected[0::2, 1::2]  # Green (top)
                        rggb_image[:, :, 2] = corrected[1::2, 0::2]  # Green (bottom)
                        rggb_image[:, :, 3] = corrected[1::2, 1::2]  # Blue
                        rggb_image = np.transpose(rggb_image, (2, 0, 1))  # (4, H, W)

                        base_name = os.path.basename(file_name)
                        name_wo_ext = os.path.splitext(base_name)[0]
                        npy_filename = f"{name_wo_ext}.npy"
                        npy_path = os.path.join(output_folder, 'images', npy_filename)
                        np.save(npy_path, rggb_image)


                        labels_file.write(f"{npy_filename}\n")


            except Exception as e:
                print(f"Error processing {file_name}: {e}")



extract_and_save_rggb_from_zip('/home/paperspace/Documents/nika_space/Nikon.zip', '/home/paperspace/Documents/nika_space/main_dataset/raw_nod/')

