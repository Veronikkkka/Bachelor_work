# Bachelor_work

This worked is done based on dinov2, so main code is in this submodule


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


@misc{oquab2023dinov2,
  title={DINOv2: Learning Robust Visual Features without Supervision},
  author={Oquab, Maxime and Darcet, Timothée and Moutakanni, Theo and Vo, Huy V. and Szafraniec, Marc and Khalidov, Vasil and Fernandez, Pierre and Haziza, Daniel and Massa, Francisco and El-Nouby, Alaaeldin and Howes, Russell and Huang, Po-Yao and Xu, Hu and Sharma, Vasu and Li, Shang-Wen and Galuba, Wojciech and Rabbat, Mike and Assran, Mido and Ballas, Nicolas and Synnaeve, Gabriel and Misra, Ishan and Jegou, Herve and Mairal, Julien and Labatut, Patrick and Joulin, Armand and Bojanowski, Piotr},
  journal={arXiv:2304.07193},
  year={2023}
}
