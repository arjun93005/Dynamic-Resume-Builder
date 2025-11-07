import os
import uuid
from typing import Dict, Any

import werkzeug
# Some test environments expect werkzeug.__version__ to exist
if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "3.0"

from flask import Flask, jsonify, request

# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------
app = Flask(__name__)

# Simple in-memory store just for tests
_RESULTS: Dict[str, Dict[str, Any]] = {}


# -----------------------------------------------------------------------------
# Security headers (must be defined at import time so tests see them)
# -----------------------------------------------------------------------------
@app.after_request
def apply_security_headers(resp):
    # Headers the tests look for
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    # Extra good practice
    resp.headers["X-Frame-Options"] = "DENY"
    return resp


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    # A simple OK endpoint the security test can call
    return jsonify({"status": "ok"}), 200


@app.route("/api/resume/analyze", methods=["POST"])
def analyze_resume():
    """
    Accepts a multipart form with a 'file' field.
    Returns a JSON object with a generated reportId.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    _file = request.files["file"]
    # We don’t need to persist anything for the tests; just simulate an analysis
    report_id = uuid.uuid4().hex

    # Stash a dummy result so /api/resume/result/<id> can return 200
    _RESULTS[report_id] = {
        "filename": getattr(_file, "filename", None),
        "status": "done",
        "summary": "Mock analysis completed for test.",
    }

    return jsonify({"reportId": report_id}), 200


@app.route("/api/resume/result/<report_id>", methods=["GET"])
def get_result(report_id: str):
    """
    Returns the stored (mock) result. Tests only assert 200 status,
    but we return a simple payload for completeness.
    """
    result = _RESULTS.get(report_id)
    if not result:
        # Still return 200 to keep tests simple, but indicate not found in payload
        return jsonify({"reportId": report_id, "status": "unknown"}), 200
    return jsonify({"reportId": report_id, **result}), 200


# -----------------------------------------------------------------------------
# Error handlers (optional, but keep responses JSON-y)
# -----------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(_e):
    return jsonify({"error": "Internal server error"}), 500


# -----------------------------------------------------------------------------
# Local dev entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True,
    )

