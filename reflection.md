# Reflection on Profile Pair Comparisons

Profiles compared:
- P1 baseline pop-happy: genre=pop, mood=happy, energy=0.8
- P2 conflict pop-sad: genre=pop, mood=sad, energy=0.9
- P3 numeric-only: genre and mood empty, numeric targets set
- P4 out-of-range-high: genre=lofi, mood=chill, numeric values set above valid range
- P5 acoustic-conflict: genre=lofi, mood=chill, acousticness=0.9, likes_acoustic=False

Top-3 snapshots used in comparisons:
- P1: Sunrise City, Gym Hero, Rooftop Lights
- P2: Sunrise City, Gym Hero, Cityline Sermon
- P3: Sunrise City, Golden Sidewalk, Cityline Sermon
- P4: Midnight Coding, Library Rain, Focus Flow
- P5: Midnight Coding, Library Rain, Focus Flow

## Pairwise Comments

1. P1 vs P2
Changing mood from happy to sad removed the mood-match boost, so Rooftop Lights dropped out and Cityline Sermon entered from energy/tempo closeness. This makes sense because mood has a large fixed weight and sad has no direct match in the catalog.

2. P1 vs P3
When genre and mood were blank, Sunrise City still stayed at the top but the score dropped because categorical boosts disappeared. This makes sense because numeric similarity can still rank songs well, but category matches are no longer available.

3. P1 vs P4
The output switched from pop/happy songs to lofi/chill songs when profile labels changed to lofi/chill, even with extreme invalid numeric values. This makes sense because out-of-range numerics get clamped and genre+mood dominate the ranking.

4. P1 vs P5
P1 favored pop-driven tracks while P5 favored lofi/chill tracks with very high scores. This makes sense because P5 strongly matches both lofi genre and chill mood plus close energy around 0.4.

5. P2 vs P3
P2 kept pop songs near the top, but P3 surfaced mixed-genre songs like Golden Sidewalk because all songs were evaluated mostly on numeric closeness. This makes sense because P3 removes category filters and broadens the candidate set.

6. P2 vs P4
P2 prioritized pop plus high energy, while P4 prioritized lofi/chill despite unrealistic numeric targets. This makes sense because P4 keeps full category weight and loses much of the numeric signal due to clamping.

7. P2 vs P5
P2 and P5 produced very different top songs because they target different category pairs, even though both are edge cases. This makes sense because category alignment contributes most of the final score in this model.

8. P3 vs P4
P3 selected tracks closest in numeric profile across genres, while P4 selected lofi/chill tracks almost regardless of numeric details. This makes sense because P3 is numeric-driven and P4 is category-driven after numeric saturation.

9. P3 vs P5
P3 included diverse genres in top-3, but P5 concentrated on lofi/chill only. This makes sense because P5 reintroduces strong category constraints and a centered energy target.

10. P4 vs P5
Both pairs returned the same top-3 songs, but P5 scores were much higher because its numeric targets are valid and close to those songs. This makes sense because P4 loses numeric contribution from out-of-range values, while P5 keeps both category and numeric boosts.
