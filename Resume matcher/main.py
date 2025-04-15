from flask import Flask, request, render_template, redirect, url_for
from pdfminer.high_level import extract_text
import spacy
import os
import re
from spacy.matcher import PhraseMatcher
from collections import Counter
from fuzzywuzzy import fuzz
from dateutil import parser as date_parser
from datetime import datetime, date
import pdfplumber

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

nlp = spacy.load("en_core_web_sm")

def extract_sections(text):
    section_titles = [
        "professional summary", "education", "work experience", "experience", "professional experience",
        "projects", "technical skills", "certifications", "contact", "personal information"
    ]

    sections = {}
    current_section = None
    lines = text.split('\n')

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # If this line matches a section title exactly, it's a new section
        if line_lower in section_titles:
            current_section = line_lower
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line_stripped)

    # Join all lines into a single string per section
    for key in sections:
        sections[key] = "\n".join(sections[key]).strip()

    return sections


def calculate_total_experience(prof_experience_text: str) -> float:
    """
    Calculate total years of experience from the Professional Experience section text.
    Extracts date ranges (e.g. 'Jan 2019 - Feb 2023' or 'Aug 2020 to Present') and
    sums up the durations.
    Returns the total years of experience as a float rounded to one decimal place.
    """
    date_pattern = re.compile(
        r'(?i)\b('
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}'
        r')\s*(?:-|–|\s+to\s+)\s*('
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}|Present|present'
        r')'
    )

    total_days = 0
    for match in date_pattern.finditer(prof_experience_text):
        start_str = match.group(1)
        end_str = match.group(2)
        try:
            start_date = date_parser.parse(start_str, default=datetime(1900, 1, 1)).date()
        except Exception:
            continue
        if end_str.lower() == "present":
            end_date = date.today()
        else:
            try:
                end_date = date_parser.parse(end_str, default=datetime(1900, 1, 1)).date()
            except Exception:
                continue
        if end_date < start_date:
            continue
        total_days += (end_date - start_date).days

    return round(total_days / 365.0, 1) if total_days > 0 else 0.0


def infer_experience_level(doc):
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    senior_keywords = {'lead', 'manage', 'direct', 'oversee', 'supervise', 'orchestrate'}
    mid_senior_keywords = {'develop', 'design', 'analyze', 'implement', 'coordinate', 'execute'}
    mid_junior_keywords = {'assist', 'support', 'collaborate', 'participate', 'facilitate'}
    if any(v in verbs for v in senior_keywords):
        return "Senior"
    elif any(v in verbs for v in mid_senior_keywords):
        return "Mid-Senior"
    elif any(v in verbs for v in mid_junior_keywords):
        return "Mid-Junior"
    else:
        return "Entry Level"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_resume():
    uploaded_file = request.files.get('file')
    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(path)
        return redirect(url_for('process_jd'))
    return "Please upload a valid PDF."

@app.route('/job_description', methods=['GET', 'POST'])
def process_jd():
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    resume_text = ""
    sections = {}
    tips = []

    SKILL_LIST = [
        "python", "java", "aws", "sql", "docker", "react", "flask", "kubernetes", "algorithms", "data structures",
        "node.js", "c++", "spring boot", "linux", "azure", "mongodb", "redis", "ai", "ml",
        "uipath", "rpa", "git", "jenkins", "html", "css", "typescript", "ci/cd", "go", "golang"
    ]

    if uploaded_files:
        latest_file = max([os.path.join(UPLOAD_FOLDER, f) for f in uploaded_files], key=os.path.getctime)
        def extract_pdf_text(filepath):
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        resume_text = extract_pdf_text(latest_file)
        sections = extract_sections(resume_text)
        print(sections)

        def extract_individual_skills(lines):
            skills_set = set()
            for entry in lines:
                parts = re.split(r'[,:•\-\n]', entry)
                for skill in parts:
                    cleaned = skill.strip().lower()
                    if cleaned and cleaned not in {"programming languages", "frameworks", "tools"}:
                        skills_set.add(cleaned)
            return skills_set

        raw_skill_lines = sections.get("technical skills", "").split('\n')
        resume_skills_set = extract_individual_skills(raw_skill_lines)

    if request.method == 'POST':
        jd_text = request.form.get('story', '').lower()
        doc = nlp(jd_text)

        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(skill) for skill in SKILL_LIST]
        matcher.add("Skills", patterns)
        matches = matcher(doc)
        jd_skills_set = set(doc[start:end].text.lower() for _, start, end in matches)

        def fuzzy_skill_match(resume_skills, jd_skills, threshold=85):
            matched = []
            for jd_skill in jd_skills:
                for res_skill in resume_skills:
                    if fuzz.ratio(jd_skill, res_skill) >= threshold:
                        matched.append(jd_skill)
                        break
            return matched

        matching_skills = fuzzy_skill_match(resume_skills_set, jd_skills_set)
        missing_skills = list(set(jd_skills_set) - set(matching_skills))

        exp_section = sections.get("professional experience", "")
        print(exp_section)
        experience_years = calculate_total_experience(exp_section)
        experience_level = infer_experience_level(nlp(exp_section))

        experience_phrases = re.findall(r'(\d{1,2})\+?\s?(?:years|yrs)', jd_text)
        if experience_phrases:
            min_required = max([int(x) for x in experience_phrases])
            experience_match = experience_years >= min_required
        else:
            experience_match = "Not specified"

        job_titles = re.findall(r"\b(?:developer|engineer|manager|consultant|analyst)\b", resume_text.lower())
        jd_title_match = re.search(r"\b(?:developer|engineer|manager|consultant|analyst)\b", jd_text)
        title_match = any(jd_title_match.group() in title for title in job_titles) if jd_title_match else False

        certs = ["aws certified", "pmp", "azure fundamentals", "gcp certified", "scrum master", "ocjp"]
        certs_in_resume = [cert for cert in certs if cert in resume_text.lower()]
        certs_in_jd = [cert for cert in certs if cert in jd_text]

        soft_skills = {"communication", "leadership", "teamwork", "collaboration", "problem-solving"}
        soft_present = [s for s in soft_skills if s in resume_text.lower()]

        transferable_skills = {
            "leadership": "Led a team of developers to deliver a project under deadline.",
            "problem solving": "Resolved production bugs quickly during release.",
            "collaboration": "Worked with product and QA in Agile environment.",
            "communication": "Presented updates in team meetings and sprint reviews.",
        }

        summary_text = sections.get("professional summary", "Summary not found.")

        return render_template("dashboard.html", **{
            "summary": summary_text,
            "skills": {
                "from_resume": list(resume_skills_set),
                "from_jd": list(jd_skills_set),
                "matched": matching_skills,
                "missing": missing_skills
            },
            "experience": {
                "phrases_found": experience_phrases,
                "matched": experience_match,
                "years": experience_years,
                "level": experience_level
            },
            "job_title_match": title_match,
            "certifications": {
                "matched": certs_in_resume,
                "missing": list(set(certs_in_jd) - set(certs_in_resume))
            },
            "soft_skills_found": soft_present,
            "transferable_skills": transferable_skills,
            "current_year": datetime.now().year
        })

    return render_template('basic.html')

if __name__ == '__main__':
    app.run(debug=True)
