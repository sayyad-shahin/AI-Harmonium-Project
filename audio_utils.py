import numpy as np
import soundfile as sf
import tempfile
import os

def generate_harmonium_note(freq, duration=1.0, sr=22050, attack=0.05, decay=0.1):
    """
    Generate a single harmonium note with a safe envelope.
    """
    total_samples = int(sr * duration)
    if total_samples == 0:
        return np.array([])
    
    t = np.linspace(0, duration, total_samples)
    
    # Basic waveform (harmonic series)
    wave = (
        np.sin(2 * np.pi * freq * t) +
        0.5 * np.sin(2 * np.pi * freq * 2 * t) +
        0.25 * np.sin(2 * np.pi * freq * 3 * t)
    )
    
    # --- Envelope construction ---
    attack_samples = min(int(attack * sr), total_samples)
    decay_samples = min(int(decay * sr), total_samples)
    
    # If attack + decay exceed total length, we reduce the decay (or both) to fit.
    # Here we give priority to attack and clip decay.
    if attack_samples + decay_samples > total_samples:
        decay_samples = total_samples - attack_samples
        if decay_samples < 0:
            decay_samples = 0
    
    sustain_samples = total_samples - attack_samples - decay_samples
    
    envelope = np.ones(total_samples)
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    if decay_samples > 0:
        envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
    # sustain region (if any) is already 1
    
    wave *= envelope
    
    # Normalize
    max_val = np.max(np.abs(wave))
    if max_val > 0:
        wave = wave / max_val
    
    return wave

def generate_harmonium_sequence(notes, durations, sr=22050):
    """
    Generate a waveform from a sequence of notes and durations.
    notes: list of frequencies (float) – None or 0 will be skipped
    durations: list of durations (float)
    """
    audio = np.array([])
    for freq, dur in zip(notes, durations):
        if freq is None or freq <= 0 or dur <= 0:
            continue
        wave = generate_harmonium_note(freq, dur, sr)
        audio = np.concatenate((audio, wave))
    return audio

def save_audio(wave, sr):
    """
    Save audio to a temporary file and return the path.
    """
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "harmonium_output.wav")
    sf.write(temp_path, wave, sr)
    return temp_path