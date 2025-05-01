# Bachelor_work

This worked is done based on dinov2, so main code is in this submodule. Also, as described in paper, the idea of input-level adapter, model-level adapter and merge blocks are taken from RAW Adapter and modified.


## added files: 

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

## Data

program expect to image in RGGB format in npy .file, and to the following dataset structure:  dataset - split(train, val, test) - dataset_name - images - npy files

## Commands
for train encoder:
python3 -m dinov2.train.train --config-file dinov2/configs/train/custom.yaml --output-dir lala3


for running linear classifier:
python3 -m dinov2.eval.linear --config-file /home/paperspace/Documents/nika_space/dinov2/dinov2/configs/eval/vitb14_pretrain.yaml  --pretrained-weights /home/paperspace/Documents/nika_space/dinov2/lala3/model_0010499.rank_0.pth  --output-dir /home/paperspace/Documents/nika_space/dinov2/lalaa3/

for running segmentation:
CUDA_LAUNCH_BLOCKING=1 python3 -m dinov2.eval.segmentation2 --train-dataset "Seg:root=/home/paperspace/Documents/nika_space/ADE20K/ADEChallengeData2016:split=train" --val-dataset "Seg:root=/home/paperspace/Documents/nika_space/ADE20K/ADEChallengeData2016:split=val"  --pretrained-weights /home/paperspace/Documents/nika_space/dinov2/basic/model_0008999.rank_0.pth  --config-file /home/paperspace/Documents/nika_space/dinov2/dinov2/configs/eval/vitb14_pretrain.yaml --output-dir seg_on_basic


