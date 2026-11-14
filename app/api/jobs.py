from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.job import Job, ModelResult
from app.services.modality import detect_modality
from app.services.pipeline import process_job

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


def get_db():
    with SessionLocal() as db:
        yield db


@router.post("", status_code=202)
async def create_job(
    background_tasks: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)],
    files: Annotated[list[UploadFile], File()],
) -> dict:
    max_bytes = settings.max_upload_mb * 1024 * 1024
    prepared = []
    for upload in files:
        filename = upload.filename or "upload"
        modality = detect_modality(filename, upload.content_type)
        if modality is None:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {filename}")
        data = await upload.read()
        if len(data) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"File too large (max {settings.max_upload_mb} MB): {filename}",
            )
        prepared.append({"filename": filename, "modality": modality, "data": data})

    job = Job(
        files=[
            {"filename": f["filename"], "modality": f["modality"], "size_bytes": len(f["data"])}
            for f in prepared
        ]
    )
    db.add(job)
    db.commit()
    background_tasks.add_task(process_job, job.id, prepared)
    return {"job_id": job.id, "status": job.status}


@router.get("")
def list_jobs(db: Annotated[Session, Depends(get_db)], limit: int = 10) -> list[dict]:
    jobs = db.scalars(select(Job).order_by(Job.created_at.desc()).limit(min(limit, 50))).all()
    return [
        {
            "job_id": job.id,
            "status": job.status,
            "files": [f["filename"] for f in job.files],
            "verdict": (job.ensemble or {}).get("verdict"),
            "confidence": (job.ensemble or {}).get("confidence"),
            "created_at": job.created_at.isoformat(),
        }
        for job in jobs
    ]


@router.get("/{job_id}")
def get_job(job_id: str, db: Annotated[Session, Depends(get_db)]) -> dict:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "error": job.error,
        "files": job.files,
    }


@router.get("/{job_id}/result")
def get_result(job_id: str, db: Annotated[Session, Depends(get_db)]) -> dict:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status not in ("done", "failed"):
        raise HTTPException(status_code=409, detail="Job is not finished yet")
    rows = db.scalars(
        select(ModelResult).where(ModelResult.job_id == job_id).order_by(ModelResult.id)
    ).all()
    return {
        "job_id": job.id,
        "status": job.status,
        "error": job.error,
        "simulated": True,
        "files": job.files,
        "model_results": [
            {
                "filename": r.filename,
                "model_name": r.model_name,
                "model_version": r.model_version,
                "modality": r.modality,
                "label": r.label,
                "score": r.score,
                "weight": r.weight,
                "processing_time_ms": r.processing_time_ms,
            }
            for r in rows
        ],
        "ensemble": job.ensemble,
    }
