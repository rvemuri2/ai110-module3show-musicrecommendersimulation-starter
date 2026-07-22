import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    instrumentalness: float
    loudness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries.

    Numeric columns are converted so we can do math later:
    - `id` becomes an int
    - the audio-feature columns become floats
    Text columns (title, artist, genre, mood) are left as strings.

    Required by src/main.py
    """
    int_fields = {"id"}
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
        "loudness",
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the points system from
    docs/algorithm_recipe.md.

    Points awarded:
    - genre match         +3
    - mood match          +2
    - energy close        +2   (within 0.15 of target)
    - acousticness close  +2   (within 0.15 of target)
    - valence close       +1   (within 0.15 of target)
    - danceability close  +1   (within 0.15 of target)

    Returns a (score, reasons) tuple, where reasons explains each category that
    earned points, e.g. "genre match (+3)".
    """
    CLOSE = 0.15  # numeric features count as a match within this distance (0-1 scale)

    score = 0.0
    reasons: List[str] = []

    # Categorical features: exact match earns the points.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 3
        reasons.append(f"genre match ({song['genre']}) (+3)")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 2
        reasons.append(f"mood match ({song['mood']}) (+2)")

    # Numeric features: earn the points when the value is close to the target.
    numeric = [
        ("target_energy", "energy", 2, "energy"),
        ("target_acousticness", "acousticness", 2, "acousticness"),
        ("target_valence", "valence", 1, "valence"),
        ("target_danceability", "danceability", 1, "danceability"),
    ]
    for pref_key, song_key, points, label in numeric:
        if abs(user_prefs[pref_key] - song[song_key]) <= CLOSE:
            score += points
            reasons.append(f"{label} close (+{points})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
