import os
import json
import pandas as pd

def get_first_name(full_name):
    # Dictionary mapping full names to first names
    name_mapping = {
        "Ijoma Mangold": "Ijoma",
        "Lars Weisbrod": "Lars",
        "Nina Pauer": "Nina"
    }
    
    # Return the first name if it's in our mapping, otherwise return the original name
    return name_mapping.get(full_name, full_name)

def process_names(item):
    # Process "Dafür" and "Dagegen" lists
    for field in ['Dafür', 'Dagegen']:
        if field in item:
            item[field] = [get_first_name(name) for name in item[field]]
    
    # Process "Vorgeschlagen_von"
    if 'Vorgeschlagen_von' in item:
        item['Vorgeschlagen_von'] = get_first_name(item['Vorgeschlagen_von'])
    
    return item

def load_json_files(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                counter = 1
                for item in data:
                    item['Nummer'] = counter
                    counter += 1
                    item = process_names(item)
                if counter > 10:
                    print(f"{filename} hat {counter} Vorschläge, passt das?")
                all_data.extend(data)
    
    df = pd.DataFrame(all_data)
    return df

# Usage
folder_path = 'gegenwartsspiel_json'
result_df = load_json_files(folder_path)

# Optional: Save the DataFrame to a CSV file
result_df.to_csv('results.csv', index=False)