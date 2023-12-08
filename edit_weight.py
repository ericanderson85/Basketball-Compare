import pandas as pd
import os
from nbaplayer import NBAPlayer
import math

df = pd.read_csv('players.csv')


def safe_multiply(stat, multiplier):
    return stat * multiplier if stat is not None else 0


def new_weight_calculation(id):
    new_weight = 0
    player = NBAPlayer(f"{id}.json")
    seasons = player.seasons() or []
    info = player.get_info()

    if any(os.path.isfile(f"static/images/{id}.{ext}") for ext in ['png', 'jpg']):
        new_weight += 15

    if info["GREATEST_75_FLAG"] == "Y":
        new_weight += 10

    new_weight += len(seasons)
    draft_year = info["DRAFT_YEAR"]
    if draft_year is not None and draft_year != "Undrafted":
        draft_year = int(draft_year)
        if int(draft_year / 1000) == 1:
            new_weight += int(draft_year % 100) / 13
        else:
            new_weight += 7.6 + (draft_year % 100) / 12
    total_minutes = 0
    total_stats = 0

    for season in seasons:
        season_stats = player.get_stats_per_game()[season]

        minutes = safe_multiply(season_stats.get("MIN"), .5)
        points = safe_multiply(season_stats.get("PTS"), 1.8)
        rebounds = safe_multiply(season_stats.get("REB"), .6)
        assists = safe_multiply(season_stats.get("AST"), 1)
        steals = safe_multiply(season_stats.get("STL"), 1.6)
        blocks = safe_multiply(season_stats.get("BLK"), 1.6)

        total_minutes += minutes
        total_stats += points + rebounds + assists + steals + blocks

    if len(seasons) > 0:
        new_weight += total_stats / 4 / len(seasons)

    return new_weight


def normalize_weight(weight, min_weight, max_weight):
    normalized_linear = (weight - min_weight) / (max_weight - min_weight)
    exponent = 3
    normalized_exponential = math.pow(normalized_linear, exponent)
    return (normalized_exponential * 10)


df['Weight'] = df['ID'].apply(new_weight_calculation)
min_weight = df['Weight'].min()
max_weight = df['Weight'].max()
df['Weight'] = df['Weight'].apply(
    lambda x: normalize_weight(x, min_weight, max_weight))
df = df.sort_values(by='Weight', ascending=False)
df['Weight'] = df['Weight'].apply(lambda x: f"{x:.2f}")
df.to_csv('modified_file.csv', index=False)
