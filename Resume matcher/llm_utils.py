import ollama
import ast
import re


def extract_transferable_skills(resume_text: str, jd_text: str) -> dict:
    prompt = f"""
    You are a resume analysis assistant.

    Given a resume and a job description, extract transferable skills as a Python-style dictionary where:
    - Key = skill name
    - Value = 1-sentence justification based on resume and JD
    Return ONLY the dictionary. No explanations, no variable assignments, no markdown.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    raw = response["message"]["content"]

    print("Raw response from LLM:\n", raw)

    try:
        # Strip variable assignment and markdown
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            cleaned_dict = match.group(0)
            return ast.literal_eval(cleaned_dict)
        else:
            print("❌ No valid dictionary found in LLM output.")
            return {}
    except Exception as e:
        print("LLM parsing failed:", e)
        return {}
