from flask import Flask, request, render_template, redirect, url_for
import spacy
import os
import re
from datetime import datetime
from sections import extract_sections
from experience import calculate_total_experience,infer_experience_level,check_experience_requirement
from resume import fuzzy_skill_match,extract_individual_skills,extract_pdf_text
from llm_utils import extract_transferable_skills
from job_utils import extract_skills_from_jd,match_job_title,extract_certifications,extract_soft_skills

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

nlp = spacy.load("en_core_web_sm")


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
    resume_skills_set = set()
    if uploaded_files:
        latest_file = max([os.path.join(UPLOAD_FOLDER, f) for f in uploaded_files], key=os.path.getctime)
        resume_text = extract_pdf_text(latest_file)
        sections = extract_sections(resume_text)
        raw_skill_lines = sections.get("technical skills", "").split('\n')
        resume_skills_set = extract_individual_skills(raw_skill_lines)

    if request.method == 'POST':
        jd_text = request.form.get('story', '').lower()
        jd_skills_set = extract_skills_from_jd(jd_text)

        matching_skills = fuzzy_skill_match(resume_skills_set, jd_skills_set)
        missing_skills = list(set(jd_skills_set) - set(matching_skills))

        exp_section = sections.get("professional experience", "")
        # print(exp_section)
        experience_years = calculate_total_experience(exp_section)
        experience_level = infer_experience_level(nlp(exp_section))
        experience_phrases = re.findall(r'(\d{1,2})\+?\s?(?:years|yrs)', jd_text)
        experience_match = check_experience_requirement(jd_text,experience_years)

        title_match = match_job_title(resume_text,jd_text)

        certs_in_resume,certs_in_jd  = extract_certifications(resume_text,jd_text)

        soft_present = extract_soft_skills(resume_text)

        transferable_skills = extract_transferable_skills(resume_text[:3000], jd_text[:2000])

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
