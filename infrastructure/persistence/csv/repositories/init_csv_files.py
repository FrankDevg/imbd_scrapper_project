import os
import csv

OUTPUT_DIR = "data"
MOVIES_CSV = os.path.join(OUTPUT_DIR, "movies.csv")
ACTORS_CSV = os.path.join(OUTPUT_DIR, "actors.csv")
MOVIE_ACTOR_CSV = os.path.join(OUTPUT_DIR, "movie_actor.csv")

def init_csv_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(MOVIES_CSV, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["id", "title", "year", "rating", "duration_minutes", "metascore","actors"])

    with open(ACTORS_CSV, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["id", "name"])

    with open(MOVIE_ACTOR_CSV, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["movie_id", "actor_id"])
