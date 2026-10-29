from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analysis_not_found():
    response = client.get(
        "/api/analysis/non-existent-session"
    )

    assert response.status_code == 404


def test_invalid_analyze_request():
    response = client.post(
        "/api/analyze",
        json={
            "user_query": "",
            "dataset_id": "invalid.csv",
        },
    )

    assert response.status_code == 422