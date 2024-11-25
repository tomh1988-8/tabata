import time
import pygame
import keyboard  # For detecting keypresses
import os
import random  # For selecting random MP3 files

# Global flag to indicate if the user wants to quit
quit_flag = False

def play_music(file):
    """
    Play the music file using pygame in a loop.
    :param file: Path to the audio file.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)  # Play in a loop
    except Exception as e:
        print(f"Error playing file {file}: {e}")

def stop_music():
    """
    Stop the music playback.
    """
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Error stopping music: {e}")

def countdown_timer(duration, message):
    """
    Countdown timer for the specified duration with responsiveness to 'q'.
    :param duration: Duration of the countdown in seconds.
    :param message: Message to display during the countdown.
    :return: True if the timer completed, False if 'q' was pressed to quit.
    """
    global quit_flag
    for remaining in range(duration, 0, -1):
        if quit_flag:  # Check if quit flag is set
            print("\nTimer stopped by user. Goodbye!")
            return False
        print(f"{message}: {remaining}s", end="\r")
        time.sleep(1)
    return True

def get_random_file(directory):
    """
    Get a random MP3 file from the specified directory.
    :param directory: Path to the directory containing MP3 files.
    :return: Full path to a random MP3 file.
    """
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".mp3")]
        if not files:
            raise FileNotFoundError(f"No MP3 files found in directory: {directory}")
        return os.path.join(directory, random.choice(files))
    except Exception as e:
        print(f"Error selecting random file from {directory}: {e}")
        return None

def tabata_block_timer(block_minutes, num_blocks, workout_duration, rest_duration, block_rest_duration, active_dir, rest_dir):
    """
    Tabata timer with configurable blocks, workout/rest durations, and music.
    
    :param block_minutes: Length of each block in minutes (must be a whole number).
    :param num_blocks: Number of blocks.
    :param workout_duration: Duration of the workout phase in seconds.
    :param rest_duration: Duration of the rest phase in seconds.
    :param block_rest_duration: Duration of the rest between blocks in seconds.
    :param active_dir: Path to the directory containing workout music files.
    :param rest_dir: Path to the directory containing rest music files.
    """
    global quit_flag
    block_seconds = block_minutes * 60
    interval_duration = workout_duration + rest_duration
    intervals_per_block = block_seconds // interval_duration

    print("Starting Tabata Timer! (Press 'q' to quit at any time.)")

    # Set up a hotkey for quitting the timer
    keyboard.add_hotkey('q', lambda: set_quit_flag())

    for block_num in range(1, num_blocks + 1):
        print(f"\n--- Block {block_num}/{num_blocks} ---")

        # Randomly select workout and rest music files for this block
        workout_music = get_random_file(active_dir)
        rest_music = get_random_file(rest_dir)

        if not workout_music or not rest_music:
            print("Error: Could not find music files. Exiting.")
            return

        for interval in range(1, intervals_per_block + 1):
            if quit_flag:  # Check if quit flag is set
                print("\nTimer stopped by user. Goodbye!")
                stop_music()
                pygame.mixer.quit()
                return

            print(f"\nInterval {interval}/{intervals_per_block}: Workout! (Press 'q' to quit)")
            play_music(workout_music)

            if not countdown_timer(workout_duration, "Workout Time Left"):
                stop_music()
                pygame.mixer.quit()
                return

            stop_music()  # Stop workout music
            print("\nTime to Rest! (Press 'q' to quit)")
            play_music(rest_music)

            if not countdown_timer(rest_duration, "Rest Time Left"):
                stop_music()
                pygame.mixer.quit()
                return

            stop_music()  # Stop rest music

        # Rest between blocks
        if block_num < num_blocks:  # No rest after the final block
            print("\n--- Rest Between Blocks ---")
            play_music(rest_music)
            if not countdown_timer(block_rest_duration, "Block Rest Time Left"):
                stop_music()
                pygame.mixer.quit()
                return
            stop_music()

    print("\nTabata session complete! Amazing effort!")
    pygame.mixer.quit()  # Clean up pygame mixer

def set_quit_flag():
    """
    Set the global quit flag to True.
    """
    global quit_flag
    quit_flag = True

# Configure your Tabata session
BLOCK_MINUTES = 5          # Length of each block in minutes (must be a whole number)
NUM_BLOCKS = 3             # Number of blocks
WORKOUT_DURATION = 20      # seconds
REST_DURATION = 10         # seconds
BLOCK_REST_DURATION = 60   # seconds (1 minute rest between blocks)

# Paths to your music directories
ACTIVE_DIR = "active"  # Replace with the path to your active (workout) music folder
REST_DIR = "rest"      # Replace with the path to your rest music folder

# Start the Tabata timer
tabata_block_timer(BLOCK_MINUTES, NUM_BLOCKS, WORKOUT_DURATION, REST_DURATION, BLOCK_REST_DURATION, ACTIVE_DIR, REST_DIR)
