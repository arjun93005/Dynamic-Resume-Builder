import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import hashlib
import uuid

import werkzeug

if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "3.0"

from flask import Flask, jsonify, request
from flask_cors import CORS

from server.services.parser import extract_text
from server.services.storage_local import ensure_upload_dir, save_file

# Config
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "uploads")
MAX_FILE_BYTES = int(os.environ.get("MAX_FILE_BYTES", 5 * 1024 * 1024))  # 5 MB
ensure_upload_dir(UPLOAD_DIR)

app = Flask(__name__)
# CORS: allow local dev origin(s). In production restrict this.
CORS(
    app,
    resources={
        r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}
    },
)

REPORTS = {}


def sha256sum(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


@app.route("/api/resume/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "file" not in request.files:
            return (
                jsonify({"error": "no file part (multipart/form-data required)"}),
                400,
            )
        f = request.files["file"]
        if f.filename == "":
            return jsonify({"error": "empty filename"}), 400

        # quick size check via content-length header if present
        content_length = request.content_length or 0
        if content_length and content_length > MAX_FILE_BYTES:
            return jsonify({"error": "file too large (content-length)"}), 413

        # save file
        report_id = str(uuid.uuid4())
        saved_path = save_file(f, report_id, UPLOAD_DIR)

        actual_size = os.path.getsize(saved_path)
        if actual_size > MAX_FILE_BYTES:
            os.remove(saved_path)
            return (
                jsonify(
                    {
                        "error": "file too large (after save)",
                        "max_bytes": MAX_FILE_BYTES,
                    }
                ),
                413,
            )

        # extract text
        try:
            text = extract_text(saved_path)
        except Exception as e:
            # keep the saved file for debugging; return a friendly error
            return jsonify({"error": "parsing_failed", "message": str(e)}), 400

        checksum = sha256sum(saved_path)
        report = {
            "id": report_id,
            "filename": f.filename,
            "size_bytes": actual_size,
            "checksum_sha256": checksum,
            "text_snippet": text[:2000],
            "status": "done",
        }
        REPORTS[report_id] = report
        return jsonify({"reportId": report_id, "checksum": checksum}), 200

    except Exception as e:
        return jsonify({"error": "internal_server_error", "message": str(e)}), 500


@app.route("/api/resume/result/<report_id>", methods=["GET"])
def get_result(report_id):
    r = REPORTS.get(report_id)
    if not r:
        return jsonify({"error": "not_found"}), 404
    return jsonify(r)


if __name__ == "__main__":
    # Bind to 0.0.0.0 so local hostnames (127.0.0.1) or network interfaces can reach it.
    app.run(debug=True, host="0.0.0.0", port=5000)
