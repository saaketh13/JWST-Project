# llm.py
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


windows_path = r"C:\Users\Anaki\OneDrive\Desktop\codingprojects\jwst\JWST-Project\Copy of Dataset - Sheet1 (1).csv"
wsl_path = '/mnt/c' + windows_path[2:].replace('\\', '/')

try:
    data = pd.read_csv(windows_path)
except Exception as e:
    print(f"Error reading the CSV file: {e}")
    exit(1)


#Load up the model
def load_astrollama_model():
    model_name = "AstroMLab/astrollama-2-7b-base_abstract"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

    return tokenizer, model


def generate_backstory(image_data, tokenizer, model):
    #Generate a prompt based on the image data
    prompt = f"Write an engaging background lore about the following astronomical objective:\n"
    prompt += f"Object: {image_data['object_name']}\n"
    prompt += f"Constellation: {image_data['Constellation']}\n"
    prompt += f"Distance: {image_data['distance(lightyear)']} light years\n"
    prompt += f"Provide a detailed background lore using these details. Talk about the creatures that might have inhabited the place. Include the details that you know.."


    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, max_length=200, do_sample=True, temperature =0.7)
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens = True)

    return generated_text

# Exampple backstory generation for a specific image
def get_backstory_for_image(image_metadata, tokenizer, model):
    backstory = generate_backstory(image_metadata, tokenizer, model)
    return backstory

tokenizer, model = load_astrollama_model()

data = pd.read_csv(wsl_path)

# Select an image (example based on first row, can be modified)
image_data = data.iloc[0]  # Get data from the first row (modify based on user selection)

# Generate and print backstory
backstory = get_backstory_for_image(image_data, tokenizer, model)
print("Generated Backstory:")
print(backstory)
