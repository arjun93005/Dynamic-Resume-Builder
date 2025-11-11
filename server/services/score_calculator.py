# server/services/score_calculator.py
from typing import Dict, Any, List
import re

DEGREE_KEYWORDS = [
    "bachelor", "b\.tech", "btech", "bsc", "bs", "master", "m\.tech", "ms", "msc", "phd", "mba"
]
TECH_SKILLS_SAMPLE = [
    "python","java","javascript","c++","c#","sql","react","node","flask","django","tensorflow",
    "pytorch","aws","azure","gcp","docker","kubernetes","html","css","typescript","golang","rust"
]

def _present(val) -> bool:
    return bool(val and str(val).strip())

def _count_nonempty_lines(s: str) -> int:
    if not s:
        return 0
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    return len(lines)

def compute_resume_score(sections: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Returns:
      {
        "score": int,            # 0..100
        "breakdown": {           # category -> points, and optional notes
          "contact": 10,
          ...
        },
        "notes": [ ... ]         # human readable notes
      }
    """
    breakdown = {}
    notes = []

    # Contact (10)
    contact = sections.get("contact_info", {}) or {}
    contact_score = 0
    if _present(contact.get("email")):
        contact_score += 4
    if _present(contact.get("phone")):
        contact_score += 4
    if _present(contact.get("linkedin")) or _present(contact.get("github")):
        contact_score += 2
    breakdown["contact"] = contact_score
    if contact_score < 10:
        notes.append("Contact info incomplete")

    # Education (15)
    edu_txt = sections.get("education", "") or ""
    edu_score = 0
    if _present(edu_txt):
        edu_score += 10
        # degree keyword
        txt_lower = edu_txt.lower()
        if any(re.search(r"\b" + kw + r"\b", txt_lower) for kw in DEGREE_KEYWORDS):
            edu_score += 5
    breakdown["education"] = edu_score
    if edu_score == 0:
        notes.append("No education section detected")

    # Experience (20)
    exp_txt = sections.get("experience", "") or ""
    exp_score = 0
    if _present(exp_txt):
        exp_score += 10
        lines = _count_nonempty_lines(exp_txt)
        if lines >= 3:
            exp_score += 10
        elif lines >= 1:
            exp_score += 5
    breakdown["experience"] = exp_score
    if exp_score < 10:
        notes.append("Few or no experience lines found")

    # Skills (25)
    skills = sections.get("skills", []) or []
    skill_score = 0
    if skills:
        skill_score += 10
        n = 0
        # If skills passed as a list of strings or a single joined string
        if isinstance(skills, list):
            n = len([s for s in skills if _present(s)])
        elif isinstance(skills, str):
            # try to split by comma or newline
            n = len([s for s in re.split(r"[\n,;•]", skills) if _present(s)])
        # tiered scoring
        if n >= 8:
            skill_score += 10
        elif n >= 4:
            skill_score += 6
        elif n >= 1:
            skill_score += 2
        # tech skill presence
        lower_join = " ".join(skills).lower() if isinstance(skills, list) else (skills.lower() if isinstance(skills, str) else "")
        if any(ts in lower_join for ts in TECH_SKILLS_SAMPLE):
            skill_score += 5
    breakdown["skills"] = skill_score
    if skill_score < 10:
        notes.append("Skills section weak or missing")

    # Projects & Certifications (10)
    projects_txt = sections.get("projects", "") or ""
    certs_txt = sections.get("certifications", "") or ""
    pc_score = 0
    if _present(projects_txt):
        pc_score += 5
    if _present(certs_txt):
        pc_score += 5
    breakdown["projects_and_certifications"] = pc_score
    if pc_score == 0:
        notes.append("No projects or certifications detected")

    # Length / substance (10)
    length_score = 0
    word_count = 0
    if metadata and isinstance(metadata, dict):
        try:
            word_count = int(metadata.get("word_count", 0) or 0)
        except Exception:
            word_count = 0
    # fallback - estimate from sections
    if word_count == 0:
        combined_text = " ".join([
            str(sections.get("contact_info", "")),
            str(sections.get("education", "")),
            str(sections.get("experience", "")),
            " ".join(sections.get("skills", [])) if isinstance(sections.get("skills", []), list) else str(sections.get("skills", "")),
        ])
        word_count = len([w for w in combined_text.split() if w.strip()])
    if word_count >= 201:
        length_score = 10
    elif 50 <= word_count <= 200:
        length_score = 5
    else:
        length_score = 0
    breakdown["length"] = length_score
    if length_score == 0:
        notes.append("Resume appears very short")

    # Sum up
    total = sum(breakdown.values())
    # clamp
    if total < 0:
        total = 0
    if total > 100:
        total = 100

    return {
        "score": int(round(total)),
        "breakdown": breakdown,
        "notes": notes,
        "word_count": word_count
    }
