from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

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
    preferred_tempo_bpm: float = 100.0
    target_valence: float = 0.5
    target_danceability: float = 0.5
    preferred_acousticness: float = 0.5

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _energy_similarity(song_energy: float, target_energy: float, radius: float = 1.0) -> float:
        """
        Converts distance in energy space into a similarity score in [0, 1].
        Closer to target energy gets a higher score.
        """
        distance = abs(song_energy - target_energy)
        similarity = 1.0 - (distance / radius)
        return max(0.0, min(1.0, similarity))

    @staticmethod
    def _numeric_similarity(value: float, target: float, radius: float) -> float:
        """Generic closeness score in [0, 1] for numeric features."""
        distance = abs(value - target)
        similarity = 1.0 - (distance / radius)
        return max(0.0, min(1.0, similarity))

    @classmethod
    def _score_song(cls, user: UserProfile, song: Song) -> float:
        """
        Weighted score based on user-preferred genre, mood, and energy target.
        """
        genre_score = 1.0 if song.genre.lower() == user.favorite_genre.lower() else 0.0
        mood_score = 1.0 if song.mood.lower() == user.favorite_mood.lower() else 0.0
        energy_score = cls._energy_similarity(song.energy, user.target_energy)
        tempo_score = cls._numeric_similarity(song.tempo_bpm, user.preferred_tempo_bpm, radius=120.0)
        valence_score = cls._numeric_similarity(song.valence, user.target_valence, radius=1.0)
        danceability_score = cls._numeric_similarity(song.danceability, user.target_danceability, radius=1.0)
        acousticness_score = cls._numeric_similarity(song.acousticness, user.preferred_acousticness, radius=1.0)

        # Weights sum to 1.0.
        return (
            (0.35 * genre_score)
            + (0.25 * mood_score)
            + (0.20 * energy_score)
            + (0.08 * tempo_score)
            + (0.05 * valence_score)
            + (0.04 * danceability_score)
            + (0.03 * acousticness_score)
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = [(song, self._score_song(user, song)) for song in self.songs]
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"matches your favorite genre ({user.favorite_genre})")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"matches your preferred mood ({user.favorite_mood})")

        energy_delta = abs(song.energy - user.target_energy)
        if energy_delta <= 0.10:
            reasons.append("has very close energy to your target")
        elif energy_delta <= 0.25:
            reasons.append("has moderately close energy to your target")

        if abs(song.tempo_bpm - user.preferred_tempo_bpm) <= 12:
            reasons.append("is close to your preferred tempo")
        if abs(song.valence - user.target_valence) <= 0.10:
            reasons.append("matches your target positivity level")
        if abs(song.danceability - user.target_danceability) <= 0.10:
            reasons.append("matches your danceability preference")

        acoustic_delta = abs(song.acousticness - user.preferred_acousticness)
        if acoustic_delta <= 0.12:
            reasons.append("is close to your acousticness preference")
        elif user.likes_acoustic and song.acousticness >= 0.65:
            reasons.append("fits your acoustic leaning")
        elif not user.likes_acoustic and song.acousticness <= 0.35:
            reasons.append("fits your non-acoustic leaning")

        if reasons:
            return "Recommended because it " + ", ".join(reasons) + "."

        return "Recommended because its overall profile is the closest available match to your preferences."


# Functional implementations required by src/main.py to load songs and generate recommendations without needing to instantiate the Recommender class.
def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def _energy_similarity(song_energy: float, target_energy: float, radius: float = 1.0) -> float:
    distance = abs(song_energy - target_energy)
    similarity = 1.0 - (distance / radius)
    return max(0.0, min(1.0, similarity))


def _numeric_similarity(value: float, target: float, radius: float) -> float:
    distance = abs(value - target)
    similarity = 1.0 - (distance / radius)
    return max(0.0, min(1.0, similarity))


# Generate recommendations based on user preferences and song attributes.
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    favorite_genre = str(user_prefs.get("genre", "")).lower()
    favorite_mood = str(user_prefs.get("mood", "")).lower()
    target_energy = float(user_prefs.get("energy", 0.5))
    preferred_tempo_bpm = float(user_prefs.get("tempo_bpm", 100.0))
    target_valence = float(user_prefs.get("valence", 0.5))
    target_danceability = float(user_prefs.get("danceability", 0.5))
    preferred_acousticness = float(user_prefs.get("acousticness", 0.5))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", preferred_acousticness >= 0.5))

    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        genre_score = 1.0 if str(song.get("genre", "")).lower() == favorite_genre else 0.0
        mood_score = 1.0 if str(song.get("mood", "")).lower() == favorite_mood else 0.0
        energy_score = _energy_similarity(float(song.get("energy", 0.0)), target_energy)
        tempo_score = _numeric_similarity(float(song.get("tempo_bpm", 0.0)), preferred_tempo_bpm, radius=120.0)
        valence_score = _numeric_similarity(float(song.get("valence", 0.0)), target_valence, radius=1.0)
        danceability_score = _numeric_similarity(
            float(song.get("danceability", 0.0)), target_danceability, radius=1.0
        )
        acousticness_score = _numeric_similarity(
            float(song.get("acousticness", 0.0)), preferred_acousticness, radius=1.0
        )

        total_score = (
            (0.35 * genre_score)
            + (0.25 * mood_score)
            + (0.20 * energy_score)
            + (0.08 * tempo_score)
            + (0.05 * valence_score)
            + (0.04 * danceability_score)
            + (0.03 * acousticness_score)
        )

        reasons = []
        if genre_score == 1.0:
            reasons.append("genre match")
        if mood_score == 1.0:
            reasons.append("mood match")
        if energy_score >= 0.85:
            reasons.append("very close energy")
        elif energy_score >= 0.70:
            reasons.append("close energy")
        if abs(float(song.get("tempo_bpm", 0.0)) - preferred_tempo_bpm) <= 12:
            reasons.append("tempo match")
        if abs(float(song.get("valence", 0.0)) - target_valence) <= 0.10:
            reasons.append("valence match")
        if abs(float(song.get("danceability", 0.0)) - target_danceability) <= 0.10:
            reasons.append("danceability match")

        song_acousticness = float(song.get("acousticness", 0.0))
        if abs(song_acousticness - preferred_acousticness) <= 0.12:
            reasons.append("acousticness match")
        elif likes_acoustic and song_acousticness >= 0.65:
            reasons.append("fits acoustic preference")
        elif not likes_acoustic and song_acousticness <= 0.35:
            reasons.append("fits non-acoustic preference")

        explanation = (
            f"{', '.join(reasons)}."
            if reasons
            else "best available balance of genre, mood, energy, and audio profile."
        )
        scored.append((song, total_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
