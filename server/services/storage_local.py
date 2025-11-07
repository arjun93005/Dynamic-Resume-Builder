import os
import time


def ensure_upload_dir(folder="uploads"):
    os.makedirs(folder, exist_ok=True)
    return folder


def save_file(file, report_id, folder="uploads"):
    ensure_upload_dir(folder)
    ext = os.path.splitext(file.filename)[1] or ".bin"
    path = os.path.join(folder, f"{report_id}{ext}")
    file.save(path)
    return path


def cleanup_old_files(folder="uploads", hours=12):
    if not os.path.exists(folder):
        return
    now = time.time()
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.getmtime(path) < now - hours * 3600:
            os.remove(path)
