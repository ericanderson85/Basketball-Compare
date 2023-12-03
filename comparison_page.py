from flask import render_template, request, Blueprint, redirect
from nbaplayer import NBAPlayer
import json
import os


comparison = Blueprint(__name__, "comparison")


def priority(player, season, attributes):
    if not isinstance(attributes, list):
        attributes = [attributes]

    player_stats = get_stats_for_player_season(player, season, attributes)
    if not player_stats or None in player_stats:
        return "Attributes unavailable for the selected player and season"

    most_similar_season = []
    for other_player in all_players():
        if other_player.player_id == player.player_id:
            continue

        for other_season in other_player.seasons():
            other_stats = get_stats_for_player_season(
                other_player, other_season, attributes)
            if not other_stats or None in other_stats:
                continue

            similarity = distance(player_stats, other_stats)
            if not most_similar_season or similarity < most_similar_season[0]:
                most_similar_season = [similarity, [
                    other_player.player_name, other_season]]

    return most_similar_season[1] if most_similar_season else "No similar seasons found"


def distance(a: list, b: list):
    return sum(abs((p - q) / ((p + q) / 2)) for p, q in zip(a, b) if p is not None and q is not None and p + q != 0)


def get_stats_for_player_season(player, season, attributes):
    try:
        return [get_stat(player, attr, season) for attr in attributes]
    except TypeError:
        return None


def get_stat(player: NBAPlayer, attr: str, season: str):
    return per_game(player=player, attribute=attr)[season]


def per_game(player: NBAPlayer, attribute: str):
    per_game_stats = player.get_stats_per_game()
    return {season: stats[attribute] for season, stats in per_game_stats.items()}


def all_players():
    return [NBAPlayer(file) for file in os.listdir("cache/") if ".json" in file]


@comparison.route("/comparison")
def player_comparison():
    player = NBAPlayer(f"{request.args.get('id')}.json")
    season = request.args.get('season')
    selected_headers = json.loads(request.args.get('s'))
    other = priority(
        player=player, season=season, attributes=selected_headers)
    other_player = other[0]
    other_season = other[1]
    return other_player + other_season
