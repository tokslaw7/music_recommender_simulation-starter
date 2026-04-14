# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
**Tokslaw Reflective Mix 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

This model suggests 5 songs from a small catalog based on a user's preferred genre, mood, and energy level.

Prompts:  

- What kind of recommendations does it generate  
primary matching features based (recommendation is based on personal experience(intensity& momentum = ENERGY) + (Emotions = MOOD)) = Mood + energy (Main)
- What assumptions does it make about the user   
search history/exploration of similar music
- Is this for real users or classroom exploration  
classroom - limited dataset

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.) 
  Genre 
- What user preferences are considered  
  search preferences
- How does the model turn those into a score  
  using metrics calculation(accuracy- correct predictions/total predictions)
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- What features of each song are used (genre, energy, mood, etc.) Genre 

Genre match is used, if it matches score = 1 , else 0 
Mood match is used, if mit matches score = 1 , else 0
Energy similarity is used to determine the distance or linear closeness.  
Total:
score = 0.45 * genre_score + 0.30 * mood_score + 0.25 * energy_similarity

Energy similarity math:

distance = |song_energy - target_energy|
energy_similarity = max(0, 1 - distance / radius), with radius = 1.0

This works because:
1. It rewards songs closest to the user’s target energy, not just higher/lower values.
2. Genre and mood are core recommendations

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  - 20 songs
- What genres or moods are represented  
intensity (energy) & emotions(Mood)
- Did you add or remove data

 Added more song metadata

- Are there parts of musical taste missing in the dataset.      Yes, they are :
  - Time of day, activity, weather, focus level because they often matter most in real life

---

## 5. Strengths  

Where does your system seem to work well  

The system works best for users with clear preferences that map directly to labels in the dataset, such as pop + happy + high energy or lofi + chill + medium energy. It captures intuitive patterns well by consistently ranking songs higher when genre and mood match and then using energy to break ties between close candidates. In my tests, the top results for baseline profiles felt reasonable and stable, especially when users gave specific and realistic preference values.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

One weakness is that the recommender over-prioritizes genre and mood, so users with uncommon or mixed tastes can get repetitive results. Because those two features carry most of the score, songs that are close on other traits like tempo or acousticness may still be ranked too low. This creates a bias toward users whose preferences match the limited labels in the dataset and can reduce recommendation diversity.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested the recommender with five profiles to see both normal and edge-case behavior:

1. Baseline pop-happy profile: genre = pop, mood = happy, energy = 0.8.
2. Conflicting profile: genre = pop, mood = sad, energy = 0.9.
3. Numeric-only profile: genre and mood empty, but exact numeric targets for energy, tempo, valence, danceability, and acousticness.
4. Out-of-range profile: genre = lofi, mood = chill, with energy/tempo/valence/danceability/acousticness set above valid ranges.
5. Contradictory acoustic profile: genre = lofi, mood = chill, acousticness = 0.9, likes_acoustic = False.

I looked for three things in the outputs: ranking stability, whether explanations matched the score drivers, and whether tiny profile changes caused large ranking shifts.

The most surprising result was that invalid numeric values still produced plausible recommendations, because numeric similarity gets clamped while genre and mood keep strong fixed weights. Another surprise was that leaving genre and mood blank still gave coherent top songs from numeric similarity alone. I also observed that acousticness and likes_acoustic can disagree, which can make explanations sound inconsistent with why a song scored well.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Next, I would add more user preferences such as activity context (studying, workout, commute), time of day, and tolerance for explicit lyrics so recommendations can better match real listening situations. I would also improve explanations by showing a short feature-level breakdown for each song (for example, what percent of the score came from genre, mood, and audio attributes) so users can understand and trust why a track was selected.

To improve diversity, I would add a re-ranking step that prevents near-duplicate songs from dominating the top 5 and ensures a healthier mix of artists or related genres. To handle more complex tastes, I would support multi-preference input (like "happy but calm" or "high energy with acoustic instruments") and blend those signals instead of forcing users into a single mood/genre label.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment was realizing that recommendation systems do not need to be overly complex to produce results that feel personal. Building this project showed me how a few weighted features, like genre, mood, and energy, can already create suggestions that seem "right" to a listener. Copilot helped me move faster by clarifying logic, suggesting cleaner code structure, and helping me debug edge cases so I could focus on understanding the system design. What surprised me most was how even a simple scoring algorithm could still feel like a real recommender, which changed how I think about the balance between model complexity and user experience.
