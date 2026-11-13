from fastapi.testclient import TestClient

from model_stubs.main import app

client = TestClient(app)


def predict(filename, monkeypatch):
    monkeypatch.setenv("DELAY_SECONDS", "0")
    return client.post("/predict", files={"file": (filename, b"abc", "video/mp4")})


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_fake_filename_gives_high_score(monkeypatch):
    body = predict("fake_clip.mp4", monkeypatch).json()
    assert body["label"] == "fake"
    assert body["score"] >= 0.7


def test_real_filename_gives_low_score(monkeypatch):
    body = predict("real_clip.mp4", monkeypatch).json()
    assert body["label"] == "real"
    assert body["score"] <= 0.3


def test_same_file_gives_same_score(monkeypatch):
    first = predict("clip.mp4", monkeypatch).json()["score"]
    second = predict("clip.mp4", monkeypatch).json()["score"]
    assert first == second
