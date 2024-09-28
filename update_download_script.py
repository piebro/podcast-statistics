import re
import requests
from bs4 import BeautifulSoup

def download_zeit_podcasts(url, wget_commands):
    """Downloads ZEIT ONLINE podcast MP3 files using wget."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        html_content = response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    for audio_player in soup.find_all('div', class_='audio-player'):
        audio_tag = audio_player.find('audio')
        if audio_tag:
            try:
                title = audio_player.find_previous('h3').find('span', class_='zon-teaser__title').text.strip()
                date_str = audio_player.find_previous('time').get('datetime').split('T')[0]
                date = date_str.replace('-', '_')  # Modify date format to avoid issues with filenames
                # Sanitize filenames for shell safety
                safe_title = re.sub(r'[^\w\s-]', '', title)
                safe_title = safe_title.replace(' ', '_')
                ad_free_src = audio_tag.get('data-src-adfree')
                src = audio_tag.get('data-src')
                filename = f"{date}_{safe_title}.mp3"
                if ad_free_src:
                    wget_commands.append(f"wget -O 'audio/{filename}' '{ad_free_src}'")
                elif src:
                    wget_commands.append(f"wget -O 'audio/{filename}' '{src}'")
            except AttributeError as e:
                print(f"Error parsing audio element: {e}")
                continue  # Skip to the next audio player if parsing fails

def main():
    wget_commands = []
    urls = [
        "https://www.zeit.de/serie/die-sogenannte-gegenwart",
        "https://www.zeit.de/serie/die-sogenannte-gegenwart?p=2",
        "https://www.zeit.de/serie/die-sogenannte-gegenwart?p=3",
        "https://www.zeit.de/serie/die-sogenannte-gegenwart?p=4"
    ]

    for url in urls:
        download_zeit_podcasts(url, wget_commands)

    with open("download_all_episodes.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#Generated wget commands for downloading Zeit Online podcast episodes\n\n")
        f.write("mkdir -p audio\n\n")
        f.write("\n".join(wget_commands))
        f.write("\n")

    print("Shell script 'download_all_episodes.sh' has been created.")

if __name__ == "__main__":
    main()