"""
Data loading, splitting, and augmentation for the PerryVision classifier.

Expects images laid out as:

    data/
      platypus/   (ordinary platypus — no agent uniform)
        img_001.jpg
        ...
      perry/      (Agent P — in uniform)
        img_001.jpg
        ...

No manual train/val/test split is required — this script splits the
combined dataset randomly at load time, so you can just keep dropping
new images into the two class folders as you collect them.

Big picture:
1. Hand train.py clean, ready-to-use DataLoader objects (train/val/test)

"""

import os
from pathlib import Path

import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

# Config
DATA_DIR = Path(__file__).resolve().parents[2]/"data"
IMAGE_SIZE = 224
BATCH_SIZE = 16
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
SEED = 42

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Transforms 
# Training gets augementation to fight overfitting on a small dataset
# Val/test stays deterministic so evaluation numbers are stable 

train_transforms = transforms.Compose([
    transforms.Resize((256, 256))
    transforms.RandomCrop(IMAGE_SIZE),
    transforms.RandomHorizontalFlip(p = 0.5),
    transforms.RandomRotation(degrees = 15),
    transforms.ColorJitter(brightness=0.2, contrast = 0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),

])

eval_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
])

class TransformSubset(torch.utils.data.Dataset):
    """Wraps a Subset so a different transform can be applied than the one
    baked into the parent ImageFolder dataset (needed because train/val/test
    need different transforms but random_split shares the underlying data)."""

    def __init__(self, subset, transform):
        self.subset = subset
        self.transform = transform

    def __len__(self):
        return len(self.subset)

    def __getitem__(self, idx):
        image, label = self.subset[idx]
        if self.transform:
            image = self.transform(image)

        return image, label

def build_dataloaders():
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Expected a data/directory at {DATA_DIR} with platypus/ and"
            f"perry/ subfolders. see README for dataset setup."
        )
    # Load with no transform yet
    full_dataset = datasets.ImageFolder(root=str(DATA_DIR), transform = None)

    if len(full_dataset) == 0 :
        raise ValueError(
            f"No images found in {DATA_DIR}. Add images to data/platypus "
            f" and data/perry/ before training"
        )
    print(f"Classes found: {full_dataset.classes}")
    print(f"Total images: {len(full_dataset)}")

    n_total = len(full_dataset)
    n_val = max(1, int(n_total * VAL_SPLIT))
    n_test = max(1, int(n_total * TEST_SPLIT))
    n_train = n_total - n_val - n_test

    generator = torch.Generator().manual_seed(SEED)
    train_subset, val_subset, test_subset = random_split(
        full_dataset, [n_train, n_val, n_test], generator=generator
    )

    train_ds = TransformSubset(train_subset, train_transforms)
    val_ds = TransformSubset(val_subset, eval_transforms)
    test_ds = TransformSubset(test_subset, eval_transforms)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    print(f"Split sizes - train: {n_train}, val:{n_val}, test:{n_test}")

    return train_loader, val_loader, test_loader, full_dataset.classes

if __name__ == "__main__":
    train_loader, val_loader, test_loader, classes = build_dataloaders()
    images, labels = next(iter(train_loader))
    print(f"Batch shape: {images.shape}, labels:{labels}")
