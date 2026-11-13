def test_unknown_job_returns_404(client):
    response = client.get("/api/v1/jobs/does-not-exist")
    assert response.status_code == 404


def test_unsupported_file_type_is_rejected(client):
    response = client.post(
        "/api/v1/jobs",
        files=[("files", ("notes.pdf", b"%PDF-1.4", "application/pdf"))],
    )
    assert response.status_code == 400
