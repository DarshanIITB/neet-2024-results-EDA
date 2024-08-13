import os
import PyPDF2
import json

def get_marks_from_text(text):
    marks = []
    for line in text:
        entries = line[:300]
        for i in range(0, 30):
            entry = entries[(2*i+1)*5:(2*i+2)*5].strip()
            if entry.isnumeric():
                marks.append(int(entry))
            else:
                break
    print(marks)
    return marks

def get_marks_list():
    marks_list = []
    centre_codes_ = []
    file_list = os.listdir('centre_wise_result_pdf')
    for file_name in file_list:
        marks = []
        with open(f"centre_wise_result_pdf/{file_name}", 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()[2:]
                marks += get_marks_from_text(text.splitlines()[2:])
        centre_codes_.append(file_name.split('.')[0])
        marks_list.append(marks)
    return marks_list, centre_codes_

marks_list, centre_codes_ = get_marks_list()

centre_wise_scores = []
for i, marks in enumerate(marks_list):
    centre_wise_scores.append({"id": centre_codes_[i], "scores": marks})

centre_wise_scores_json = {entry["id"]: entry["scores"] for entry in centre_wise_scores}

with open('centre_wise_scores.json', 'w') as file:
    json.dump(centre_wise_scores_json, file)