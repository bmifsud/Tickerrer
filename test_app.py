import pytest
from fastapi.testclient import TestClient
import os
import downloader
from main import app

client = TestClient(app)

def setup_function():
    # Reset stored_data.json and chart.png before tests
    if os.path.exists(downloader.DATA_FILE):
        os.remove(downloader.DATA_FILE)
    if os.path.exists("chart.png"):
        os.remove("chart.png")

def test_get_empty_data():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json() == []

def test_post_and_get_data():
    sample_data = [
        {"date": "2026-01-01", "price": 100},
        {"date": "2026-01-02", "price": 105}
    ]
    post_resp = client.post("/api/data", json=sample_data)
    assert post_resp.status_code == 200
    assert post_resp.json() == {"message": "Data saved successfully"}

    get_resp = client.get("/api/data")
    assert get_resp.status_code == 200
    assert get_resp.json() == sample_data

def test_get_chart_endpoint():
    sample_data = [
        {"date": "2026-01-01", "price": 100},
        {"date": "2026-01-02", "price": 105}
    ]
    client.post("/api/data", json=sample_data)

    chart_resp = client.get("/api/chart")
    assert chart_resp.status_code == 200
    assert chart_resp.headers["content-type"] == "image/png"
    assert len(chart_resp.content) > 0
