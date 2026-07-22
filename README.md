# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Real world recommenders like Spotify and YouTube look at many things at once. They study your listening history, such as what you play, skip, and save. They compare you to millions of other users to find people with similar taste. They also look at the sound of the songs and the context, like the time of day. All of this feeds huge machine learning models that keep learning from your feedback and update over time. My version is much simpler. It only looks at the song's attributes and compares them to one user's stated preferences using a fixed math rule that I write myself. It does not learn from other users or train a model. My version prioritizes being simple and easy to explain, so I can always say exactly why a song was recommended.

Song uses: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness

UserProfile uses: favorite_genre, favorite_mood, target_energy, likes_acoustic

---

## How The System Works

Explain your design in plain language.

My recommender is content-based: it looks only at the qualities of each song and how well they match what one listener says they like. It does not learn from other users or train a model. It just follows a simple, fixed points system that I can fully explain. For every song it awards points for each preference the song matches, adds those points into a total score, and then ranks the songs from the
highest score to the lowest. The higher the score, the better the match.

A note on potential biases: because genre is worth the most points, this system might over-prioritize genre and overlook great songs that match the user's mood but sit in a different genre. Exact matching also means a similar genre earns zero points, which can trap the listener in one style.

The algorithm recipe is included in the docs/algorithm_recipe.md

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

  Each song carries text/category fields (`id`, `title`, `artist`, `genre`, `mood`) and numeric fields on a 0–1 scale (`energy`, `valence`, `danceability`, `acousticness`, `instrumentalness`, `loudness`) plus `tempo_bpm`. The scoring actually uses six of these: `genre`, `mood`, `energy`, `valence`, `danceability`, and `acousticness`.

- What information does your `UserProfile` store
  - It stores the listener's taste as target values: a `favorite_genre`, a `favorite_mood`, a `target_energy`, and whether they like acoustic music (`likes_acoustic`). The dictionary version extends this with `target_valence`, `target_danceability`, and `target_acousticness` so the preferences line up with the song's numeric features.

- How does your `Recommender` compute a score for each song
  - It judges one song at a time and adds up points for each preference the song matches: +3 if the genre matches, +2 if the mood matches, +2 if energy is close to the target (within 0.15), +2 if acousticness is close, +1 if valence is close, and +1 if danceability is close. The points add up to a total from 0 to 11. Genre is worth the most because it is the strongest signal of taste; valence and danceability are worth the least and mainly break ties. As it scores, it also collects a short reason for every category that earned points, so each recommendation can be explained.

- How do you choose which songs to recommend
  - I score every song, then sort them from most points to fewest. If two songs tie, the one with the lower `id` comes first, so the results stay predictable. Finally I take the top _k_ songs and return them with their score and explanation.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python -m src.main` scores every song against several taste profiles
and prints the top 5 for each. Below is the first profile, **High-Energy Pop**
(the remaining profiles, including two adversarial edge cases, are in
[Experiments You Tried](#experiments-you-tried)):

```
Loaded songs: 18

============================================================
  High-Energy Pop — top 5
  genre=pop | mood=happy | energy=0.9
============================================================

1. Sunrise City — Neon Echo
   Score: 11.00
     • genre match (pop) (+3)
     • mood match (happy) (+2)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

2. Gym Hero — Max Pulse
   Score: 9.00
     • genre match (pop) (+3)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

3. Rooftop Lights — Indigo Parade
   Score: 6.00
     • mood match (happy) (+2)
     • energy close (+2)
     • valence close (+1)
     • danceability close (+1)

4. Voltage Peak — Pulsewave
   Score: 6.00
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

5. Concrete Kings — Blocktape
   Score: 5.00
     • energy close (+2)
     • acousticness close (+2)
     • danceability close (+1)
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I ran the recommender against five taste profiles: three "normal" ones and two
adversarial edge cases designed to try to trick the scoring. The output for each
is below.

### Chill Lofi

A clean match — the two lofi/chill songs tie at a perfect 11.

```
============================================================
  Chill Lofi — top 5
  genre=lofi | mood=chill | energy=0.35
============================================================

1. Midnight Coding — LoRoom
   Score: 11.00
     • genre match (lofi) (+3)
     • mood match (chill) (+2)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

2. Library Rain — Paper Lanterns
   Score: 11.00
     • genre match (lofi) (+3)
     • mood match (chill) (+2)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

3. Focus Flow — LoRoom
   Score: 9.00
     • genre match (lofi) (+3)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

4. Spacewalk Thoughts — Orbit Bloom
   Score: 8.00
     • mood match (chill) (+2)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)

5. Paper Boats — Fenwood
   Score: 6.00
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)
     • danceability close (+1)
```

### Deep Intense Rock

Storm Runner wins at 10 (it misses only danceability, whose target 0.50 is 0.16
away from its 0.66 — just past the 0.15 threshold).

```
============================================================
  Deep Intense Rock — top 5
  genre=rock | mood=intense | energy=0.9
============================================================

1. Storm Runner — Voltline
   Score: 10.00
     • genre match (rock) (+3)
     • mood match (intense) (+2)
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)

2. Gym Hero — Max Pulse
   Score: 6.00
     • mood match (intense) (+2)
     • energy close (+2)
     • acousticness close (+2)

3. Concrete Kings — Blocktape
   Score: 5.00
     • energy close (+2)
     • acousticness close (+2)
     • valence close (+1)

4. Iron Verdict — Ashfall
   Score: 5.00
     • energy close (+2)
     • acousticness close (+2)
     • danceability close (+1)

5. Sunrise City — Neon Echo
   Score: 4.00
     • energy close (+2)
     • acousticness close (+2)
```

### Adversarial: Hyper but Sad/Acoustic (conflicting targets)

This profile asks for maximum energy AND a quiet, sad, acoustic, undanceable
sound — a combination no real song has. The scores collapse (the winner only
reaches 5), which is correct. But the #1 pick, Storm Runner, is the *opposite* of
the acoustic/sad request: it wins purely on genre (+3) and energy (+2). A
points-sum can still confidently rank a song first when it nails the high-weight
fields and flunks the rest. Note also that `mood="sad"` does not exist in the
dataset and silently scores 0 with no warning.

```
============================================================
  Adversarial: Hyper but Sad/Acoustic — top 5
  genre=rock | mood=sad | energy=0.95
============================================================

1. Storm Runner — Voltline
   Score: 5.00
     • genre match (rock) (+3)
     • energy close (+2)

2. Winter Elegy — Anna Vorne
   Score: 3.00
     • acousticness close (+2)
     • danceability close (+1)

3. Sunrise City — Neon Echo
   Score: 2.00
     • energy close (+2)

4. Library Rain — Paper Lanterns
   Score: 2.00
     • acousticness close (+2)

5. Gym Hero — Max Pulse
   Score: 2.00
     • energy close (+2)
```

### Adversarial: Nonexistent Taste (kpop / angry, all numerics at 0.5)

Genre and mood can never match, and every numeric target sits at 0.5. The result
is a pile of near-tied low scores (four songs tie at 4), so the lowest-`id`
tie-breaker effectively becomes the ranker. The system never reports "no good
match" — it always returns 5 songs with false confidence.

```
============================================================
  Adversarial: Nonexistent Taste — top 5
  genre=kpop | mood=angry | energy=0.5
============================================================

1. Midnight Coding — LoRoom
   Score: 4.00
     • energy close (+2)
     • valence close (+1)
     • danceability close (+1)

2. Focus Flow — LoRoom
   Score: 4.00
     • energy close (+2)
     • valence close (+1)
     • danceability close (+1)

3. Island Time — Sun Rebels
   Score: 4.00
     • energy close (+2)
     • acousticness close (+2)

4. Dusty Roads Home — Clay Hartman
   Score: 4.00
     • energy close (+2)
     • valence close (+1)
     • danceability close (+1)

5. Coffee Shop Stories — Slow Stereo
   Score: 3.00
     • energy close (+2)
     • danceability close (+1)
```

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
