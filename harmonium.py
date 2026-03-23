# harmonium.py

NOTE_MAP = {
    "Sa": 240,
    "Re": 270,
    "Ga": 288,
    "Ma": 320,
    "Pa": 360,
    "Dha": 405,
    "Ni": 432,
    "Sa_high": 480
}

def get_closest_note(freq):
    """
    Return the note name closest to the given frequency.
    """
    if freq is None or freq <= 0:
        return None
    closest_note = None
    min_diff = float("inf")
    for note, f in NOTE_MAP.items():
        diff = abs(freq - f)
        if diff < min_diff:
            min_diff = diff
            closest_note = note
    return closest_note

def contour_to_notes(times, pitches, silence_threshold=0.1, min_duration=0.05):
    """
    Convert a pitch contour into a sequence of (note_name, start_time, end_time).
    Silences are removed; segments shorter than min_duration are merged.
    Returns:
        notes: list of note names (str)
        durations: list of durations (float)
    """
    # Map each frame to a note
    note_names = []
    for p in pitches:
        if p > 0:
            note = get_closest_note(p)
            note_names.append(note)
        else:
            note_names.append(None)
    
    # Group into segments
    segments = []
    current_note = None
    start_time = 0
    for i, note in enumerate(note_names):
        if note != current_note:
            if current_note is not None:
                end_time = times[i]
                duration = end_time - start_time
                if duration >= min_duration:
                    segments.append((current_note, duration))
            current_note = note
            start_time = times[i]
    if current_note is not None:
        duration = times[-1] - start_time
        if duration >= min_duration:
            segments.append((current_note, duration))
    
    # Separate note names and durations
    notes = [seg[0] for seg in segments]
    durations = [seg[1] for seg in segments]
    return notes, durations