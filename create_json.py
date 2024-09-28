import google.generativeai as genai
import os
import json
from pathlib import Path
import typing_extensions as typing
import re
import time
from typing import Literal

# Define the allowed names
AllowedNames = Literal["Ijoma", "Lars", "Nina", "Zuhörer/Publikum/Gast"]

# Define the structure for our podcast data
class PodcastEpisode(typing.TypedDict):
    Vorgeschlagen_von: AllowedNames
    Beschreibung: str
    Dafür: list[AllowedNames]
    Dagegen: list[AllowedNames]
    Endergebnis: bool

# Configure the API
genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO_API"])

# Set up input and output directories
input_dir = Path("gegenwartsspiel_md")
output_dir = Path("gegenwartsspiel_json")
output_dir.mkdir(exist_ok=True)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-002")

# Function to extract date and title from filename
def extract_info_from_filename(filename):
    match = re.match(r"(\d{4})_(\d{2})_(\d{2})_(.+)\.md", filename)
    if match:
        year, month, day, title = match.groups()
        date = f"{year}-{month}-{day}"
        title = title.replace("_", " ")
        return date, title
    return None, None

# Prompt template
prompt_template = """
Konvertiere die folgende Markdown-Liste von Podcast-Episoden in eine JSON-Liste. Beachte dabei:
- Eine Überschrift ist immer ein Phänomen und damit einen JSON Objekt.
- Jedes Phänomen MUSS alle folgenden Felder enthalten:
  - "Vorgeschlagen_von": Nur "Ijoma", "Lars", "Nina", oder "Zuhörer/Publikum/Gast" sind erlaubt.
  - "Beschreibung": Eine kurze Beschreibung des vorgeschlagenen Phänomens.
  - "Dafür": Eine Liste von Namen (nur "Ijoma", "Lars", "Nina", oder "Zuhörer/Publikum/Gast").
  - "Dagegen": Eine Liste von Namen (nur "Ijoma", "Lars", "Nina", oder "Zuhörer/Publikum/Gast").
  - "Endergebnis": "true" wenn das Phänomen akzeptiert wurde, sonst "false".
- Alle Felder müssen ausgefüllt sein.
- Die Listen "Dafür" und "Dagegen" dürfen leer sein, aber müssen immer als Listen vorhanden sein.

Ein Beispiel für eine Ausgabe sieht so aus:

[
  {{
    "Beschreibung": "Der Kompostwurm ist nicht nur ein simples Tier im Garten, sondern ein Lifestyle-Objekt. Es geht um den \\"Wurmhumus\\", der durch den Mistwurm entsteht und als hochwertiger Dünger verkauft wird, aber auch um das ganze Set und den Wurm selbst.  Der Kompostwurm wird zum Gegenstand von Gesprächen und Statussymbol.",
    "Dafür": [
      "Ijoma"
    ],
    "Dagegen": [],
    "Endergebnis": true,
    "Vorgeschlagen_von": "Nina",
    "Datum": "2021-10-04",
    "Episode": "Ist Schönheit sexistisch"
  }},
  {{
    "Beschreibung": "Seit Kurzem können auf Twitter Micropayments via Bitcoin mit dem Lightning-Netzwerk abgewickelt werden. Das ermöglicht u.a. das \\"Tippen\\" von Tweets und wird als zukünftig revolutionär für die Monetarisierung von Inhalten, insbesondere in der Podcast-Industrie, eingeschätzt.",
    "Dafür": [
      "Nina"
    ],
    "Dagegen": [],
    "Endergebnis": true,
    "Vorgeschlagen_von": "Ijoma",
    "Datum": "2021-10-04",
    "Episode": "Ist Schönheit sexistisch"
  }},
  {{
    "Beschreibung": "Die populärste Form der Selbsttherapie besteht darin, die eigenen (meist negativen) Glaubenssätze zu finden, zu hinterfragen und umzucodieren. Dieser Ansatz wird in allen Lebensbereichen, besonders in der Selbsthilfe, angewendet und als Weg zur Heilung propagiert.",
    "Dafür": [
      "Ijoma"
    ],
    "Dagegen": [],
    "Endergebnis": true,
    "Vorgeschlagen_von": "Nina",
    "Datum": "2021-10-04",
    "Episode": "Ist Schönheit sexistisch"
  }}
]

Hier ist der Markdown-Inhalt:

{markdown_content}
"""

# Function to validate the JSON data
def validate_json_data(json_data):
    allowed_names = {"Ijoma", "Lars", "Nina", "Zuhörer/Publikum/Gast"}
    valid_data = []
    for idea in json_data:
        # Check if all required fields are present
        required_fields = ["Vorgeschlagen_von", "Beschreibung", "Dafür", "Dagegen", "Endergebnis"]
        if not all(field in idea for field in required_fields):
            print(f"Error: Incomplete data - missing fields: {idea}")
            continue

        # Validate and correct the values
        if idea['Vorgeschlagen_von'] not in allowed_names:
            idea['Vorgeschlagen_von'] = "Zuhörer/Publikum/Gast"
        idea['Dafür'] = [name if name in allowed_names else "Zuhörer/Publikum/Gast" for name in idea['Dafür']]
        idea['Dagegen'] = [name if name in allowed_names else "Zuhörer/Publikum/Gast" for name in idea['Dagegen']]
        
        # Ensure Endergebnis is a boolean
        idea['Endergebnis'] = idea['Endergebnis'] in [True, 'true', 'True']

        # Add the validated idea to the list
        valid_data.append(idea)
    
    return valid_data

# Process each .md file in the input directory
for md_file in sorted(input_dir.glob("*.md")):
    print(f"Processing file: {md_file.name}")
    # Extract date and title from filename
    date, title = extract_info_from_filename(md_file.name)
    if not date or not title:
        print(f"Warning: Couldn't extract date and title from {md_file.name}. Skipping this file.")
        continue

    # Read the Markdown file
    with open(md_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # Combine prompt and markdown content
    full_prompt = prompt_template.format(markdown_content=markdown_content)

    # Generate content with JSON mode
    result = model.generate_content(
        full_prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[PodcastEpisode]
        ),
    )

    # Parse the JSON response
    try:
        json_data = json.loads(result.text)
        # Validate and correct the JSON data
        valid_json_data = validate_json_data(json_data)
        
        if not valid_json_data:
            print(json_data)
            print(f"Error: No valid data found in {md_file.name}. Skipping this file.")
            continue

        # Add date and title to each episode
        for episode in valid_json_data:
            episode['Datum'] = date
            episode['Episode'] = title

        # Save the output
        output_file = output_dir / f"{md_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(valid_json_data, file, ensure_ascii=False, indent=2)
        print(f"Results saved to: {output_file}")
    except json.JSONDecodeError:
        print(f"Error processing {md_file.name}: The API response couldn't be parsed as JSON. Here's the raw response:")
        print(result.text)

    time.sleep(30)  # a little delay because of rate limits in the free tier

print("Processing completed.")