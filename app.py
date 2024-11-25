import streamlit as st
import os
import random
import pygame
import time
import pandas as pd  # For creating and styling the dynamic table

# Initialize global quit flag
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
        st.error(f"Error playing file {file}: {e}")

def stop_music():
    """
    Stop the music playback.
    """
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        st.error(f"Error stopping music: {e}")

def countdown_timer(duration, stage, block, interval, table_placeholder):
    """
    Countdown timer for the specified duration with dynamic table updates.
    :param duration: Duration of the countdown in seconds.
    :param stage: Current stage (Workout/Rest).
    :param block: Current block number.
    :param interval: Current interval number.
    :param table_placeholder: Streamlit placeholder for dynamic table updates.
    :return: True if the timer completed, False if 'q' was pressed to quit.
    """
    global quit_flag

    # Dynamic table update
    for remaining in range(duration, 0, -1):
        if quit_flag:
            st.warning("Timer stopped by user.")
            return False

        # Create the table content as styled HTML
        table_html = f"""
        <table style="width: 100%; text-align: center; border-collapse: collapse; font-size: 24px; font-weight: bold;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 2px solid black; padding: 10px;">Block</th>
                    <th style="border: 2px solid black; padding: 10px;">Interval</th>
                    <th style="border: 2px solid black; padding: 10px;">Active/Rest</th>
                    <th style="border: 2px solid black; padding: 10px;">Time Remaining</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="border: 2px solid black; padding: 10px;">{block}</td>
                    <td style="border: 2px solid black; padding: 10px;">{interval}</td>
                    <td style="border: 2px solid black; padding: 10px;">{stage}</td>
                    <td style="border: 2px solid black; padding: 10px;">{remaining}s</td>
                </tr>
            </tbody>
        </table>
        """

        # Update the table in the Streamlit UI
        table_placeholder.markdown(table_html, unsafe_allow_html=True)

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
        st.error(f"Error selecting random file from {directory}: {e}")
        return None

def start_tabata(block_minutes, num_blocks, workout_duration, rest_duration, block_rest_duration, active_dir, rest_dir, table_placeholder):
    """
    Start the Tabata timer with the specified parameters.
    """
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
            play_music(workout_music)
            if not countdown_timer(workout_duration, "Active", block_num, interval, table_placeholder):
                stop_music()
                pygame.mixer.quit()
                return

            stop_music()

            # Rest phase
            play_music(rest_music)
            if not countdown_timer(rest_duration, "Rest", block_num, interval, table_placeholder):
                stop_music()
                pygame.mixer.quit()
                return

            stop_music()

        # Rest between blocks
        if block_num < num_blocks:
            play_music(rest_music)
            if not countdown_timer(block_rest_duration, "Rest Between Blocks", block_num, "N/A", table_placeholder):
                stop_music()
                pygame.mixer.quit()
                return
            stop_music()

    st.success("Tabata session complete! Amazing effort!")
    pygame.mixer.quit()

# Streamlit UI
st.set_page_config(layout="wide")  # Enable wide layout

# Create two columns: one for inputs, one for display
left_col, right_col = st.columns([1, 3])  # Adjusted column ratio for narrower inputs

# Inputs in the left column
with left_col:
    st.title("Tabata Timer")
    st.write("Configure your Tabata session below:")
    with st.container():
        block_minutes = st.number_input("Block Duration (minutes)", min_value=1, max_value=60, value=5)
    with st.container():
        num_blocks = st.number_input("Number of Blocks", min_value=1, max_value=10, value=3)
    with st.container():
        workout_duration = st.number_input("Workout Duration (seconds)", min_value=10, max_value=300, value=20)
    with st.container():
        rest_duration = st.number_input("Rest Duration (seconds)", min_value=5, max_value=300, value=10)
    with st.container():
        block_rest_duration = st.number_input("Rest Between Blocks (seconds)", min_value=10, max_value=300, value=60)

    # Directories for music
    with st.container():
        active_dir = st.text_input("Active (Workout) Music Directory", value="active")
    with st.container():
        rest_dir = st.text_input("Rest Music Directory", value="rest")

    # Start/Stop buttons
    if st.button("Start Tabata"):
        quit_flag = False
        table_placeholder = right_col.empty()  # Placeholder for dynamic table updates
        start_tabata(
            block_minutes,
            num_blocks,
            workout_duration,
            rest_duration,
            block_rest_duration,
            active_dir,
            rest_dir,
            table_placeholder,
        )

    if st.button("Stop Tabata"):
        quit_flag = True
        stop_music()
        st.warning("Tabata session stopped.")
