# main.py
import pandas as pd
import llm

# Load data from Windows path or WSL path
def load_data(windows_path):
    wsl_path = '/mnt/c' + windows_path[2:].replace('\\', '/')
    try:
        data = pd.read_csv(wsl_path)
        return data
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        exit(1)

# Search objects by name, constellation, and distance range
def search_object(data, object_name=None, constellation=None, distance_range=None):
    results = data.copy()
    results['distance(lightyear)'] = pd.to_numeric(results['distance(lightyear)'].str.replace(',', ''), errors='coerce')
    
    if object_name:
        results = results[results['object_name'].str.contains(object_name, case=False, na=False)]
    if constellation:
        results = results[results['Constellation'].str.contains(constellation, case=False, na=False)]
    if distance_range:
        min_distance, max_distance = distance_range
        results = results[(results['distance(lightyear)'] >= min_distance) & (results['distance(lightyear)'] <= max_distance)]

    return results

# Main script entry
if __name__ == "__main__":
    windows_path = r"C:\Users\Anaki\OneDrive\Desktop\codingprojects\jwst\JWST-Project\Copy of Dataset - Sheet1 (1).csv"
    data = load_data(windows_path)

    # Display basic data info
    print(data.head())
    print("Unique object names:", data['object_name'].unique())
    print("Unique constellations:", data['Constellation'].unique())
    print("Distance range:", data['distance(lightyear)'].min(), "-", data['distance(lightyear)'].max())

    # Search for NGC 604
    result = search_object(data, object_name="NGC 604", constellation="Triangulum", distance_range=(2000000, 3000000))
    print("Search result for NGC 604:")
    print(result)
    
    # LLM backstory generation (Example)
    tokenizer, model = llm.load_astrollama_model()
    image_data = data.iloc[0]
    backstory = llm.get_backstory_for_image(image_data, tokenizer, model)
    print("Generated Backstory:")
    print(backstory)
