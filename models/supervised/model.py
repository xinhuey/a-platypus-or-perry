"""
Model definition for the PerryVision classifier.

Uses transfer learning on a pretrained ResNet18: the convolutional base
(trained on ImageNet) is frozen, and only a new binary classification head
is trained. This is what makes a small dataset (a few hundred images)
workable — the model isn't learning to see from scratch, just learning to
map already-good visual features to your two classes.
"""

import torch
import torch.nn as nn
from torchvision import models

def build_model(num_classes: int = 2, freeze_base: bool = True) -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

    if freeze_base:
        for param in model.parameters():
            param.requires_grad = False

    # Replace the final fully-connected layer with a fresh head for our
    # two classes. This new layer is trainable even when the base is frozen

    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    return model 

def unfreeze_last_block(model: nn.Module) -> nn.Module:
    """
    Optional fine-tuning step: unfreeze the last residual block (layer4)
    so it can adapt slightly to the specified images, once the new head has already 
    learned something reasonable. Call this after a few epochs of training with 
    everything else frozen, then continue training with a smaller learning rate
    """

    for param in model.layer4.parameters():
        param.requires_grad = True

    return model

if __name__ == "__main__":
    model = build_model()
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Trainable parametes: {trainable:,} / {total:,}")

    
    