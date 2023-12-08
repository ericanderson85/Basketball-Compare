import base64
import io
import csv
from math import pi
import matplotlib.pyplot as plt
from random_player import get_random_player
import os
import json
from nbaplayer import NBAPlayer
from flask import render_template, request, Blueprint, redirect, url_for
import matplotlib
matplotlib.use('Agg')


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
                    other_player, other_season]]

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


def radar(stats, other_stats, categories):
    normalization_factors = {
        "PTS": 50.2, "AST": 14.5, "REB": 27.2, "STL": 4.1, "BLK": 5.6,
        "TOV": 5.7, "FGA": 39.5, "FGM": 20, "FG_PCT": 100,
        "FG3A": 13.2, "FG3M": 5.5, "FG3_PCT": 100
    }
    label_mapping = {
        "PTS": "PTS",
        "AST": "AST",
        "REB": "REB",
        "BLK": "BLK",
        "STL": "STL",
        "TOV": "TOV",
        "FGA": "FGA",
        "FGM": "FGM",
        "FG_PCT": "FG%",
        "FG3A": "3PA",
        "FG3M": "3PM",
        "FG3_PCT": "3P%"
    }

    # Normalize the data
    normalized = [stats[i] / normalization_factors[categories[i]]
                  for i in range(len(categories))]
    other_normalized = [other_stats[i] / normalization_factors[categories[i]]
                        for i in range(len(categories))]

    # Number of variables
    N = len(categories)

    # Dataset 1
    values1 = normalized
    values1 += normalized[:1]

    # Dataset 2
    values2 = other_normalized
    values2 += other_normalized[:1]

    # Compute angle for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Complete the loop

    # Rotate the plot so that the first axis is at the top
    # Offset by pi/2 (90 degrees) to put the first axis at the top
    theta_offset = pi / -2
    angles = [(angle - theta_offset) % (2 * pi) for angle in angles]

    # Create a new figure for the spider plot
    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.yaxis.grid(False)

    ax.spines['polar'].set_visible(False)

    # Set the angle gridlines and labels
    ax.set_thetagrids([a * 180/pi for a in angles[:-1]],
                      categories, color="#B30000", fontsize=20)

    for label, angle in zip(ax.get_xticklabels(), angles):
        # Ensure there is no background fill interfering
        label.set_backgroundcolor('none')
        label.set_zorder(3)  # Place the labels on top of other elements

    # Draw one axe per variable and add labels
    categories = [label_mapping.get(label, label) for label in categories]
    plt.xticks(angles[:-1], categories)

    # Plot data and fill area for the first dataset
    ax.plot(angles, values1, label='Dataset 1', color="#006F00")
    ax.fill(angles, values1, '#006F00', alpha=.3)

    # Plot data and fill area for the second dataset
    ax.plot(angles, values2, label='Dataset 2', color="#004480")
    ax.fill(angles, values2, '#004480', alpha=.3)

    ax.set_yticklabels([])
    ax.yaxis.set_tick_params(labelsize=0)

    ax.figure.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Save it to a temporary buffer.
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    plt.close(fig)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return (data)


@comparison.route("/comparison")
def player_comparison():
    player = NBAPlayer(f"{request.args.get('id')}.json")
    players = []
    with open('players.csv', "r", newline='', errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            players.append(row)
    season = request.args.get('season')
    selected_headers = json.loads(request.args.get('s'))
    other_player = priority(
        player=player, season=season, attributes=selected_headers)
    other_season = other_player[1]
    other_player = other_player[0]
    stats = [player.get_stats_per_game()[season][key]
             for key in selected_headers if key in player.get_stats_per_game()[season]]
    try:
        other_stats = [other_player.get_stats_per_game()[other_season][key]
                       for key in selected_headers if key in other_player.get_stats_per_game()[other_season]]
    except:
        return redirect(url_for("home"))

    random_player = get_random_player()
    radar_chart = radar(stats=stats, other_stats=other_stats,
                        categories=selected_headers)

    return render_template("comparison.html", player=player, season=season, selected_headers=selected_headers, other_player=other_player, stats=stats, other_stats=other_stats, other_season=other_season, attr=selected_headers, random_player=random_player, radar_chart=radar_chart, players=players)
