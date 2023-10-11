import spacy
nlp = spacy.load("model_output_old/model-best/")

with open("test_resume.txt", "r") as f:
    text = f.read()
#print(nlp.pipeline)
doc = nlp(text)
for ent in doc.ents:
     print(ent.text+ " -> " +ent.label_)