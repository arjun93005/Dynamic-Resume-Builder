import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import io
import json

from server.app import app


def test_api_upload(monkeypatch, tmp_path):
    client = app.test_client()
    data = {"file": (io.BytesIO(b"test content"), "x.txt")}
    r = client.post(
        "/api/resume/analyze", data=data, content_type="multipart/form-data"
    )
    assert r.status_code == 200
    rid = json.loads(r.data)["reportId"]
    res = client.get(f"/api/resume/result/{rid}")
    assert res.status_code == 200
