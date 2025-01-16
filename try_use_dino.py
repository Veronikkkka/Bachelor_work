import sys
sys.path.append('external/dinov2')

# from argparse import Namespace
# from dinov2.models import build_model
# import torch

# args = Namespace(
#     arch='dinov2_vitb14',         # Correct architecture name
#     patch_size=14,                # Patch size for ViT-B/14
#     img_size=224,                 # Input image size
#     layerscale=True,              # Whether to use layerscale
#     ffn_layer='swiglu',           # Feedforward network layer type
#     block_chunks=1,               # Number of block chunks for model efficiency
#     qkv_bias=True,
#     ffn_bias=True,
#     proj_bias=True,               # Whether to use bias in projection layers
#     interpolate_offset=True,      # Whether to use interpolation for offsets
#     interpolate_antialias=True,
#     num_register_tokens=1
# )
# dino_model = build_model(args)
# dino_model.eval()
# # Optionally, load from a specific checkpoint
# checkpoint = torch.load('path/to/checkpoint.pth', map_location='cpu')
# dino_model.load_state_dict(checkpoint['model'], strict=True)

# dinov2_vits14 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14')


from torch.hub import load_state_dict_from_url
import torch
from my_raw_adapter import prepare_adapted_model
# Load pretrained DINOv2 model
dinov2_model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14')

# Add adapters and prepare for fine-tuning
adapted_model = prepare_adapted_model(dinov2_model)