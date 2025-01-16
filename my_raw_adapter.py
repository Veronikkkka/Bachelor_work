import torch
import torch.nn as nn
from torch.nn import functional as F
from typing import Optional

class RawAdapter(nn.Module):
    def __init__(self, dim: int, dropout: float = 0.1, init_scale: float = 1e-3):
        super().__init__()
        self.down = nn.Linear(dim, dim // 8)
        self.up = nn.Linear(dim // 8, dim)
        self.layer_norm = nn.LayerNorm(dim)
        self.dropout = nn.Dropout(dropout)
        
        nn.init.normal_(self.down.weight, std=init_scale)
        nn.init.normal_(self.up.weight, std=init_scale)
        nn.init.zeros_(self.down.bias)
        nn.init.zeros_(self.up.bias)

    def forward(self, x):
        residual = x
        x = self.layer_norm(x)
        x = self.down(x)
        x = F.gelu(x)
        x = self.up(x)
        x = self.dropout(x)
        x = residual + x
        return x

class ModifiedAttentionBlock(nn.Module):
    def __init__(self, original_block, dim: int):
        super().__init__()
        self.original_block = original_block
        self.adapter = RawAdapter(dim)
        
        for param in self.original_block.parameters():
            param.requires_grad = False

    def forward(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        x = self.original_block(x, **kwargs)
        x = self.adapter(x)
        return x

def add_adapters_to_dinov2(model):
    """
    Add raw adapters to a pretrained DINOv2 model after each attention block.
    """
    model.requires_grad_(False)
    
    for block in model.blocks:
        dim = block.attn.qkv.in_features
        block.attn = ModifiedAttentionBlock(block.attn, dim)
    
    return model


def prepare_adapted_model(pretrained_model):
    """
    Prepare a DINOv2 model with adapters for fine-tuning.
    """
    model = add_adapters_to_dinov2(pretrained_model)
    
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"Total parameters: {total_params:,}")
    
    return model