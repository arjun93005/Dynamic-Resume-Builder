import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import os
import uuid
from typing import Dict, Any
from flask import Flask, jsonify, request
from flask_cors import CORS

import werkzeug
# 🧩 Fix for Werkzeug 3.x not having __version__ — needed for Flask test client
if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "3.0.0"

from server.services.parser import extract_text
from server.services.storage_local import ensure_upload_dir, save_file, cleanup_old_files
from server.services.section_extractor import extract_sections
from server.services.pdf_exporter import export_to_pdf
from server.services.section_extractor import extract_sections, detect_missing_sections
from server.services.score_calculator import compute_resume_score

# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
ensure_upload_dir(UPLOAD_DIR)

_RESULTS: Dict[str, Dict[str, Any]] = {}

# -----------------------------------------------------------------------------
@app.after_request
def apply_security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    resp.headers["X-Frame-Options"] = "DENY"
    return resp


@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok"}), 200


@app.route("/api/resume/analyze", methods=["POST"])
def analyze_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    ensure_upload_dir(UPLOAD_DIR)
    file_path = save_file(file, UPLOAD_DIR)

    # --- ✅ New corruption-safe extraction ---
    try:
        resume_text = extract_text(file_path)
        if not resume_text.strip():
            raise ValueError("Empty or unreadable file content")
    except (ValueError, Exception) as e:
        return jsonify({
            "error": "File could not be processed",
            "details": str(e)
        }), 422

    # Continue normal flow only if extraction successful
    try:
        extracted_sections = extract_sections(resume_text)
        missing_sections = detect_missing_sections(extracted_sections)
        char_count = len(resume_text)
        word_count = len([w for w in resume_text.split() if w.strip()])

        metadata = {
            "filename": file.filename,
            "file_type": os.path.splitext(file.filename)[1].replace(".", "").upper() or "UNKNOWN",
            "character_count": char_count,
            "word_count": word_count,
        }

        score_result = compute_resume_score(extracted_sections, metadata)

        report_id = uuid.uuid4().hex
        _RESULTS[report_id] = {
            "filename": file.filename,
            "status": "done",
            "sections": extracted_sections,
            "metadata": metadata,
            "score": score_result,
            "missing_sections": missing_sections,
        }

        cleanup_old_files(UPLOAD_DIR)

        return jsonify({
            "reportId": report_id,
            "filename": file.filename,
            "sections": extracted_sections,
            "metadata": metadata,
            "score": score_result,
            "missing_sections": missing_sections
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@app.route("/api/resume/result/<report_id>", methods=["GET"])
def get_result(report_id: str):
    result = _RESULTS.get(report_id)
    if not result:
        return jsonify({"reportId": report_id, "status": "unknown"}), 200
    return jsonify({"reportId": report_id, **result}), 200


@app.route("/api/resume/export/<report_id>", methods=["GET"])
def export_resume_report(report_id: str):
    result = _RESULTS.get(report_id)
    if not result:
        return jsonify({"error": "Report not found"}), 404

    pdf_path = export_to_pdf(result, output_path=os.path.join(UPLOAD_DIR, f"{report_id}.pdf"))
    return jsonify({"pdf_path": pdf_path}), 200


@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(_e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True,
    )
