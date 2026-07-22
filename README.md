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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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
