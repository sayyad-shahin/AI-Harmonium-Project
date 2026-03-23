import librosa
import numpy as np

def extract_pitch_contour(audio_path, sr=22050, hop_length=512):
    """
    Extract pitch contour using pYIN algorithm.
    Returns:
        times: array of time stamps (in seconds)
        pitches: array of pitch frequencies (Hz), with 0 for unvoiced/silence
    """
    y, sr = librosa.load(audio_path, sr=sr)
    # Use pYIN for more reliable pitch tracking
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop_length)
    # Get the pitch at each time frame (max magnitude)
    pitch_vals = []
    times = librosa.times_like(pitches, sr=sr, hop_length=hop_length)
    for i in range(pitches.shape[1]):
        idx = magnitudes[:, i].argmax()
        pitch = pitches[idx, i]
        # Only keep if magnitude is above threshold (optional)
        pitch_vals.append(pitch if pitch > 0 else 0)
    return times, np.array(pitch_vals)

def pitch_stats(pitch_vals):
    """
    Compute lowest, highest, average pitch from non-zero pitches.
    """
    nonzero = pitch_vals[pitch_vals > 0]
    if len(nonzero) == 0:
        return 0, 0, 0
    return np.min(nonzero), np.max(nonzero), np.mean(nonzero)