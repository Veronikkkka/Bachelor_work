import os
import json
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

from collections import defaultdict



LABEL_FILES = [
    "/home/paperspace/Documents/nika_space/main_dataset/labels.txt",

]
OUTPUT_JSON = "label_mapping.json"
DISTANCE_THRESHOLD = 0.1 


all_labels = set()
for file in LABEL_FILES:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            label = " ".join(parts[1:])
            all_labels.add(label)

all_labels = sorted(list(all_labels))
print(f"Loaded {len(all_labels)} unique labels.")


model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(all_labels, normalize_embeddings=True)


clustering = AgglomerativeClustering(
    n_clusters=None,
    distance_threshold=DISTANCE_THRESHOLD,
    metric="cosine",
    linkage="average"
)
clusters = clustering.fit_predict(embeddings)

cluster_map = defaultdict(list)
for idx, cluster_id in enumerate(clusters):
    cluster_map[cluster_id].append(all_labels[idx])

label_mapping = {}
for cluster_labels in cluster_map.values():
    canonical = cluster_labels[0]
    for lbl in cluster_labels:
        label_mapping[lbl] = canonical


with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(label_mapping, f, indent=2)

print(f"Saved mapping for {len(label_mapping)} labels to '{OUTPUT_JSON}'")
