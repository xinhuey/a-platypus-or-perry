"""
Evaluates the trained model on the held-out test split 

Usage:
    python evaluate.py

Requires a checkpoint at checkpoints/best_model.pt(produced by train.py)
Prints accuracy, precision/recall/F1 per class, and a confusion matrix

"""

import json 
from pathlib import Path 

import torch 
from sklearn.metrics import classification_report, confusion_matrix

from dataset import build_dataloaders
from model import build_model

CHECKPOINT_DIR = Path(__file__).resolve().parent / "checkpoints"

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    checkpoint_path = CHECKPOINT_DIR / "best_model.pt"
    classes_path = CHECKPOINT_DIR / "classes.json"

    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"No checkpoint found at {checkpoint_path}. Run train.py first"
        )

    with open(classes_path) as f:
        classes = json.load(f)

    _, _, test_loader, _ = build_dataloaders()

    model = build_model(num_classes=len(classes)).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()

    all_preds, all_labels = [], []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().tolist())
            all_labels.extend(labels.tolist())

    print(f"Classes: {classes}\n")
    print("Classification report:")
    print(classification_report(all_labels, all_preds, target_names=classes))

    print("Confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(all_labels, all_preds))


if __name__ == "__main__":
    main()