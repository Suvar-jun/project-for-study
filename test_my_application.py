from fastapi.testclient import TestClient

from application import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_calc_salary_zero_hours():
    response = client.get("/calc_salary", params={"hours": 0})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "За сегодня вы заработали 0 рублей."


def test_calc_salary_missing_hours():
    response = client.get("/calc_salary")  # hours обязателен
    assert response.status_code == 422  # Validation Error от FastAPI

def test_calc_salary_normal_case():
    response = client.get("/calc_salary", params={"hours": 8})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "За сегодня вы заработали 8000 рублей."





