# Algorithm Recipe — Music Recommender Simulation

This document describes the exact rules the recommender uses to decide which
songs to recommend. It is a **content-based** recipe: songs are scored purely on
how well their attributes match a user's stated taste profile, using a fixed
points system (no machine learning, no other-user data).

## Overview

> For every song, award a fixed number of **points** for each preference it
> matches. Important categories are worth more points than minor ones. Add up
> the points into one total score, sort all songs from most points to fewest,
> and return the top _k_. Along the way, collect a short "reason" for every
> category that earned points, so each pick can be explained.

## The Taste Profile

Defined in `src/main.py` as the `user_prefs` dictionary:

```python
user_prefs = {
    "favorite_genre": "lofi",       # categorical exact-match
    "favorite_mood": "focused",     # categorical exact-match
    "target_energy": 0.40,          # numeric, want it close
    "target_valence": 0.55,         # numeric, want it close
    "target_danceability": 0.55,    # numeric, want it close
    "target_acousticness": 0.80,    # numeric, want it close
}
```

## Step 1 — Award points per category

Each category is worth a whole number of points. A song earns the points if it
matches; otherwise it earns 0 for that category.

**Categorical features** — earn the points on an exact match:

```python
if song.genre == user_prefs["favorite_genre"]:  points += 3   # genre match
if song.mood  == user_prefs["favorite_mood"]:   points += 2   # mood match
```

**Numeric features** — earn the points when the song's value is "close" to the
target, meaning within 0.15 (since these attributes are all on a 0–1 scale):

```python
if abs(user_prefs["target_energy"]       - song.energy)       <= 0.15:  points += 2
if abs(user_prefs["target_acousticness"] - song.acousticness) <= 0.15:  points += 2
if abs(user_prefs["target_valence"]      - song.valence)      <= 0.15:  points += 1
if abs(user_prefs["target_danceability"] - song.danceability) <= 0.15:  points += 1
```

> Note: `tempo_bpm` is not used. It runs 60–152, not 0–1, so the 0.15 "close"
> rule would not apply to it without scaling first.

## Step 2 — Points table

| Category              | Points | Why it is worth this much           |
| --------------------- | ------ | ----------------------------------- |
| `favorite_genre`      | 3      | Strongest identity signal           |
| `favorite_mood`       | 2      | Second-strongest categorical signal |
| `target_energy`       | 2      | Core "feel" dimension               |
| `target_acousticness` | 2      | Core "feel" dimension               |
| `target_valence`      | 1      | Refines happy vs. sad               |
| `target_danceability` | 1      | Breaks ties within a mood           |
| **Max possible**      | **11** |                                     |

The total score for a song is simply the sum of the points it earned, from 0 to
11. Points are the tunable knob: if genre feels too dominant, lower it from 3.

## Step 3 — Build the reasons (for explanation)

Whenever a category earns points, append a human-readable reason:

```python
if song.genre == user_prefs["favorite_genre"]:  reasons.append(f"matches your favorite genre ({song.genre})")
if song.mood  == user_prefs["favorite_mood"]:   reasons.append(f"matches your mood ({song.mood})")
if abs(user_prefs["target_energy"] - song.energy) <= 0.15:  reasons.append("energy is close to what you like")
# ...same pattern for acousticness, valence, and danceability
```

`score_song` returns `(points, reasons)`; the explanation is those reasons joined.

## Step 4 — Rank and return

1. Score every song with `score_song` -> `(song, points, reasons)`.
2. Sort descending by `points`.
3. Tie-breaker: lower song `id` wins (stable, predictable).
4. Return the top `k`.

## Sanity Check

With the lo-fi study profile above, **Focus Flow (id 9)** should top the list
with a perfect **11/11**: genre (3) + mood (2) + energy (2) + acousticness (2) +
valence (1) + danceability (1). **Library Rain (id 4)** and **Midnight Coding
(id 2)** follow, each scoring **9** (they match everything except mood, so they
tie and id 4 comes first). This is the expected outcome to confirm the recipe is
wired correctly.

## Scope Note

This recipe drives the **functional / dictionary path** (`score_song`,
`recommend_songs`), which reads all six preference keys. The **OOP path**
(`Recommender.recommend` with a `UserProfile` object) follows the same logic but
currently only has four fields available: `favorite_genre`, `favorite_mood`,
`target_energy`, and `likes_acoustic`.
