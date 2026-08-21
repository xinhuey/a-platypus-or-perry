"""
FastAPI backend serving the PerryVision classifier.

Run with:
    uvicorn app:app --reload --port 8000

Exposes:
    POST /classify   — accepts an uploaded image, returns a ClassificationResult
    GET  /health      — basic liveness check
"""

from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from inference import classifier

app = FastAPI(title="PerryVision API")

# Allows Next.js server to call this API directly from browser

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://127.0.0.1:3000",
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", 
            "classes": classifier.classes
            }

@app.post("/classify")
async def classify(image: UploadFile = File(...)):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    raw_bytes = await image.read()

    try:
        pil_image = Image.open(BytesIO(raw_bytes))
        pil_image.load()
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="File could not be read as an image.")

    result = classifier.predict(pil_image)
    return result 