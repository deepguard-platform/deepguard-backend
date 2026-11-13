import os
import subprocess
import sys

STUBS = [
    ("video-model-a", "video", 8001),
    ("video-model-b", "video", 8002),
    ("audio-model-a", "audio", 8003),
    ("text-model-a", "text", 8004),
]

processes = []
for name, modality, port in STUBS:
    env = {**os.environ, "MODEL_NAME": name, "MODALITY": modality}
    command = [sys.executable, "-m", "uvicorn", "model_stubs.main:app", "--port", str(port)]
    processes.append(subprocess.Popen(command, env=env))

try:
    for process in processes:
        process.wait()
except KeyboardInterrupt:
    for process in processes:
        process.terminate()
