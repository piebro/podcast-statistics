import google.generativeai as genai
import os
from pathlib import Path

prompt = """
Bitte erstellen Sie eine umfassende Zusammenfassung dieser Podcast-Episode. Die Zusammenfassung sollte Folgendes enthalten:

1. Hauptthemen: Welche Hauptthemen werden in dieser Episode besprochen?
2. Kernaussagen: Was sind die wichtigsten Punkte oder Erkenntnisse zu jedem Thema?
3. Diskussionsverlauf: Wie entwickelt sich die Diskussion? Gibt es interessante Wendungen oder Meinungsverschiedenheiten?
4. Gäste (falls vorhanden): Wer sind die Gäste und was tragen sie zur Diskussion bei?
5. Schlussfolgerungen: Welche Schlüsse werden am Ende gezogen?
6. Besondere Momente: Gibt es humorvolle, kontroverse oder besonders aufschlussreiche Momente?

Bitte strukturieren Sie die Zusammenfassung in klare Abschnitte und verwenden Sie Aufzählungspunkte, wo es angemessen ist. Die Zusammenfassung sollte etwa 500-700 Wörter lang sein und einen guten Überblick über den gesamten Inhalt der Episode geben.
"""

# Configure the API
genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO_API"])

# Set the input file path and output directory
input_file = Path("audio/2024_08_26_Wie_lange_geht_Party_Girl_Forever.mp3")
output_dir = Path("zusammenfassungen")
output_dir.mkdir(exist_ok=True)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro-002")

if not input_file.exists():
    print(f"Error: File '{input_file}' not found.")
else:
    print(f"Processing: {input_file.name}")
    
    # Upload the file
    uploaded_file = genai.upload_file(str(input_file))
    print("Uploaded file.")
    
    # Generate content
    result = model.generate_content([uploaded_file, prompt])
    
    # Save the output
    output_file = output_dir / f"{input_file.stem}_summary.md"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(result.text)
    print(f"Summary saved to: {output_file}")

print("Processing complete.")