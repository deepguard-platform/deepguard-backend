def test_frontend_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "DeepGuard" in response.text
