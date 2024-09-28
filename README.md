# Statistics about the Zeit Podcast: Die sogennant Gegenwart.

Statistics about the Podcast: "Die sogennant Gegenwart". In each episode they play a small game in the beginning. Using an LLM API, I extracted short descriptiones and the scores of each game and aggregated them for some interesting statistics.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-generativeai beautifulsoup4 pandas matplotlib tabulate
```

## Usage

The code is writen for Linux but with a few adjustments it should work on Windows and MacOS too.

```bash
# update the download script
python3 update_download_script.py

# run the download script
bash download_all_episodes.sh

# answer questions about each episode in the "audio" folder using gemini
python3 answer_questions_from_audio.py

# create a .json for each .md file in gegenwartsspiel_md using gemini
python3 create_json.py

# create a the results.csv table with all the results
python3 create_results_csv.py

# create all plots and statistics
python3 create_plots.py
```

## Prompt for new "Gegenwartsphänomenen"

```
# Prompt zur Generierung von Gegenwartsphänomenen

Erstelle eine Liste von 5-7 fiktiven, aber plausiblen Gegenwartsphänomenen, die aktuelle Trends, gesellschaftliche Entwicklungen oder kulturelle Veränderungen widerspiegeln. Orientiere dich dabei an folgenden Richtlinien:

1. Zeitrahmen: Die Phänomene sollten in der nahen Gegenwart (bis zu 6 Monate in der Zukunft) angesiedelt sein.

2. Themenbereiche: Berücksichtige verschiedene Aspekte wie Technologie, Soziales, Kultur, Arbeitswelt, Konsum, Sprache oder Gesundheit.

3. Detailtiefe: Beschreibe jedes Phänomen in 2-3 Sätzen. Erkläre kurz, worin es besteht und warum es relevant ist.

4. Realitätsnähe: Die Phänomene sollten zwar fiktiv, aber glaubwürdig und an reale Trends angelehnt sein.

5. Innovationsgrad: Versuche, überraschende oder unerwartete Entwicklungen zu erfassen, die dennoch im Bereich des Möglichen liegen.

6. Stil: Verwende einen sachlichen, leicht journalistischen Ton, ähnlich wie in der Vorlage.

7. Format: Gib jedem Phänomen ein fiktives Datum (im Format JJJJ-MM-TT) und eine kurze Beschreibung.

Beispiel:
"2024-10-07: Ein neuer Trend in der Musikindustrie sieht vor, dass Künstler ihre Songs in verschiedenen Versionen veröffentlichen, die auf die Akustik spezifischer Kopfhörermodelle optimiert sind. Dies führt zu einer engeren Zusammenarbeit zwischen Musikern und Kopfhörerherstellern."

Erstelle nun eine Liste von Gegenwartsphänomenen nach diesem Muster.
```

Und die Antwort von Opus-3.0

```
Hier ist eine Liste von fiktiven, aber plausiblen Gegenwartsphänomenen:

2024-10-02: In immer mehr Städten entstehen "Coworking-Cafés", die tagsüber als klassischer Coworking-Space und abends als Café oder Bar fungieren. Dieses Konzept ermöglicht eine effiziente Raumnutzung und fördert die Vernetzung zwischen Berufstätigen und der lokalen Gemeinschaft.

2024-09-18: Virtuelle Influencer, die durch KI gesteuert werden, gewinnen auf Social-Media-Plattformen an Popularität. Unternehmen nutzen diese digitalen Persönlichkeiten, um ihre Produkte zu bewerben und mit Zielgruppen zu interagieren, ohne auf reale Menschen angewiesen zu sein.

2024-11-05: Ein neuer Gesundheitstrend namens "Micro-Mindfulness" setzt auf kurze, gezielte Achtsamkeitsübungen, die sich leicht in den Alltag integrieren lassen. Smartphone-Apps und Wearables erinnern Nutzer daran, regelmäßig innezuhalten und sich auf den Moment zu konzentrieren.

2024-10-20: In der Modeindustrie setzen sich "Slow Fashion Circles" durch - Gruppen von Verbrauchern, die hochwertige Kleidungsstücke gemeinsam besitzen und untereinander tauschen. Dieses Konzept reduziert den individuellen Konsum, ohne auf vielseitige Garderobe verzichten zu müssen.

2024-09-28: Immer mehr Unternehmen bieten ihren Mitarbeitern "Kreativitäts-Stipendien" an, die es ihnen ermöglichen, für einige Wochen oder Monate an eigenen Projekten zu arbeiten. Diese Initiativen sollen Innovation fördern und die Mitarbeiterzufriedenheit steigern.

2024-11-12: In der Gastronomie etablieren sich "Mystery-Menüs", bei denen Gäste nicht wissen, welche Gerichte sie serviert bekommen. Stattdessen werden die Menüs auf Basis von individuellen Geschmacksprofilen und Präferenzen der Gäste zusammengestellt, die vorab erfasst werden.

2024-10-15: Ein neues soziales Netzwerk namens "Narrativ" ermöglicht es Nutzern, ihre Lebensgeschichten in Form von multimedialen Zeitleisten zu teilen. Die Plattform legt Wert auf Authentizität und tiefgründige Interaktionen, um oberflächlichen Content zu vermeiden.
```

Und hier eine von Sonnet-3.5

```
Hier ist eine Liste von 6 fiktiven, aber plausiblen Gegenwartsphänomenen, die aktuelle Trends und Entwicklungen widerspiegeln:

2024-05-20: "Micro-Mentoring" etabliert sich als neue Form der beruflichen Weiterentwicklung. Arbeitnehmer buchen 15-minütige Online-Sessions mit Experten verschiedener Branchen, um punktuell Wissen und Erfahrungen auszutauschen. Diese Kurzberatungen ermöglichen eine flexible und effiziente Weiterbildung im Arbeitsalltag.

2024-06-30: Der Trend zu "Silent Restaurants" breitet sich in Großstädten aus. Diese Lokale bieten Gästen eine Umgebung ohne Hintergrundmusik oder laute Gespräche, um dem zunehmenden Bedürfnis nach Ruhe und Achtsamkeit beim Essen gerecht zu werden. Besucher kommunizieren über Tablets oder Handzeichen mit dem Personal.

2024-07-15: "Augmented Reality Graffiti" revolutioniert die Straßenkunst. Künstler platzieren digitale Kunstwerke an realen Orten, die nur über spezielle AR-Apps sichtbar sind. Diese Technik ermöglicht eine neue Form des urbanen Ausdrucks, ohne öffentliches Eigentum zu beschädigen.

2024-08-22: "Eco-Sleep" wird zum neuen Gesundheitstrend. Hotels und Privathaushalte richten Schlafzimmer mit speziellen Luftfiltern, natürlichen Materialien und biophilen Designelementen ein, um die Schlafqualität zu verbessern und gleichzeitig den ökologischen Fußabdruck zu reduzieren.

2024-09-10: "Flavor Syncing" etabliert sich als innovative Marketingstrategie in der Lebensmittelindustrie. Unternehmen synchronisieren die Geschmacksprofile ihrer Produkte mit populären Streaming-Inhalten, um ein immersives Geschmackserlebnis beim Medienkonsum zu schaffen.

2024-10-01: "Digital Detox Zones" werden in öffentlichen Räumen eingerichtet. Diese speziell abgeschirmten Bereiche in Parks, Bibliotheken und Cafés blockieren alle digitalen Signale, um Menschen einen Rückzugsort von der ständigen Online-Präsenz zu bieten und die Face-to-Face-Kommunikation zu fördern.
```

## License

All code in this project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.