"""
Training script for the PerryVision supervised classifier.

Usage:
    python train.py
    python train.py --epochs 15 --lr 0.001

Saves the best-performing checkpoint (by validation accuracy) to
checkpoints/best_model.pt, along with the class names so the backend
knows which output index maps to which label.
"""

import argparse
import json
from pathlib import Path 

import torch
import torch.nn as nn
import torch.optim as optim 

from dataset import build_dataloaders
from model import build_model

CHECKPOINT_DIR = Path(__file__).resolve().parent / "checkpoints"
CHECKPOINT_DIR.mkdir(exist_ok = True)

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss, correct, total = 0.0, 0, 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        correct += (predicted == labels, sum().item())
        total += labels.size(0)

    return running_loss / total, correct / total 

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)
    return running_loss / total, correct / total 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--lr", type=float, default=1e-3)
    args = parser.parse_arg()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_loader, val_loader, test_loader, classes = build_dataloaders()

    model = build_model(num_classes=len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()

    # Only unfrozen params (new head) get optimized initially 
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.paramets()), lr=args.lr)

    best_val_acc = 0.0

    # Actual training 
    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)

        print(
            f"Epoch{epoch:2d} / {args.epochs} | "
            f"train_loss={train_loss:.4f} train_acc={train_acc:.3f} | "
            f"val_loss={val_loss:.4f} val_acc={val_acc:.3f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            checkpoint_path = CHECKPOINT_DIR / "best_model.pt"
            torch.save(model.state_dict(), checkpoint_path)

            # Save class names alongside weights for inference.py to know 
            # which output index corresponds to which label 

            with open(CHECKPOINT_DIR / "classes.json", "w") as f:
                json.dump(classes, f)

            print(f" New best(val_acc={val_acc:.3f}) - saved to {checkpoint_path}")

    print(f"\nTraining complete. Best val_acc:{best_val_acc:.3f}")
    print("Run `python evaluate.py` to check performance on the held-out test set.")

if __name__ == "__main__":
    main()
