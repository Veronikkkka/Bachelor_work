import os
import glob
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from torchvision.models import ResNet50_Weights
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
# model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)


data_dir = "raw"
image_paths = glob.glob(os.path.join(data_dir, "*.TIF"))
print(image_paths)
preprocess = transforms.Compose([
    transforms.Resize((224, 224)), 
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


from torchvision import models
model = models.resnet50(weights=ResNet50_Weights.DEFAULT)


model.eval()


embeddings = []
for image_path in image_paths:
    print(image_path)
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        input_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        embedding = model(input_tensor)
        embeddings.append(embedding.squeeze(0).numpy())


print(f"Extracted {len(embeddings)} embeddings from the dataset!")

for i, embedding in enumerate(embeddings):
    print(f"Embedding {i+1}: {embedding}")

embeddings = np.array(embeddings)
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
reduced_embeddings = tsne.fit_transform(embeddings)

# pca = PCA(n_components=50)
# reduced_embeddings = TSNE(n_components=2, random_state=42).fit_transform(pca.fit_transform(embeddings))

plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], s=5, alpha=0.7)
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.grid()
plt.show()