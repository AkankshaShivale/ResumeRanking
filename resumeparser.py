import PyPDF2
from PyPDF2 import PdfReader

reader = PdfReader("AkankshaShivaleResume_DataToBiz.pdf")
str = ""
for page in reader.pages:
    str+=page.extract_text()




# with open("AkankshaShivaleResume_DataToBiz.pdf",'rb') as f:
#     content = f.read()
#     print(content.decode(errors ="ignore"))
# this will print all file content in binary which is not useful.