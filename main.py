import requests
import pygame
import time
import json  # Use 'csv' or 'json' depending on the file format

# Replace with your raw GitHub URL and the path to your music file
GITHUB_RAW_URL = 'https://raw.githubusercontent.com/yalli09/Schoolv/refs/heads/main/state.txt'
MUSIC_PATH = 'song.mp3'

# Initialize pygame mixer to play music
pygame.mixer.init()

# Flag to track if music is playing
music_playing = False

def play_music():
    global music_playing
    if not music_playing:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        music_playing = True
        print("Music is now playing...")

def stop_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False
        print("Music has stopped.")

def check_file():
    previous_status = None  # To track previous status value

    while True:
        try:
            # Fetch the raw content from the GitHub page
            response = requests.get(GITHUB_RAW_URL)
            response.raise_for_status()  # Check if the request was successful

            # Assuming the file is a JSON file, parse it
            data = response.json()  # If it's a CSV file, use csv.reader

            # Check if '1' is in the file
            if isinstance(data, list):
                current_status = None
                for row in data:
                    if row.get('status') == 1:  # Example check for a row with 'status' key
                        current_status = 1
                        break
                else:
                    current_status = 0

                # If status is 1 and the previous status was not 1, play music
                if current_status == 1 and previous_status != 1:
                    play_music()

                # If status is 0 and the previous status was not 0, stop music
                if current_status == 0 and previous_status != 0:
                    stop_music()

                # Update previous status
                previous_status = current_status

            # Wait for a bit before checking again (e.g., check every 10 seconds)
            time.sleep(10)

        except requests.RequestException as e:
            print(f"Error fetching the file: {e}")
            time.sleep(10)  # Retry after a delay

if __name__ == "__main__":
    check_file()
