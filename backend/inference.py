"""
Loads the trained supervised model and runs prediction on a single image 

Reuses model.py and dataset.py from models/supervised/ directly, rather than 
duplicating the architecture or transform definitions 


"""

import json 
import sys 
from pathlib import Path 

import torch 
from PIL import Image 

# Make models/supervised/importable 
SUPERVISED_DIR = Path(__file__).resolve().parents[1] / "models" / "supervised"
sys.path.insert(0, str(SUPERVISED_DIR))

from model import build_model
from dataset import eval_transforms 

CHECKPOINT_DIR = SUPERVISED_DIR / "checkpoints"
CHECKPOINT_PATH = CHECKPOINT_DIR / "best_model.pt"
CLASSES_PATH = CHECKPOINT_DIR / "classes.json"

# Maps the dataset's folder-derived class names to the verdict vocabulary 
# the frontend expects (agent/ ordinary)
VERDICT_MAP = {
    "perry" : "agent",
    "platypus": "ordinary",
}

FIELD_NOTES = {
    "agent":(
        "PERRY THE PLATYPUS ??!!??"
    ),
    "ordinary":(
        "Relax, Dr Doof. It's just a platypus."
    ),
}

GIF_MAP = {
    "agent": "/gifs/agent-result.gif",
    "ordinary": "/gifs/ordinary-playtypus.gif",
}

class Classifier:
    """ 
    Loads checkpoint once at startup and reuses it for every request
    rather than reloading the model from disk on every prediction 
    """

    def __init__(self):
        if not CHECKPOINT_PATH.exists():
            raise FileNotFoundError(
                f"No trained model found at {CHECKPOINT_PATH}."
                f"Run train.py in models/supervised/ first."
            )
        with open(CLASSES_PATH) as f:
            self.classes = json.load(f)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = build_model(num_classes= len(self.classes))
        self.model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def predict(self, image: Image.Image) -> dict:
        image = image.convert("RGB")
        tensor = eval_transforms(image).unsqueeze(0).to(self.device)

        outputs = self.model(tensor)
        probabilities = torch.softmax(outputs, dim = 1)[0]
        confidence, predicted_idx = torch.max(probabilities, dim = 0)

        class_name = self.classes[predicted_idx_item()] # perry or platypus
        verdict = VERDICT_MAP[class_name]

        label = (
            "PERRY THE PLATYPUS! "
            if verdict == "agent"
            else "Relax. Just a platypus. They don't do much"
        )

        return {
            "verdict": verdict, 
            "confidence": round(confidence.item(), 4),
            "label": label,
            "fieldNotes" : FIELD_NOTES[verdict],
            "gifSrc": GIF_MAP[verdict],
        }

# Loaded once when this module is imported 
classifier = Classifier()