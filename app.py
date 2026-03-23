import streamlit as st
import tempfile
import os
import matplotlib.pyplot as plt
import librosa
import numpy as np

from pitch import extract_pitch_contour, pitch_stats
from harmonium import NOTE_MAP, get_closest_note, contour_to_notes
from audio_utils import generate_harmonium_sequence, save_audio

st.set_page_config(page_title="AI Harmonium Converter", layout="centered")
st.title("🎹 AI Voice → Harmonium Converter")
st.write("Upload your voice and convert it into a realistic harmonium melody.")

audio = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"])

if audio is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio.read())
        temp_audio_path = tmp_file.name

    # Load and display audio player
    st.audio(temp_audio_path, format="audio/wav")

    # Extract pitch contour
    with st.spinner("Analyzing pitch..."):
        try:
            times, pitches = extract_pitch_contour(temp_audio_path)
        except Exception as e:
            st.error(f"Error processing audio: {e}")
            st.stop()

    # Statistics
    low, high, avg = pitch_stats(pitches)
    st.subheader("🎤 Voice Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Lowest Pitch", f"{low:.2f} Hz" if low else "—")
    col2.metric("Highest Pitch", f"{high:.2f} Hz" if high else "—")
    col3.metric("Average Pitch", f"{avg:.2f} Hz" if avg else "—")

    # Plot pitch contour
    fig, ax = plt.subplots()
    ax.plot(times, pitches, label="Pitch")
    ax.axhline(y=avg, color='r', linestyle='--', label="Average")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Pitch Contour")
    ax.legend()
    st.pyplot(fig)

    # Convert to harmonium notes and filter out silence
    notes, durations = contour_to_notes(times, pitches)
    
    # Filter out None notes (silence) – these are gaps where pitch was zero
    filtered = [(note, dur) for note, dur in zip(notes, durations) if note is not None]
    if not filtered:
        st.warning("No valid notes detected. Try a clearer recording.")
        st.stop()
    notes, durations = zip(*filtered)  # unzip into separate lists

    # Map note names to frequencies (all notes are guaranteed valid now)
    frequencies = [NOTE_MAP[note] for note in notes]

    # Display detected notes sequence
    st.subheader("🎼 Detected Harmonium Notes")
    note_str = " → ".join(notes)
    st.success(note_str)

    # Generate harmonium audio from note sequence
    with st.spinner("Generating harmonium melody..."):
        wave = generate_harmonium_sequence(frequencies, durations)
        output_path = save_audio(wave, sr=22050)

    st.subheader("🎹 Harmonium Output")
    st.audio(output_path, format="audio/wav")

    # Provide download button
    with open(output_path, "rb") as f:
        st.download_button(
            label="Download Harmonium Audio",
            data=f,
            file_name="harmonium_melody.wav",
            mime="audio/wav"
        )

    # Clean up temporary files
    os.unlink(temp_audio_path)
    os.unlink(output_path)