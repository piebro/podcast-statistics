import google.generativeai as genai
import os
from pathlib import Path
import time

prompt = """
In diesem Podcast spielen die Moderatoren zu Beginn ein Spiel, bei dem sie versuchen, Phänomene der Gegenwart zu beschreiben. Einer schlägt ein Phänomen vor, und die anderen beurteilen, ob es tatsächlich ein Gegenwartsphänomen ist. Dabei vergeben sie Punkte je nachdem, ob sie das Phänomen als zeitgenössisch einstufen oder nicht.
Bitte führen Sie folgende Aufgabe aus:
Erstellen Sie eine Liste der besprochenen Phänomene mit folgenden Informationen zu jedem:
 - Wer hat es vorgeschlagen?
 - Eine kurze Beschreibung des Phänomens in 2-3 Sätzen
 - Wer hat dafür oder dagegen gestimmt (einen Punkt vergeben oder nicht)? Dabei ist die Meinung von der Person die das Phänomen vorgeschlagen hat egal.
 - Was war das Endergebnis - wurde es als Gegenwartsphänomen akzeptiert?
Benutze dabei dieses Format:
**Phänomen 1: **
* **Vorgeschlagen von:**
* **Beschreibung:**
* **Dafür:**
* **Dagegen:**
* **Endergebnis:**
"""

# Configure the API
genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO_API"])

# Set up input and output directories
input_dir = Path("audio")
output_dir = Path("gegenwartsspiel_md")
output_dir.mkdir(exist_ok=True)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro-002")

# Process all MP3 files in the input directory
for mp3_file in sorted(input_dir.glob("*.mp3"))[82:]:
    print(f"Processing: {mp3_file.name}")
    
    # Upload the file
    uploaded_file = genai.upload_file(str(mp3_file))
    print("Uploaded file.")
    
    # Generate content
    result = model.generate_content([uploaded_file, prompt])
    
    # Save the output
    output_file = output_dir / f"{mp3_file.stem}.md"
    with open(output_file, "w") as file:
        file.write(result.text)
    
    print(f"Results saved to: {output_file}")
    time.sleep(60) # because of rate limits for the free version

print("All files processed successfully.")