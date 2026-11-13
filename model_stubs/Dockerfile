FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY model_stubs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model_stubs ./model_stubs

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "model_stubs.main:app", "--host", "0.0.0.0", "--port", "8000"]
