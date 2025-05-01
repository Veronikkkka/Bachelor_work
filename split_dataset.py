import os
import shutil
import random
from pathlib import Path

def split_dataset_randomly(
    root,
    output_dir=None,
    split_ratios=(0.8, 0.1, 0.1),
    seed=42,
    verbose=True
):
    """
    Randomly split dataset into train/val/test folders with subfolder structure preserved.

    Args:
        root (str): Path to the root dataset directory with subfolders (e.g., 'ade', 'raise').
        output_dir (str): Where to save the split folders. Defaults to root.
        split_ratios (tuple): Ratios for (train, val, test), must sum to 1.
        seed (int): Random seed for reproducibility.
        verbose (bool): Whether to print progress.
    """
    assert sum(split_ratios) == 1.0, "Split ratios must sum to 1"
    random.seed(seed)
    
    root = Path(root)
    output_dir = Path(output_dir or root)

    splits = ['train', 'val', 'test']
    split_ratio_map = dict(zip(splits, split_ratios))

    for subfolder in sorted(os.listdir(root)):
        print("subfolder: ", subfolder)
        if subfolder != "challenge":
            continue
        class_folder = root / subfolder
        images_folder = class_folder / "images"
        if not images_folder.exists():
            continue

        image_files = list(images_folder.glob("*.npy"))
        random.shuffle(image_files)

        n_total = len(image_files)
        n_train = int(n_total * split_ratio_map['train'])
        n_val   = int(n_total * split_ratio_map['val'])
        n_test  = n_total - n_train - n_val

        split_files = {
            'train': image_files[:n_train],
            'val':   image_files[n_train:n_train+n_val],
            'test':  image_files[n_train+n_val:]
        }

        for split_name, files in split_files.items():
            target_dir = output_dir / split_name / subfolder / "images"
            os.makedirs(target_dir, exist_ok=True)

            for file_path in files:
                shutil.copy(file_path, target_dir / file_path.name)

            if verbose:
                print(f"{split_name.upper():<5} - {subfolder:<10}: {len(files)} files → {target_dir}")

    print("Dataset split completed successfully")

# split_dataset_randomly("/home/paperspace/Documents/nika_space/main_dataset")
def merge_two_labels(file1, file2, output_file="labels_all.txt"):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    combined = lines1 + lines2

    with open(output_file, 'w', encoding='utf-8') as out:
        out.writelines(combined)

    print(f"Merged {len(lines1)} + {len(lines2)} = {len(combined)} lines into: {output_file}")



merge_two_labels("/home/paperspace/Documents/nika_space/main_dataset/ade/labels.txt", "/home/paperspace/Documents/nika_space/main_dataset/raise/labels.txt")

