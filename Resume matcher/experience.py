import re
from dateutil import parser as date_parser
from datetime import datetime, date

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

def check_experience_requirement(jd_text: str, years: float) -> bool | str:
    experience_phrases = re.findall(r'(\d{1,2})\+?\s?(?:years|yrs)', jd_text)
    if experience_phrases:
        min_required = max([int(x) for x in experience_phrases])
        experience_match = years >= min_required
    else:
        experience_match = "Not specified"

    return experience_match

