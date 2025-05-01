import pdfplumber
import re
from fuzzywuzzy import fuzz


def extract_pdf_text(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_individual_skills(lines):
    """
    Extracts skills from the resume
    :param lines: skills or technical skills from resume
    :return: set of skills
    """
    skills_set = set()
    for entry in lines:
        parts = re.split(r'[,:•\-\n]', entry)
        for skill in parts:
            cleaned = skill.strip().lower()
            if cleaned and cleaned not in {"programming languages", "frameworks", "tools"}:
                skills_set.add(cleaned)
    return skills_set

def fuzzy_skill_match(resume_skills, jd_skills, threshold=85):
        matched = []
        for jd_skill in jd_skills:
            for res_skill in resume_skills:
                if fuzz.ratio(jd_skill, res_skill) >= threshold:
                    matched.append(jd_skill)
                    break
        return matched

