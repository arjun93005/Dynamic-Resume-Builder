import os, time

def ensure_upload_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_file(file, upload_dir):
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)
    return file_path

def cleanup_old_files(directory, age_limit_minutes=5):
    now = time.time()
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if os.path.isfile(path) and now - os.path.getmtime(path) > age_limit_minutes * 60:
            os.remove(path)
