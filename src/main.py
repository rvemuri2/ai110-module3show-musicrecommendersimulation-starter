"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: an upbeat "pop / happy" listener
    user_prefs = {
        "favorite_genre": "pop",        # categorical exact-match
        "favorite_mood": "happy",       # categorical exact-match
        "target_energy": 0.80,          # wants high energy
        "target_valence": 0.80,         # wants upbeat, positive songs
        "target_danceability": 0.80,    # wants danceable songs
        "target_acousticness": 0.15,    # prefers produced, not acoustic
    }

    k = 5
    recommendations = recommend_songs(user_prefs, songs, k=k)

    line = "=" * 60
    print(f"\n{line}")
    print(f"  Top {k} recommendations for your taste profile")
    print(
        f"  genre={user_prefs['favorite_genre']} | "
        f"mood={user_prefs['favorite_mood']} | "
        f"energy={user_prefs['target_energy']}"
    )
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        reasons = explanation.split("; ")
        for reason in reasons:
            print(f"     • {reason}")

    print(f"\n{line}")


if __name__ == "__main__":
    main()
