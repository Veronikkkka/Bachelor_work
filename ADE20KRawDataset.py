from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from torch.utils.data import DataLoader

class ADE20KRawDataset(Dataset):
    def __init__(self, data_dir, mode='training', transform=None):
        """
        """
        self.data_dir = Path(data_dir)
        self.mode = mode
        self.transform = transform
        self.image_paths = self._load_image_paths()
    
    def _load_image_paths(self):
        """
        Load paths for synthetic RAW images in the dataset
        """
        if self.mode == 'training':
            subdirs = ['training_raw', 'training_raw_low', 'training_raw_over_exp']
        elif self.mode == 'validation':
            subdirs = ['validation_raw', 'validation_raw_low', 'validation_raw_over_exp']

        image_paths = []
        for subdir in subdirs:
            image_dir = self.data_dir / 'images' / subdir
            image_paths.extend(image_dir.glob('*.*'))

        return sorted(image_paths)
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        """
        Get image and label
        """
        image_path = self.image_paths[idx]
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        return {'image': image, 'path': str(image_path)}


data_dir = "/home/nika/Documents/Bahelor/ADE20K_raw/ADE20K/ADEChallengeData2016"


transform = transforms.Compose([
    transforms.Resize((256, 256)),  # resize
    transforms.ToTensor(),
])

dataset = ADE20KRawDataset(data_dir, mode='training', transform=transform)
print(len(dataset))
print(dataset.image_paths[:10])

validation_dataset = ADE20KRawDataset(data_dir, mode='validation', transform=transform)
print(len(validation_dataset))
print(validation_dataset.image_paths[:10])

# from torch.utils.data import random_split

# train_size = int(0.7 * len(dataset))
# val_size = int(0.15 * len(dataset))
# eval_size = len(dataset) - train_size - val_size

# train_dataset, val_dataset, eval_dataset = random_split(dataset, [train_size, val_size, eval_size])
# print(len(train_dataset))
# print(len(val_dataset))
# print(len(eval_dataset))


train_loader = DataLoader(dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(validation_dataset, batch_size=16, shuffle=False)




# Example
for batch in train_loader:
    images = batch['image']
    paths = batch['path']
    
    print(f"Batch size: {images.size()}")
    print(f"Sample paths: {paths[:3]}")
    
    import matplotlib.pyplot as plt
    plt.imshow(images[0].permute(1, 2, 0))
    plt.title(paths[0])
    plt.axis('off')
    plt.show()
    break