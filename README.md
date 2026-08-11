# A Platypus? Perry the Platypus???

**Is that Perry, or just a platypus?**

A fine-grained binary image classifier that does what Dr. Doofenshmirtz never could: readily tell apart _Perry the Platypus_ from an ordinary, non-secret-agent platypus. Upload a picture, get an instant verdict. Dr Doof will definitely appreciate this!

Built as a hands-on learning project to compare **supervised**, **unsupervised**, and **reinforcement learning** approaches to the exact same classification problem.

## 🎯 User Manual for Dr Doof

1. **Upload** a picture.
2. **Classify** — a trained model predicts whether the image shows Perry the Platypus or just a regular platypus.
3. **React** — the result is paired with a corresponding GIF that verifies if it is Perry or not!

## 🧠 Why this project exists

This repo isn't just a novelty classifier — it's a sandbox for understanding how different machine learning paradigms tackle the _same_ problem:

| Approach                   | Role in this project                                                                                    | What it teaches                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Supervised Learning**    | Primary model — fine-tuned CNN trained on labeled images                                                | Standard classification workflow: labeled data → loss minimization                          |
| **Unsupervised Learning**  | Side experiment — clusters image embeddings without labels                                              | Whether the two classes are naturally separable in feature space                            |
| **Reinforcement Learning** | Side experiment — framed as a contextual bandit (image = context, label = action, correctness = reward) | How reward-driven learning differs from loss-driven learning on a single-shot decision task |

The supervised model is the one that actually powers the app; the other two exist for comparison and learning purposes.

## 🛠️ Tech stack

- **Model:** PyTorch (transfer learning from a pretrained CNN, e.g. MobileNetV2 or ResNet18)
- **Backend:** FastAPI / Flask serving predictions
- **Frontend:** Next.jd
- **Data handling:** Pillow, NumPy, scikit-learn (for the clustering experiment)

## 🚀 Getting started

```bash
# Clone the repo
git clone https://github.com/<your-username>/perryvision.git
cd perryvision

# Install dependencies
pip install -r requirements.txt

# Train the supervised model
python train.py --model supervised

# Run the backend
uvicorn backend.app:app --reload


## ⚠️ Disclaimer

This is a fan-made, educational project not affiliated with or endorsed by Disney. Perry the Platypus is the property of Disney. This project is intended for personal learning purposes.
```
