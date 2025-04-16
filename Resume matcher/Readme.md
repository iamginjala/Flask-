# Resume Match Dashboard

An intelligent resume and job description matcher built using Flask, spaCy, and PDFMiner. This project parses a user's resume and compares it with a pasted job description to highlight matching skills, inferred experience levels, transferable skills, and missing keywords — all within a clean, downloadable dashboard.

## Features

- **PDF Resume Parsing**: Uses `pdfplumber` to extract text from uploaded resumes.
- **Section Detection**: Separates resume into structured sections like Professional Summary, Technical Skills, Experience, and Education.
- **Skill Extraction**: Extracts technical skills from both resumes and job descriptions using spaCy + PhraseMatcher.
- **Fuzzy Matching**: Matches resume skills to JD skills even with minor mismatches using fuzzywuzzy.
- **Experience Inference**: Dynamically calculates total years of experience from job date ranges and infers seniority level using NLP.
- **Transferable Skills**: Highlights user-defined strengths from experience relevant to the role.
- **Dashboard Generation**: Displays the results in a clean, responsive dashboard (HTML + CSS).
- **PDF Download**: Exports the dashboard as a printable/downloadable PDF for use as a modern resume alternative.

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-WebApp-lightgrey)
![spaCy](https://img.shields.io/badge/NLP-spaCy-orange)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap-blueviolet)


## How It Works

1. **Upload Resume**: User uploads a PDF resume.
2. **Paste Job Description**: User pastes a job description from LinkedIn/Indeed/etc.
3. **Dashboard Output**: System parses both and compares:
   - Matched vs. Missing Skills
   - Total Experience & Inferred Level
   - Soft Skills & Transferable Skills
   - Project Showcase (with Tech Stack)
4. **Download as PDF**: Dashboard can be exported as a one-page PDF report.

## Project Demo
 see output in output folder

## Setup Instructions

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
