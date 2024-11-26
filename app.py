import streamlit as st
import os
import random
import pygame
import time

# Initialize global quit flag
quit_flag = False

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

def play_music(file):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)  # Play in a loop
    except Exception as e:
        st.error(f"Error playing file {file}: {e}")

def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        st.error(f"Error stopping music: {e}")

def countdown_timer(duration, stage, block, interval, table_placeholder, image_placeholder, exercise=None):
    global quit_flag

    # Image paths for active and rest phases
    active_image_path = "images/eddie.png"
    rest_image_path = "images/dog.png"

    image_placeholder.image(
        active_image_path if stage == "Active" else rest_image_path,
        use_container_width=True,
    )

    for remaining in range(duration, 0, -1):
        if quit_flag:
            st.warning("Timer stopped by user.")
            return False

        # Determine exercise display
        exercise_display = exercise if stage == "Active" else "Breathe"

        # Create the table content as styled HTML
        table_html = f"""
        <table style="width: 100%; text-align: center; border-collapse: collapse; font-size: 24px; font-weight: bold;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 2px solid black; padding: 10px;">Block</th>
                    <th style="border: 2px solid black; padding: 10px;">Interval</th>
                    <th style="border: 2px solid black; padding: 10px;">Active/Rest</th>
                    <th style="border: 2px solid black; padding: 10px;">Time Remaining</th>
                    <th style="border: 2px solid black; padding: 10px;">Exercise</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="border: 2px solid black; padding: 10px;">{block}</td>
                    <td style="border: 2px solid black; padding: 10px;">{interval}</td>
                    <td style="border: 2px solid black; padding: 10px;">{stage}</td>
                    <td style="border: 2px solid black; padding: 10px;">{remaining}s</td>
                    <td style="border: 2px solid black; padding: 10px;">{exercise_display}</td>
                </tr>
            </tbody>
        </table>
        """

        table_placeholder.markdown(table_html, unsafe_allow_html=True)
        time.sleep(1)

    return True

def get_random_file(directory):
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".mp3")]
        if not files:
            raise FileNotFoundError(f"No MP3 files found in directory: {directory}")
        return os.path.join(directory, random.choice(files))
    except Exception as e:
        st.error(f"Error selecting random file from {directory}: {e}")
        return None

def start_tabata(block_minutes, num_blocks, workout_duration, rest_duration, block_rest_duration, active_dir, rest_dir, table_placeholder, image_placeholder):
    global quit_flag
    block_seconds = block_minutes * 60
    interval_duration = workout_duration + rest_duration
    intervals_per_block = block_seconds // interval_duration

    for block_num in range(1, num_blocks + 1):
        workout_music = get_random_file(active_dir)
        rest_music = get_random_file(rest_dir)

        if not workout_music or not rest_music:
            st.error("Error: Could not find music files. Exiting.")
            return

        for interval in range(1, intervals_per_block + 1):
            if quit_flag:
                st.warning("Timer stopped by user.")
                stop_music()
                pygame.mixer.quit()
                return

            # Workout phase
            exercise = random.choice(exercises)
            play_music(workout_music)
            if not countdown_timer(workout_duration, "Active", block_num, interval, table_placeholder, image_placeholder, exercise):
                stop_music()
                pygame.mixer.quit()
                return

            stop_music()

            # Rest phase
            play_music(rest_music)
            if not countdown_timer(rest_duration, "Rest", block_num, interval, table_placeholder, image_placeholder):
                stop_music()
                pygame.mixer.quit()
                return

            stop_music()

        # Rest between blocks
        if block_num < num_blocks:
            play_music(rest_music)
            if not countdown_timer(block_rest_duration, "Rest Between Blocks", block_num, "N/A", table_placeholder, image_placeholder):
                stop_music()
                pygame.mixer.quit()
                return
            stop_music()

    st.success("Tabata session complete! Amazing effort!")
    pygame.mixer.quit()

# Streamlit UI
st.set_page_config(layout="wide")

# Create two columns: one for inputs, one for display
left_col, right_col = st.columns([1, 3])

# Inputs in the left column
with left_col:
    st.title("Tabata!")
    st.write("Configure your Tabata session below:")
    block_minutes = st.number_input("Block Duration (minutes)", min_value=1, max_value=60, value=5)
    num_blocks = st.number_input("Number of Blocks", min_value=1, max_value=10, value=3)
    workout_duration = st.number_input("Workout Duration (seconds)", min_value=10, max_value=300, value=20)
    rest_duration = st.number_input("Rest Duration (seconds)", min_value=5, max_value=300, value=10)
    block_rest_duration = st.number_input("Rest Between Blocks (seconds)", min_value=10, max_value=300, value=60)
    active_dir = st.text_input("Active (Workout) Music Directory", value="active")
    rest_dir = st.text_input("Rest Music Directory", value="rest")

    if st.button("Start Tabata"):
        quit_flag = False
        table_placeholder = right_col.empty()  # Placeholder for dynamic table updates
        image_placeholder = right_col.empty()  # Placeholder for image updates
        start_tabata(
            block_minutes,
            num_blocks,
            workout_duration,
            rest_duration,
            block_rest_duration,
            active_dir,
            rest_dir,
            table_placeholder,
            image_placeholder,
        )

    if st.button("Stop Tabata"):
        quit_flag = True
        stop_music()
        st.warning("Tabata session stopped.")
