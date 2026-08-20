"""
FastAPI backend serving the PerryVision classifier.

Run with:
    uvicorn app:app --reload --port 8000

Exposes:
    POST /classify   — accepts an uploaded image, returns a ClassificationResult
    GET  /health      — basic liveness check
"""