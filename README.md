# Bachelor_work

This worked is done based on dinov2, so main code is in this submodule

## aded files: 

congigs/train/custom.yaml

data/datasets/augmentation_rggb.py new
data/datasets/knn_for_main.py
data/datasets/main_dataset.py
data/datasets/my_dataset.py
data/datasets/npz_raw.py
data/datasets/pre_process_in_advance.py
data/datasets/pre_processor.py
data/datasets/raise_dataset.py
data/datasets/raw_nod.py

eval/segmentation1.py
eval/segmentation2.py

models/help.py
models/input_level_adapter.py

train/rgb_to_raw.py
train/knn.py
train/segmentation_head.py

## changed files:

configs/eval/vitb14_pretrain.yaml

data/transforms.py
data/augmentations.py
data/loaders.py

eval/linear.py

eval/utils.py


models/vision_transformer.py

train/ssl_meta_arch.py
train/train.py
