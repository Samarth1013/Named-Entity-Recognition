import json
import os
import spacy
from spacy.tokens import DocBin

resume_data = json.load(open('resume_data.json', 'r', encoding="utf-8"))
print(len(resume_data))

def spacy_doc(file,data):
  nlp = spacy.blank("en")
  db = DocBin()

  for text,annot in data:
    doc = nlp.make_doc(text)
    ents = []
    entity_indices = []
    for start, end, label in annot["entities"]:  # add character indexes
        skip_entity = False
        for idx in range(start, end):
            if idx in entity_indices:
                skip_entity = True
                break
        if skip_entity == True:
            continue

        entity_indices = entity_indices + list(range(start,end))

        try:
            span = doc.char_span(start, end, label=label, alignment_mode="strict")
        except:
            continue

        if span is None:
            error_data = str([start, end])+ "   " +str(text) + "\n"
            file.write(error_data)
            #print("Skipping entity")
        else:
            ents.append(span)
    try:
      doc.ents = ents  # label the text with the ents
      db.add(doc)
    except:
      pass

  return db

from sklearn.model_selection import train_test_split
train, test = train_test_split(resume_data, test_size=0.3)
print(len(train), len(test))

os.chdir(r'D:\samar\PycharmProjects\Resume_Parser')
file = open('error.txt', 'w', encoding='utf-8')

db = spacy_doc(file, train)
db.to_disk("./resume_train.spacy")

db = spacy_doc(file, test)
db.to_disk("./resume_test.spacy")

file.close()

import torch
print(torch.cuda.is_available())
# def db(file,data):
# nlp = spacy.blank("en")
# db = DocBin() # create a DocBin object
#
# with open("resume_data.json", "r", encoding="utf-8") as json_file:
#     data=json.loads(json_file.read())
#
#     for text,annot in data:
#         doc = nlp.make_doc(text)
#         ents = []
#         entity_indices = []
#         for start, end, label in annot["entities"]:  # add character indexes
#             skip_entity = False
#             for idx in range(start, end):
#                 if idx in entity_indices:
#                     skip_entity = True
#                     break
#             if skip_entity == True:
#                 continue
#
#             entity_indices = entity_indices + list(range(start,end))
#
#             try:
#                 span = doc.char_span(start, end, label=label, alignment_mode="strict")
#             except:
#                 continue
#
#             if span is None:
#                 # error_data = str([start, end])+ "  " +str(text) + "\n"
#                 # file.write(error_data)
#                 print("Skipping entity")
#             else:
#                 ents.append(span)
#         doc.ents = ents  # label the text with the ents
#         db.add(doc)
#
#
# os.chdir(r'D:\samar\PycharmProjects\Resume_Parser')
# db.to_disk("./resume_train.spacy") # save the docbin object
#
# from spacy.cli.train import train
# train("./config.cfg", "./output_resume", overrides={"paths.train": "./resume_train.spacy", "paths.dev": "./resume_train.spacy"})