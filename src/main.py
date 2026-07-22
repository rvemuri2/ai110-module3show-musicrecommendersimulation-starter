"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Three distinct "normal" taste profiles.
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "target_valence": 0.85,
        "target_danceability": 0.85,
        "target_acousticness": 0.10,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.55,
        "target_danceability": 0.55,
        "target_acousticness": 0.85,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.40,
        "target_danceability": 0.50,
        "target_acousticness": 0.10,
    },
    # --- Adversarial / edge-case profiles ---
    # Conflicting: wants maximum energy AND a sad, quiet, acoustic sound at the
    # same time. In real music these rarely co-occur, so this probes whether the
    # score rewards contradictory targets that no single song can satisfy.
    "Adversarial: Hyper but Sad/Acoustic": {
        "favorite_genre": "rock",
        "favorite_mood": "sad",         # "sad" is not a mood in the dataset
        "target_energy": 0.95,
        "target_valence": 0.05,
        "target_danceability": 0.10,
        "target_acousticness": 0.95,
    },
    # Nonexistent taste: genre and mood that do not exist in the catalog, with
    # every numeric target parked at 0.5. Probes whether the recommender still
    # returns something sensible when nothing can match categorically.
    "Adversarial: Nonexistent Taste": {
        "favorite_genre": "kpop",       # not in the dataset
        "favorite_mood": "angry",       # not in the dataset
        "target_energy": 0.50,
        "target_valence": 0.50,
        "target_danceability": 0.50,
        "target_acousticness": 0.50,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one named profile."""
    line = "=" * 60
    print(f"\n{line}")
    print(f"  {name} — top {k}")
    print(
        f"  genre={user_prefs['favorite_genre']} | "
        f"mood={user_prefs['favorite_mood']} | "
        f"energy={user_prefs['target_energy']}"
    )
    print(line)

    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k), start=1
    ):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     • {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
