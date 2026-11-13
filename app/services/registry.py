from app.core.config import settings

MODELS = [
    {"name": "video-model-a", "modality": "video", "weight": 0.6, "local_port": 8001},
    {"name": "video-model-b", "modality": "video", "weight": 0.4, "local_port": 8002},
    {"name": "audio-model-a", "modality": "audio", "weight": 1.0, "local_port": 8003},
    {"name": "text-model-a", "modality": "text", "weight": 1.0, "local_port": 8004},
]


def models_for(modality: str) -> list[dict]:
    return [m for m in MODELS if m["modality"] == modality]


def model_url(model: dict) -> str:
    if settings.model_url_mode == "docker":
        return f"http://{model['name']}:8000"
    return f"http://localhost:{model['local_port']}"
