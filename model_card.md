# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

TuneMatch 1.0 — a simple, explainable recommender that matches songs to a listener's stated taste.

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

TuneMatch suggests songs from a small catalog that fit one listener's stated taste (favorite genre, favorite mood, and a few audio preferences like energy and acousticness). It assumes the user can describe their taste as simple labels and numbers, and that a good match is a song whose features are close to those preferences. It is built for classroom exploration, not for real users. It should
not be used to make real product decisions, to judge anyone's taste, or on large real-world catalogs, and it does not learn from listening history.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Each song has a genre, a mood, and audio numbers like energy and acousticness, and the user gives a favorite genre, favorite mood, and target values for a few of those numbers. The model gives a song points for each preference it matches: the most points for a genre match, fewer for mood, and some for being close to the target numbers. It adds those points into one score, ranks songs from highest to lowest, and shows the top few along with the reasons they scored. Compared to the starter, I filled in the empty scoring, added more songs and features, and used a clear points system so every recommendation can be explained.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

The catalog has 18 songs, each with a title, artist, genre, mood, and seven audio numbers (energy, tempo, valence, danceability, acousticness, instrumentalness, and loudness). It covers 15 genres (such as pop, lofi, rock, jazz, hip hop, and metal) and 14 moods (such as happy, chill, intense, and melancholic). I added 8 songs and two new features (instrumentalness and loudness) to the starter set.
The dataset is tiny and English-leaning, with no lyrics and only a few songs per genre, so many real tastes are missing.

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

The system works well for listeners with a clear, common taste, like High-Energy Pop or Chill Lofi, where it puts the obvious best song first. It correctly captures the "feel" of music through energy and acousticness, so calm songs and loud songs separate cleanly. Its picks matched my intuition: pop-happy users get upbeat pop and lofi users get quiet acoustic tracks. Because every pick comes with reasons, it is easy to see why a song was chosen, and it is fast and simple to follow.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

The main weakness I found is that the "energy gap" is a hard cliff: a song within 0.15 of the user's target energy earns full points, but a song 0.16 away earns nothing and scores the same as a song at the opposite end of the scale. Because the catalog's energy values are clustered around 0.25 to 0.50 and 0.75 to 0.97 with a gap in between, this favors users whose target lands in those dense zones, so a user targeting 0.30 or 0.90 matches 7 of 18 songs while a user targeting 0.65 matches only 3 and a user wanting very low energy matches just 1. The model also does not consider tempo, valence, or instrumentalness in the main path, and it uses exact matching for genre and mood, so underrepresented or slightly misspelled genres (like "indie pop" instead of "pop") get no credit at all. This makes the system overfit to whichever genre a user names and quietly under-serve listeners with in-between or extreme tastes. A smoother distance-based score that rewards closeness gradually would reduce this bias.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

### Profiles tested

I tested five profiles: three everyday ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and two adversarial ones (a contradictory "high energy but sad and acoustic" profile, and a "nonexistent taste" profile using a fake genre and mood with every number at 0.5). For each, I checked whether the top song matched the genre and mood and whether mismatches sank.

### What surprised me

A partly-matching song can still rank near the top. For a "Happy Pop" listener, "Gym Hero" keeps landing second even though its mood is "intense," not "happy": it is still pop, high-energy, danceable, and non-acoustic, so it scores on almost everything and misses only the mood box, which is not enough to push it down. I was also surprised the contradictory profile still picked a confident number one
(just with a low score), and the nonexistent-taste profile produced a big tie decided silently by the lowest-id rule.

### Comparing the profiles (pairwise)

- High-Energy Pop vs Chill Lofi: opposite ends of energy and acousticness, so they share no top songs.
- High-Energy Pop vs Deep Intense Rock: both want high energy and overlap on loud tracks, but genre and mood split them (happy pop vs intense rock).
- Chill Lofi vs Deep Intense Rock: near-opposites (calm acoustic vs loud aggressive), with nothing shared at the top.
- High-Energy Pop vs Adversarial Hyper/Sad/Acoustic: Pop scores high; the contradictory profile can't, since no song is both hyper and sad-acoustic.
- Chill Lofi vs Adversarial Hyper/Sad/Acoustic: the "acoustic" wish overlaps lofi, but the high-energy demand clashes, so lofi tracks score low.
- Deep Intense Rock vs Adversarial Hyper/Sad/Acoustic: both name rock so Storm Runner tops both, but the adversarial version scores it far lower.
- High-Energy Pop vs Adversarial Nonexistent: Pop has a clear winner; the fake profile is a pile of tied low scores with no genre/mood anchor.
- Chill Lofi vs Adversarial Nonexistent: Lofi gives obvious winners; the fake profile ties on mid-range numbers only.
- Deep Intense Rock vs Adversarial Nonexistent: Rock gives one strong pick; the fake profile spreads weak ties across unrelated genres.
- Adversarial Hyper/Sad/Acoustic vs Adversarial Nonexistent: both low, but the hyper one has a genre anchor (one song stands out) while the fake one has none (everything ties).

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

First, I would replace the hard 0.15 cutoff with a smooth score that rewards closeness gradually, so near-misses count instead of being ignored. Second, I would let genres count as partly similar (for example, "indie pop" close to "pop") instead of exact matching only. Third, I would add a diversity rule so the top picks are not all the same artist or sound, and use the unused features like
tempo and instrumentalness to handle more complex tastes. I would also turn the point lists into short friendly sentences to explain recommendations better.

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

My biggest learning moment was realizing a recommender is really just a scoring rule plus a sort, and that the weights I chose quietly shaped every result. AI tools helped me move quickly on the routine parts, like writing the CSV loader, structuring the scoring function, and drafting documentation, but I had to double-check them on the math and the data, for example confirming the scores matched my algorithm recipe, that the tie-breaker ordered songs as expected, and
that claims like the genre counts were actually true and not just assumed. What surprised me most was how a simple points system can still feel like a real recommendation, because attaching clear reasons to each pick makes it seem thoughtful even though it is only addition, and it also fooled easily, like Gym Hero ranking high by matching everything except mood. If I extended this, I would
add smoother scoring, genre similarity, and a diversity rule, and test it on a bigger, more varied catalog. Overall it changed how I see music apps: recommendations are choices made by whoever sets the rules, not neutral facts.
