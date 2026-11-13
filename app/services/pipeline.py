import requests

from app.db.session import SessionLocal
from app.models.job import Job, ModelResult
from app.services.ensemble import run_ensemble
from app.services.registry import model_url, models_for

REQUEST_TIMEOUT_SECONDS = 60


def call_model(model: dict, filename: str, data: bytes) -> dict:
    """Send one file to one model service and return its JSON answer."""
    response = requests.post(
        f"{model_url(model)}/predict",
        files={"file": (filename, data)},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def process_job(job_id: str, files: list[dict]) -> None:
    """Runs in the background: queued -> processing -> done (or failed)."""
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        try:
            job.status = "processing"
            job.progress = 5
            db.commit()

            tasks = [(f, m) for f in files for m in models_for(f["modality"])]
            results = []
            for index, (f, model) in enumerate(tasks, start=1):
                try:
                    answer = call_model(model, f["filename"], f["data"])
                except requests.RequestException:
                    answer = None
                if answer is not None:
                    db.add(
                        ModelResult(
                            job_id=job_id,
                            filename=f["filename"],
                            model_name=answer["model_name"],
                            model_version=answer["model_version"],
                            modality=answer["modality"],
                            label=answer["label"],
                            score=answer["score"],
                            weight=model["weight"],
                            processing_time_ms=answer["processing_time_ms"],
                        )
                    )
                    results.append(
                        {
                            "model_name": answer["model_name"],
                            "score": answer["score"],
                            "weight": model["weight"],
                        }
                    )
                job.progress = 5 + int(90 * index / len(tasks))
                db.commit()

            if results:
                job.ensemble = run_ensemble(results)
                job.status = "done"
            else:
                job.status = "failed"
                job.error = "No model service answered"
            job.progress = 100
            db.commit()
        except Exception as exc:
            db.rollback()
            job.status = "failed"
            job.error = f"Processing error: {exc}"[:500]
            job.progress = 100
            db.commit()
