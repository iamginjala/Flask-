import spacy
from spacy.matcher import PhraseMatcher
import re

nlp = spacy.load("en_core_web_sm")
SKILL_LIST = [
        "python", "java", "aws", "sql", "docker", "react", "flask", "kubernetes", "algorithms", "data structures",
        "node.js", "c++", "spring boot", "linux", "azure", "mongodb", "redis", "ai", "ml",
        "uipath", "rpa", "git", "jenkins", "html", "css", "typescript", "ci/cd", "go", "golang"
    ]




def extract_skills_from_jd(jd_text):
    doc = nlp(jd_text)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILL_LIST]
    matcher.add("Skills", patterns)
    matches = matcher(doc)
    jd_skills = set(doc[start:end].text.lower() for _, start, end in matches)

    return jd_skills
def match_job_title(resume_text: str, jd_text: str) -> bool:
    job_titles = re.findall(r"\b(?:developer|engineer|manager|consultant|analyst)\b", resume_text.lower())
    jd_title_match = re.search(r"\b(?:developer|engineer|manager|consultant|analyst)\b", jd_text)
    title_match = any(jd_title_match.group() in title for title in job_titles) if jd_title_match else False

    return title_match

def extract_certifications(resume_text, jd_text):
    certs = ["aws certified", "pmp", "azure fundamentals", "gcp certified", "scrum master", "ocjp"]
    certs_in_resume = [cert for cert in certs if cert in resume_text.lower()]
    certs_in_jd = [cert for cert in certs if cert in jd_text]

    return certs_in_resume,certs_in_jd
def extract_soft_skills(resume_text):
    soft_skills = {"communication", "leadership", "teamwork", "collaboration", "problem-solving"}
    soft_present = [s for s in soft_skills if s in resume_text.lower()]

    return soft_present