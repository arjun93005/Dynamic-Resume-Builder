from server.app import app

def test_upload_security_headers():
    client = app.test_client()
    response = client.get("/")
    assert "X-Content-Type-Options" in response.headers
    assert "Strict-Transport-Security" in response.headers

def test_temp_cleanup(tmp_path):
    import os, time
    from server.services.storage_local import cleanup_old_files
    old_file = tmp_path / "old.txt"
    old_file.write_text("old data")
    os.utime(old_file, (time.time() - 400, time.time() - 400))
    cleanup_old_files(tmp_path, age_limit_minutes=1)
    assert not old_file.exists()
