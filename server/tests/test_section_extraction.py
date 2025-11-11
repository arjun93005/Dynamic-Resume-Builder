import pytest
from server.services.section_extractor import extract_sections
from server.services.section_extractor import detect_missing_sections

@pytest.fixture
def sample_resume_text():
    return """
    John Doe
    john.doe@email.com | +1 234 567 8900 | linkedin.com/in/johndoe | github.com/johndoe

    EDUCATION
    Bachelor of Technology in Computer Science, ABC University (2020–2024)

    EXPERIENCE
    Software Intern at TechCorp - Built REST APIs with Flask.

    SKILLS
    Python, JavaScript, SQL, Flask, React
    """

def test_extract_sections_returns_dict(sample_resume_text):
    result = extract_sections(sample_resume_text)
    assert isinstance(result, dict)
    assert "contact_info" in result
    assert "education" in result
    assert "experience" in result
    assert "skills" in result

def test_contact_info_extraction(sample_resume_text):
    data = extract_sections(sample_resume_text)["contact_info"]
    assert data["email"] == "john.doe@email.com"
    assert "+1 234 567 8900" in data["phone"]
    assert "linkedin.com/in/johndoe" in data["linkedin"]
    assert "github.com/johndoe" in data["github"]

def test_education_extraction(sample_resume_text):
    edu = extract_sections(sample_resume_text)["education"]
    assert "Computer Science" in edu

def test_experience_extraction(sample_resume_text):
    exp = extract_sections(sample_resume_text)["experience"]
    assert "Software Intern" in exp
    assert "Flask" in exp

def test_skills_extraction(sample_resume_text):
    skills = extract_sections(sample_resume_text)["skills"]
    assert "Python" in skills
    assert "React" in skills


def test_detect_missing_sections_all_present():
    data = {
        "contact_info": {"email": "test@test.com"},
        "education": "B.Tech at PES",
        "experience": "2 years internship",
        "skills": ["Python", "ML"]
    }
    missing = detect_missing_sections(data)
    assert missing == []

def test_detect_missing_sections_some_missing():
    data = {
        "contact_info": {},
        "education": "",
        "experience": "Worked on project",
        "skills": []
    }
    missing = detect_missing_sections(data)
    assert "contact_info" in missing
    assert "education" in missing
    assert "skills" in missing
    assert "experience" not in missing