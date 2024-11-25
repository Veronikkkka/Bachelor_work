import os
import csv
import requests

download_folder = os.path.expanduser("~/Downloads/raw")
os.makedirs(download_folder, exist_ok=True)


file_path = "RAISE_1.csv"
count = 0

with open(file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if count > 100:
            break
        image_url = row.get("TIFF")
        if image_url:
            try:
                filename = os.path.basename(image_url)
                output_path = os.path.join(download_folder, filename)
                
                print("download:", filename)
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                
                with open(output_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                # print("Saved", output_path)
                count += 1
            except Exception as e:
                print(f"Failed to download {image_url}: {e}")
