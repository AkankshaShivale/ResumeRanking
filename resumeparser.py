# with open("AkankshaShivaleResume_DataToBiz.pdf",'rb') as f:
#     content = f.read()
#     print(content.decode(errors ="ignore"))
# this will print all file content in binary which is not useful.

from PyPDF2 import PdfReader
import re
import json

reader = PdfReader("resume\RutujaBirajdar_Software_Web_Resume[1].pdf")

str = ""
for page in reader.pages:
    str+=page.extract_text()

text = str.lower()

# print(text)
# print(re.findall(r"\n\s*([A-Za-z\s&]+)\s*\n(?=\s*\n)", text))

common_resume_headers = {
    "personal": ["contact information", "personal information", "profile", "about me"],
    "summary": ["summary", "professional summary", "career summary", "objective", "career objective"],
    "education": ["education", "academic background", "academic qualifications", "coursework"],
    "experience": ["experience", "work experience", "professional experience", "employment history", "career history"],
    "projects": ["projects", "academic projects", "research projects", "work projects", "capstone projects"],
    "skills": ["skills", "technical skills", "core competencies", "key skills", "expertise"],
    "certifications": ["certifications", "licenses", "training", "professional training", "certification and tools"],
    "achievements": ["achievements", "awards", "honors", "recognition"],
    "publications": ["publications", "research papers", "patents"],
    "extracurricular": ["hobbies", "interests", "extracurricular activities", "volunteer work", "community service"],
    "languages": ["languages", "language proficiency"],
    "references": ["references", "referees", "professional references"],
    "address": ["address", "contact address", "residential address", "current address", "permanent address"]
}


# sections = re.findall(r"\n\s*([A-Za-z\s]+)\s*\n", text)
sections = re.findall(r"\n\s*([A-Za-z\s&:]+)\s*\n", text)
# sections = [s.strip().lower() for s in sections if len(s.strip().split()) <= 5]
sections = [s.strip().strip(':').lower() for s in sections if len(s.strip().split()) <= 5]

print("sections: ", sections)

# d = {
#     key: s
#     for s in sections
#     for key, value in common_resume_headers.items()
#     if s in common_resume_headers[key]
# }

d = {
    key: s.strip()
    for s in sections
    for key, value in common_resume_headers.items()
    if s.strip() in [v.strip().lower() for v in value]
}

for k in common_resume_headers.keys():
    if k not in d.keys():
        d[k] = None

headers = [value for value in d.values() if value]
print("headers: ", headers)

def extract_text_for_header(header):
    # Find exact header position (use lower() for case insensitivity)
    skill_idx = headers.index(header.lower())

    # Determine next header
    next_header = headers[skill_idx + 1] if skill_idx + 1 < len(headers) else None

    # Escape headers for regex safely
    header_escaped = re.escape(header)
    next_header_escaped = re.escape(next_header) if next_header else None

    '''re.escape() tells Python:
        "Treat this word literally, don’t interpret any special regex symbols inside it."
        Example:
        re.escape("c++") → 'c\+\+'
        (because + has special meaning in regex)
    '''

    if next_header_escaped:
        pattern = rf"{header_escaped}\s*[:]*\s*\n(.*?)(?=\n\s*{next_header_escaped}\s*[:]*\s*\n|$)"
        ''' 
        \n                             : Match a newline character (start of the header line).
        \s*                            : Match any amount of whitespace (spaces, tabs).
        {header_escaped}               : The actual header name, e.g., “education”.
        \s*\n                          : Allow optional spaces before the next newline after the header.
        (.*?)                          : Capture everything after the header (non-greedy — stops early when next pattern matches).
        \n\s*{next_header_escaped}\s*\n: Stop when the next header starts.
        '''
        '''[:]* → optional colon

            (?= ... | $) → lookahead: stop at next header or end of text

            re.S | re.I → multiline + case-insensitive'''
    else:
        pattern = rf"\n\s*{header_escaped}\s*\n(.*)"

    matches = re.findall(pattern, text, flags=re.S | re.I)
    return matches[0].strip() if matches else ""


header = "skills"
# for header in headers:
#     print(f"{header} : { extract_text_for_header(header)}")

header_and_content = {header: extract_text_for_header(header) for header in headers}

# final_sec_and_content = dict()

# for header in headers:
#     for key, value in d.items():
#         if header == value:
#             final_sec_and_content[key] = headers[header]



final_sec_and_content = {
    key: header_and_content[header]
    for header in headers
    for key, value in d.items()
    if header == value
}

for key,value in d.items():
    if not value:
         final_sec_and_content[key] = None

first_header = headers[0]
if first_header:
    # Capture text from start to first header
    pattern = rf"^(.*?)\s*{first_header}"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    personal_text = match.group(1).strip() if match else ""

if not final_sec_and_content["personal"]:
    final_sec_and_content["personal"] = personal_text


JSON_final_sec_and_content = json.dumps(final_sec_and_content,indent=4)
print(JSON_final_sec_and_content)

