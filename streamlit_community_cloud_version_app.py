import streamlit as st
import random
import time

# Base GitHub URL for accessing raw files
GITHUB_BASE_URL = "https://raw.githubusercontent.com/tomh1988-8/tabata/main/"

# Paths for Active and Rest Music
ACTIVE_MUSIC_PATH = GITHUB_BASE_URL + "active/"
REST_MUSIC_PATH = GITHUB_BASE_URL + "rest/"

# List of exercises
exercises = [
    "Push-Ups", "Sit-Ups", "V-Ups", "Squats", "Front Lunges",
    "Back Lunges", "Star Jumps", "Burpees", "Plank",
    "KB Swings", "KB Goblet Squats",
    "KB Deadlifts", "KB Cleans (Alternating)",
    "KB Snatches (Alternating)", "KB Farmer's Carry",
    "KB Overhead Press (Alternating)", "Mountain Climbers",
    "Jump Squats", "Bicycle Crunches"
]

# Updated list of active phase MP3 files
ACTIVE_FILES = [
    "80s-style-thrash-metal-track-short-version-261517.mp3",
    "80s-thrash-metal-track-retro-heavy-metal-energy-263548.mp3",
    "a-hero-of-the-80s-126684.mp3",
    "fibonacci-heavy-thrash-metal-instrumental-262792.mp3",
    "intense-nu-metal-thrash-fusion-battle-of-lepanto-258047.mp3",
    "lady-of-the-80x27s-128379.mp3",
    "round1.mp3",
    "round2.mp3",
    "round3.mp3",
    "short-thrash-metal-instrumental-265084.mp3",
    "very-heavy-melodic-metal-instrumental-236531.mp3"
]

# Placeholder for rest MP3 files (update with actual filenames from the rest folder)
REST_FILES = [
    "rest1.mp3"
]

# Helper Functions
def get_random_file(file_list, base_url):
    """Get a random file URL from a list of files in the GitHub repository."""
    return base_url + random.choice(file_list)

def countdown_timer(duration, stage, block, interval, exercise=None):
    """Run a countdown timer and display progress."""
    for remaining in range(duration, 0, -1):
        st.write(f"**Block {block} | Interval {interval} | {stage}**")
        st.write(f"Time Remaining: **{remaining}s**")
        st.write(f"Exercise: **{exercise if stage == 'Active' else 'Breathe'}**")
        time.sleep(1)

def play_audio(file_url):
    """Stream audio in the browser using Streamlit."""
    if file_url:
        st.audio(file_url)

def start_tabata(block_minutes, num_blocks, workout_duration, rest_duration, block_rest_duration):
    """Run the full Tabata session."""
    block_seconds = block_minutes * 60
    interval_duration = workout_duration + rest_duration
    intervals_per_block = block_seconds // interval_duration

    for block_num in range(1, num_blocks + 1):
        workout_music = get_random_file(ACTIVE_FILES, ACTIVE_MUSIC_PATH)
        rest_music = get_random_file(REST_FILES, REST_MUSIC_PATH)

        if not workout_music or not rest_music:
            st.error("Error: Could not find music files. Exiting.")
            return

        for interval in range(1, intervals_per_block + 1):
            # Workout Phase
            exercise = random.choice(exercises)
            st.subheader(f"Active Phase: Block {block_num}, Interval {interval}")
            play_audio(workout_music)
            countdown_timer(workout_duration, "Active", block_num, interval, exercise)

            # Rest Phase
            st.subheader(f"Rest Phase: Block {block_num}, Interval {interval}")
            play_audio(rest_music)
            countdown_timer(rest_duration, "Rest", block_num, interval)

        # Rest Between Blocks
        if block_num < num_blocks:
            st.subheader(f"Rest Between Blocks: Block {block_num}")
            play_audio(rest_music)
            countdown_timer(block_rest_duration, "Rest Between Blocks", block_num, "N/A")

    st.success("Tabata session complete! Amazing effort!")

# Streamlit App UI
st.set_page_config(layout="wide")

st.title("It's Tabata Time!")
st.write("Configure your Tabata session below:")

# Inputs
block_minutes = st.number_input("Block Duration (minutes)", min_value=1, max_value=60, value=5)
num_blocks = st.number_input("Number of Blocks", min_value=1, max_value=10, value=3)
workout_duration = st.number_input("Workout Duration (seconds)", min_value=10, max_value=300, value=20)
rest_duration = st.number_input("Rest Duration (seconds)", min_value=5, max_value=300, value=10)
block_rest_duration = st.number_input("Rest Between Blocks (seconds)", min_value=10, max_value=300, value=60)

if st.button("Start Tabata"):
    st.info("Starting Tabata session...")
    start_tabata(
        block_minutes,
        num_blocks,
        workout_duration,
        rest_duration,
        block_rest_duration,
    )
