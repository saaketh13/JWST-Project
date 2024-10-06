from flask import Flask, render_template, request, jsonify
from pandas as pd
from llm import load_astrollama_model, get_backstory_for_image
from main import search_object, load_data
from query import process_question


app = Flask(__name__)

windows_path = r"C:\Users\Anaki\OneDrive\Desktop\codingprojects\jwst\JWST-Project\Copy of Dataset - Sheet1 (1).csv"
wsl_path = '/mnt/c' + windows_path[2:].replace('\\', '/')

data = load_data(wsl_path)
tokenizer, model = load_astrollama_model


# Route for searching objects
@app.route('/')
def index():
    return render_template('index.html')

def search():
    object_name = request.json.get('object_name')
    constellation = request.json.get('Constellation')
    distance_range = request.json.get('object_name')
    
