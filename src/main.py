"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: a "lo-fi study listener"
    user_prefs = {
        "favorite_genre": "lofi",       # categorical exact-match
        "favorite_mood": "focused",     # categorical exact-match
        "target_energy": 0.40,          # numeric: 1 - |target - value|
        "target_valence": 0.55,         # separates happy-calm from sad-calm
        "target_danceability": 0.55,    # separates groovy from static
        "target_acousticness": 0.80,    # full 0-1 signal (not a boolean)
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
