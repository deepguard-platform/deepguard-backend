import asyncio
import hashlib
import os
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

MODALITY = os.getenv("MODALITY", "video")
MODEL_NAME = os.getenv("MODEL_NAME", f"{MODALITY}-model-a")
MODEL_VERSION = os.getenv("MODEL_VERSION", "0.1-demo")

app = FastAPI(title=f"Stub model: {MODEL_NAME}")


def simulated_score(data: bytes, filename: str) -> float:
    digest = hashlib.sha256(MODEL_NAME.encode() + data).digest()
    fraction = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
    name = filename.lower()
    if "fake" in name:
        return round(0.70 + 0.28 * fraction, 4)
    if "real" in name:
        return round(0.02 + 0.28 * fraction, 4)
    return round(fraction, 4)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "modality": MODALITY,
    }


@app.post("/predict")
async def predict(file: Annotated[UploadFile, File()]) -> dict:
    delay = float(os.getenv("DELAY_SECONDS", "2"))
    data = await file.read()
    await asyncio.sleep(delay)
    score = simulated_score(data, file.filename or "")
    return {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "modality": MODALITY,
        "label": "fake" if score >= 0.5 else "real",
        "score": score,
        "processing_time_ms": int(delay * 1000),
        "details": {"simulated": True},
    }
