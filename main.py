# main.py
import pandas as pd
import query
import llm

windows_path = r"C:\Users\Anaki\OneDrive\Desktop\codingprojects\jwst\JWST-Project\Copy of Dataset - Sheet1 (1).csv"
wsl_path = '/mnt/c' + windows_path[2:].replace('\\', '/')

data = pd.read_csv(wsl_path)
    

# Display the first few rows
print(data.head())

def search_object(data, object_name=None, constellation=None, distance_range=None):
    results = data.copy()
    print(f"Initial data shape: {results.shape}")

    # Convert distance to numeric, replacing non-numeric values with NaN
    results['distance(lightyear)'] = pd.to_numeric(results['distance(lightyear)'].str.replace(',', ''), errors='coerce')
    
    # Filter by object name
    if object_name:
        mask = results['object_name'].str.contains(object_name, case=False, na=False)
        results = results[mask]
        print(f"After object name filter: {results.shape}")
        if results.empty:
            print(f"No matches found for object name: {object_name}")
            return results

    # Filter by constellation
    if constellation:
        mask = results['Constellation'].str.contains(constellation, case=False, na=False)
        results = results[mask]
        print(f"After constellation filter: {results.shape}")
        if results.empty:
            print(f"No matches found for constellation: {constellation}")
            return results

    # Filter by distance range
    if distance_range:
        min_distance, max_distance = distance_range
        mask = (results['distance(lightyear)'] >= min_distance) & (results['distance(lightyear)'] <= max_distance)
        results = results[mask]
        print(f"After distance range filter: {results.shape}")
        if results.empty:
            print(f"No matches found in distance range: {distance_range}")
            return results

    return results

# Print unique values in relevant columns
print("Unique object names:", data['object_name'].unique())
print("Unique constellations:", data['Constellation'].unique())
print("Distance range:", data['distance(lightyear)'].min(), "-", data['distance(lightyear)'].max())

# Search for NGC 604
result = search_object(data, object_name="NGC 604", constellation="Triangulum", distance_range=(2000000, 3000000))
print("Search result for NGC 604:")
print(result)

# If the above search doesn't work, try a more lenient search
if result.empty:
    result = search_object(data, object_name="NGC 604")
    print("Lenient search result for NGC 604:")
    print(result)