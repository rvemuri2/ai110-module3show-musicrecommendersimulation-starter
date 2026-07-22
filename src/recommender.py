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
    # Numeric feature counts as a match within this distance (0-1 scale).
    CLOSE = 0.15
    # A song is considered "acoustic" at or above this acousticness value.
    ACOUSTIC_THRESHOLD = 0.5

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score one Song against a UserProfile; returns (score, reasons)."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += 3
            reasons.append(f"genre match ({song.genre}) (+3)")

        if song.mood == user.favorite_mood:
            score += 2
            reasons.append(f"mood match ({song.mood}) (+2)")

        if abs(user.target_energy - song.energy) <= self.CLOSE:
            score += 2
            reasons.append("energy close (+2)")

        # likes_acoustic is a boolean, so reward songs whose acousticness agrees
        # with the preference (acoustic when wanted, non-acoustic when not).
        is_acoustic = song.acousticness >= self.ACOUSTIC_THRESHOLD
        if is_acoustic == user.likes_acoustic:
            score += 2
            fit = "acoustic" if user.likes_acoustic else "non-acoustic"
            reasons.append(f"{fit} as you prefer (+2)")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score, ties broken by lowest id."""
        ranked = sorted(
            self.songs,
            key=lambda song: (-self._score(user, song)[0], song.id),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = self._score(user, song)
        if not reasons:
            return "Recommended as a fallback; it does not strongly match your preferences."
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV into a list of dicts, casting numeric columns."""
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
    """Score a song dict against user prefs (see docs/algorithm_recipe.md); returns (score, reasons)."""
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
    """Rank songs with score_song() and return the top k as (song, score, explanation) tuples."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["id"]))

    return [
        (song, score, "; ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in ranked[:k]
    ]
