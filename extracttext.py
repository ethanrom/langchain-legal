import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

def extract_info(input_text):
    # Parse the input text using spaCy
    doc = nlp(input_text)
    
    # Find all named entities and dates in the parsed text
    names = [(ent.text, ent.start_char, ent.end_char, "PERSON") for ent in doc.ents if ent.label_ == "PERSON"]
    addresses = [(ent.text, ent.start_char, ent.end_char, "ADDRESS") for ent in doc.ents if ent.label_ == "GPE"]
    dates = [(ent.text, ent.start_char, ent.end_char, "DATE") for ent in doc.ents if ent.label_ == "DATE"]
    
    # Return the extracted information as a dictionary
    return {"names": names, "addresses": addresses, "dates": dates}

