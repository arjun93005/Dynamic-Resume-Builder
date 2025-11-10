import re

def extract_contact_info(text: str) -> dict:
    """
    Extracts contact info — email, phone, and LinkedIn/GitHub links
    """
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.findall(r"\+?\d[\d\s\-]{8,}\d", text)
    linkedin = re.findall(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+", text)
    github = re.findall(r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+", text)

    return {
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "linkedin": linkedin[0] if linkedin else "",
        "github": github[0] if github else "",
    }


def extract_education(text: str) -> str:
    """
    Extracts the Education section from resume text
    """
    pattern = r"(education|academics|qualification|b\.tech|bachelor|master|university|college)[\s\S]{0,500}"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).strip() if match else ""


def extract_experience(text: str) -> str:
    """
    Extracts the Work Experience / Employment section
    """
    pattern = r"(experience|employment|internship|work history|professional)[\s\S]{0,600}"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).strip() if match else ""


def extract_skills(text: str) -> list:
    """
    Extracts a list of skills based on common keywords or bullet patterns
    """
    pattern = r"(skills|technical skills|technologies|competencies)[\s\S]{0,300}"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return []

    section = match.group(0)
    # Split by commas, bullets, or line breaks
    parts = re.split(r"[\n,•;]", section)
    clean = [p.strip() for p in parts if len(p.strip()) > 1 and not re.match(r"skills", p, re.IGNORECASE)]
    return clean


def extract_sections(text: str) -> dict:
    """
    High-level extraction combining all core sections
    """
    contact = extract_contact_info(text)
    education = extract_education(text)
    experience = extract_experience(text)
    skills = extract_skills(text)

    return {
        "contact_info": contact,
        "education": education,
        "experience": experience,
        "skills": skills,
    }
