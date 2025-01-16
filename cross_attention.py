import torch.nn as nn
import torch.nn.functional as F
import math


class CrossAttentionConditioner(nn.Module):
    def __init__(self, dino_dim, raw_dim):
        super().__init__()
        
        self.raw_proj = nn.Linear(raw_dim, dino_dim)
    
        self.q = nn.Linear(dino_dim, dino_dim)
        self.k = nn.Linear(dino_dim, dino_dim)
        self.v = nn.Linear(dino_dim, dino_dim)
        
    def forward(self, dino_feat, raw_feat):
        raw_feat = self.raw_proj(raw_feat)
        
        q = self.q(dino_feat)
        k = self.k(raw_feat)
        v = self.v(raw_feat)
       
        attn = (q @ k.transpose(-2, -1)) / math.sqrt(q.size(-1))
        attn = F.softmax(attn, dim=-1)
        
        output = attn @ v
        
        return dino_feat + output
