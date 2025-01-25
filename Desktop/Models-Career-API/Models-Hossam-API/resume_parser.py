import pdfplumber
import re

def parse_resume(pdf_path):
    """Parse the resume PDF to extract relevant information.

    Args:
        pdf_path (str): The path to the PDF resume.

    Returns:
        dict: A dictionary containing extracted information.
    """
    resume_data = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": [],
        "education": [],
    }

    with pdfplumber.open(pdf_path) as pdf:
        # Iterate through each page of the PDF
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                # Extract name (assumed to be the first line)
                if resume_data["name"] is None:
                    resume_data["name"] = text.split('\n')[0]

                # Extract email using regex
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
                if email_match:
                    resume_data["email"] = email_match.group(0)

                # Extract phone number using regex (example pattern, can be adjusted)
                phone_match = re.search(r'\(?\b[0-9]{3}[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b', text)
                if phone_match:
                    resume_data["phone"] = phone_match.group(0)

                # Extract skills (assumes skills are listed under a "Skills" section)
                if "skills" in text.lower():
                    skills_section = text.lower().split("skills")[-1]
                    skills = re.findall(r'\b\w+\b', skills_section)
                    resume_data["skills"].extend(skills)

                # Extract education (assumes education is listed under an "Education" section)
                if "education" in text.lower():
                    education_section = text.lower().split("education")[-1]
                    education = re.findall(r'\b\w+\b', education_section)
                    resume_data["education"].extend(education)

    return resume_data


