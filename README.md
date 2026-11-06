## Local setup
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash). On Linux/Mac: source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Useful commands
```bash
ruff check .            # lint
ruff format .           # format code
pytest                  # run tests
pre-commit run --all-files
```


## Run with Docker
```bash
cp .env.example .env        # then set a password in .env (letters and numbers only)
docker compose up --build
```
- API docs (Swagger): http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness (checks PostgreSQL and Redis): http://localhost:8000/health/ready

Stop with `docker compose down` (add `-v` only if you want to delete the database data).
