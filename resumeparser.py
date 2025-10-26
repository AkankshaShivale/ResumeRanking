from PyPDF2 import PdfReader
import re
reader = PdfReader("resume\AkankshaShivaleResume_DataToBiz.pdf")
str = ""
for page in reader.pages:
    str+=page.extract_text()

text = str.lower()
# print(text)
# print(re.findall(r"\n\s*([A-Za-z\s&]+)\s*\n(?=\s*\n)", text))

common_resume_headers = {
    "personal": [
        "contact information",
        "personal information",
        "profile",
        "about me"
    ],
    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "objective",
        "career objective"
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "coursework"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "relevant experience",
        "career history"
    ],
    "projects": [
        "projects",
        "academic projects",
        "research projects",
        "work projects",
        "capstone projects"
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "key skills",
        "expertise"
    ],
    "certifications": [
        "certifications",
        "licenses",
        "training",
        "professional training"
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors",
        "recognition"
    ],
    "publications": [
        "publications",
        "research papers",
        "patents"
    ],
    "extracurricular": [
        "hobbies",
        "interests",
        "extracurricular activities",
        "volunteer work",
        "community service"
    ],
    "languages": [
        "languages",
        "language proficiency"
    ],
    "references": [
        "references",
        "referees",
        "professional references"
    ]
}

sections = re.findall(r"\n\s*([A-Za-z\s]+)\s*\n", text)
sections = [s.strip().lower() for s in sections if len(s.strip().split()) <= 5]

# print(sections)

d = {key: s for s in sections for key,value in common_resume_headers.items() if s in common_resume_headers[key]}
for k in common_resume_headers.keys():
    if k not in d.keys():
        d[k] = None

headers = [value for value in d.values() if value]

print(headers)

# Find the index of "skills" in headers
skill_idx = headers.index("skills")

# Determine the next header after skills
next_header = headers[skill_idx + 1] if skill_idx + 1 < len(headers) else None

# Regex pattern: capture text after "skills" until the next header (non-greedy)
if next_header:
    pattern = rf"skills\s*(.*?)\s*{next_header}"
else:
    pattern = r"skills\s*(.*)"

match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
skills_text = match.group(1).strip() if match else ""

print(skills_text)


# with open("AkankshaShivaleResume_DataToBiz.pdf",'rb') as f:
#     content = f.read()
#     print(content.decode(errors ="ignore"))
# this will print all file content in binary which is not useful.