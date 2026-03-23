# AI Voice to Harmonium Converter

AI Voice to Harmonium Converter is a Python-based application that converts human voice into harmonium-style musical output. It extracts pitch from audio using Librosa, maps it to Indian musical notes, and generates harmonium sound using waveform synthesis.

## Features
- Audio upload (WAV/MP3)
- Pitch detection (low, high, average)
- Note mapping (Sa, Re, Ga, Ma, Pa, Dha, Ni)
- Harmonium sound generation
- Audio playback and download

## Technologies Used
- Python
- Librosa
- NumPy
- Streamlit

## How to Run
1. Install dependencies:
   pip install streamlit librosa numpy soundfile

2. Run the app:
   streamlit run app.py
