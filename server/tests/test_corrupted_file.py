import io
import pytest
from server.app import app

def test_corrupted_pdf_upload(monkeypatch):
    client = app.test_client()

    # simulate a bad file that parser will fail to read
    bad_file = io.BytesIO(b"%PDF- corrupted-content")
    data = {"file": (bad_file, "bad_resume.pdf")}
    response = client.post("/api/resume/analyze",
                           data=data, content_type="multipart/form-data")

    assert response.status_code == 422
    data = response.get_json()
    assert "corrupted" in data["details"].lower()

def test_empty_txt(monkeypatch, tmp_path):
    client = app.test_client()
    empty_file = io.BytesIO(b"")
    data = {"file": (empty_file, "empty.txt")}
    response = client.post("/api/resume/analyze",
                           data=data, content_type="multipart/form-data")

    assert response.status_code == 422
    assert "empty" in response.get_json()["details"].lower()
