# query.py
import pandas as pd
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fuzzywuzzy import fuzz, process

# Load the dataset
def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Load the model and tokenizer for intent classification
def load_intent_model():
    tokenizer = AutoTokenizer.from_pretrained("AstroMLab/astrollama-2-7b-base_abstract")
    model = AutoModelForSequenceClassification.from_pretrained("AstroMLab/astrollama-2-7b-base_abstract")
    return tokenizer, model

# Classify the intent from a user question
def classify_intent(question, tokenizer, model):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    intent = torch.argmax(probabilities).item()
    return ["find", "distance"][intent]

# Extract entities from a user question
def extract_entities(question, data):
    object_entities = re.findall(r'(NGC \d+|M\d+)', question)
    constellation_names = data['Constellation'].unique().tolist()
    matched_constellation = process.extractOne(question, constellation_names, scorer=fuzz.token_sort_ratio)
    constellation = matched_constellation[0] if matched_constellation[1] > 60 else None
    distance = re.findall(r'(\d+) light years', question)

    return {
        "object": object_entities,
        "constellation": [constellation] if constellation else [],
        "distance": distance
    }

# Query the data based on intent and entities
def query_data(intent, entities, data):
    if intent == "find":
        query = data
        if entities["constellation"]:
            query = query[query['Constellation'].str.contains('|'.join(entities["constellation"]), case=False, na=False)]
        if entities["distance"]:
            max_distance = int(entities["distance"][0])
            query = query[pd.to_numeric(query['distance(lightyear)'].str.replace(',', ''), errors='coerce') < max_distance]
        return query
    elif intent == "distance" and entities["object"]:
        object_name = entities["object"][0]
        result = data[data['object_name'].str.contains(object_name, case=False, na=False)]
        if not result.empty:
            return f"The distance of {object_name} is {result['distance(lightyear)'].values[0]} light years."
        return f"Object {object_name} not found."
    
    return "I couldn't find an answer to that question."

# Process and answer a natural language question
def process_question(question, data):
    tokenizer, model = load_intent_model()
    intent = classify_intent(question, tokenizer, model)
    entities = extract_entities(question, data)
    return query_data(intent, entities, data)

# Example usage
if __name__ == "__main__":
    windows_path = r"C:\Users\Anaki\OneDrive\Desktop\codingprojects\jwst\JWST-Project\Copy of Dataset - Sheet1 (1).csv"
    data = load_data(windows_path)
    
    questions = [
        "Find galaxies in the Carina constellation under 8000 light years",
        "What is the distance of NGC 604 in Triangulum?",
        "Tell me about Orion objects"
    ]

    for question in questions:
        print(f"Question: {question}")
        answer = process_question(question, data)
        print(f"Answer: {answer}")
