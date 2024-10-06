# llm.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer
def load_astrollama_model():
    model_name = "AstroMLab/astrollama-2-7b-base_abstract"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
    return tokenizer, model

# Generate backstory based on image data
def generate_backstory(image_data, tokenizer, model):
    prompt = (
        f"Write an engaging background lore about the following astronomical object:\n"
        f"Object: {image_data['object_name']}\n"
        f"Constellation: {image_data['Constellation']}\n"
        f"Distance: {image_data['distance(lightyear)']} light years\n"
        "Provide a detailed background lore using these details. Talk about the creatures that might have inhabited the place."
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, max_length=200, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Wrapper function to get backstory for a given image
def get_backstory_for_image(image_metadata, tokenizer, model):
    return generate_backstory(image_metadata, tokenizer, model)
