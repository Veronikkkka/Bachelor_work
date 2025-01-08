import os
import rawpy
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class MITAdobeFiveKDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        """
        self.root_dir = root_dir
        self.file_names = [f for f in os.listdir(root_dir) if f.endswith('.dng')]
        self.transform = transform

    def __len__(self):
        return len(self.file_names)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir, self.file_names[idx])
        
        # Load the DNG image using rawpy
        with rawpy.imread(img_name) as raw:
            rgb_image = raw.postprocess()

        # Convert to PIL Image for compatibility with torchvision transforms
        pil_image = Image.fromarray(rgb_image)
        
        if self.transform:
            pil_image = self.transform(pil_image)

        return pil_image


transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),  
])


dataset = MITAdobeFiveKDataset(root_dir='/home/nika/Documents/Bahelor/fivek_dataset/raw_photos/HQa1to700/photos', transform=transform)

dataloader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=4)

# for batch in dataloader:
#     print(batch.shape)


# sample = dataset[0]
# print(sample.shape)

import matplotlib.pyplot as plt
import random

def plot_random_images(dataset, num_images=5):
    fig, axes = plt.subplots(1, num_images, figsize=(15, 5))
    for i in range(num_images):
        idx = random.randint(0, len(dataset) - 1)
        image = dataset[idx]
        image = image.permute(1, 2, 0).numpy()
        image = np.clip(image, 0, 1) 
        axes[i].imshow(image)
        axes[i].axis('off')
    plt.show()
plot_random_images(dataset)