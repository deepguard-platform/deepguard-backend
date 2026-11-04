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
