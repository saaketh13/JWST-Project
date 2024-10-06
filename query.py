# query.py
# Being able to query the data using english questions
# question: "Find galaxies in the Carina constellation under 8000 light years"
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
import pandas as pd
import main 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


windows_path = r"C:\Users\Anaki\OneDrive\Desktop\codingprojects\jwst\JWST-Project\Copy of Dataset - Sheet1 (1).csv"
wsl_path = '/mnt/c' + windows_path[2:].replace('\\', '/')

def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

tokenizer = AutoTokenizer.from_pretrained("AstroMLab/astrollama-2-7b-base_abstract")
model = AutoModelForSequenceClassification.from_pretrained("AstroMLab/astrollama-2-7b-base_abstract")

def classify_intent(question):
    inputs = tokenizer(question, return_tensors="pt", truncation = True, padding = True)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim = 1)
    intent = torch.argmax(probabilities).item()
    return ["find", "distance"][intent] # Simplified intents

def extract_entities(question):
    object_entities = re.finall(r'(NGC \d+|M\d+)', question)
    constellation_names = data['Constellation'].unique().tolist()

    matched_constellations = process.extractOne(question, constellation_names, scorer = fuzz.token_sort_ratio)
    if matched_constellations[1] > 60:
        constellation = matched_constellations[0] 
    else:
        None
    distance = re.findall(r'(\d+) light years', question)

    return {
        "object": object_entities,
        "constellation": [constellation] if constellation else [],
        "distance": distance
    }

def query_data(intent, entities, data):
    if intent == "find":
        query = data
        if entities["constellation"]:
            query = query[query['Constellation'].str.contains('|'.join(entities["constellation"]), case = False, na = False)]
        if entities["distance"]:
            max_distance = int(entities["distance"][0])
            query = query[pd.to_numeric(query['distance(lightyear)'].str.replace(',', ''), errors='coerce') < max_distance]
        return query
    elif intent == "distance":
        if entities["object"]:
            object_name = entities["object"][0]
            result = data[data['object_name'].str.contains(object_name, case=False, na=False)]
            if not result.empty:
                return f"The distance of the {object_name} is {result['distance(lightyear)'].values[0]} light years."
        elif intent == "description":
            # Generate a backstory using a pre-trained language model like AstroMLab/astrollama-2-7b-base_abstract
            return f"Generating an AI backstory for {entities['object'][0] if entities['object'] else 'the selected object'}."
        return "I couldn't find an answer to that question."
    

def process_question(question, data):
    intent = classify_intent(question)
    entities = extract_entities(question)
    return query_data(intent, entities, data)


data = load_data(wsl_path)
questions = [
    "Find galaxies in the Carina constellation under 8000 light years",
    "What is the distance of NGC 604 in Triangulum?",
    "Tell me about Orion objects"
]


for question in questions:
    print(f"Question:  {question}")
    result = process_question(question, data)
    print("Answer: {result}")
    print()


# Example of using NLP to ask a question
# user_question = "What is the distance of NGC 604 in Triangulum?"
# result = query_csv_with_nlp(user_question, data)
# print(result)
