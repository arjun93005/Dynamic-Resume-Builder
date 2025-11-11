# server/tests/test_scoring.py
import pytest
from server.services.score_calculator import compute_resume_score

def sample_sections_minimal():
    return {
        "contact_info": {"email": "", "phone": "", "linkedin": "", "github": ""},
        "education": "",
        "experience": "",
        "skills": [],
        "projects": "",
        "certifications": ""
    }

def sample_sections_full():
    return {
        "contact_info": {"email": "a@b.com", "phone": "+1 234 567 8900", "linkedin": "linkedin.com/in/x", "github": ""},
        "education": "Bachelor of Technology in Computer Science, ABC University (2021-2025)",
        "experience": "Software Intern at TechCorp\nWorked on APIs\nImplemented feature X",
        "skills": ["Python", "Flask", "React", "AWS", "SQL", "Docker", "Kubernetes", "TensorFlow"],
        "projects": "Chatbot project using NLP",
        "certifications": "AWS Certified Cloud Practitioner"
    }

def test_score_minimal_is_low():
    sec = sample_sections_minimal()
    meta = {"word_count": 10}
    res = compute_resume_score(sec, meta)
    assert isinstance(res["score"], int)
    assert res["score"] <= 20  # should be low for minimal resume

def test_score_full_is_high():
    sec = sample_sections_full()
    meta = {"word_count": 350}
    res = compute_resume_score(sec, meta)
    assert isinstance(res["score"], int)
    assert res["score"] >= 70  # full resume should score high

def test_breakdown_fields_present():
    sec = sample_sections_full()
    res = compute_resume_score(sec, {"word_count": 200})
    assert "breakdown" in res
    for k in ["contact","education","experience","skills","projects_and_certifications","length"]:
        assert k in res["breakdown"]
