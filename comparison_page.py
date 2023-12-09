import base64
from scipy.spatial import KDTree
import numpy as np
import json
import io
from math import pi
import matplotlib.pyplot as plt
from random_player import get_random_player
import json
from nbaplayer import NBAPlayer
from flask import render_template, request, Blueprint, redirect, url_for
import matplotlib
matplotlib.use('Agg')


comparison = Blueprint(__name__, "comparison")


def normalize(data):
    return [
        round(100 * data[0] / 50.4, 1) if data[0] is not None else 0.0,
        round(100 * data[1] / 14.5, 1) if data[1] is not None else 0.0,
        round(100 * data[2] / 27.2, 1) if data[2] is not None else 0.0,
        round(100 * data[3] / 5.6, 1) if data[3] is not None else 0.0,
        round(100 * data[4] / 4.1, 1) if data[4] is not None else 0.0,
        round(100 * data[5] / 5.7, 1) if data[5] is not None else 0.0,
        round(100 * data[6] / 39.5, 1) if data[6] is not None else 0.0,
        round(100 * data[7] / 20, 1) if data[7] is not None else 0.0,
        data[8] if data[8] is not None else 0.0,
        round(100 * data[9] / 13.2, 1) if data[10] is not None else 0.0,
        round(100 * data[10] / 5.3, 1) if data[10] is not None else 0.0,
        data[11] if data[11] is not None else 0.0]


def headers(input_strings):
    conversion_dict = {
        "PTS": 0,
        "AST": 1,
        "REB": 2,
        "BLK": 3,
        "STL": 4,
        "TOV": 5,
        "FGA": 6,
        "FGM": 7,
        "FG_PCT": 8,
        "FG3A": 9,
        "FG3M": 10,
        "FG3_PCT": 11
    }
    return [conversion_dict.get(item, None) for item in input_strings]


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


def nearest_player(player, season, selected_headers):
    with open('index.json', 'r') as file:
        indices = json.load(file)
    indices_list = headers(selected_headers)
    with open('tree_format.json', 'r') as file:
        unfiltered_data = json.load(file)
        data = []
        for i in range(len(unfiltered_data)):
            if indices[i][0] != player.player_id:
                filtered_sublist = [unfiltered_data[i][j]
                                    for j in indices_list]
                data.append(filtered_sublist)
            else:
                data.append([0.0 for _ in range(len(indices_list))])
    kdtree = KDTree(np.array(data))
    player_stats = normalize(
        NBAPlayer(f"{player.player_id}.json").get_stats_simple()[season][2])
    compare_stats = np.array([player_stats[i] for i in indices_list])
    index = kdtree.query(compare_stats)[1]
    return indices[index]


@comparison.route("/comparison")
def player_comparison():
    selected_headers = json.loads(request.args.get('s'))
    player = NBAPlayer(f"{request.args.get('id')}.json")
    season = request.args.get('season')
    season_index = player.seasons().index(season)

    try:
        other_id, other_season = nearest_player(
            player, season_index, selected_headers)
    except:
        return redirect(url_for("home"))

    other_player = NBAPlayer(f"{other_id}.json")

    stats = [player.get_stats_per_game()[season][key]
             for key in selected_headers]
    other_stats = [other_player.get_stats_per_game()[other_season][key]
                   for key in selected_headers]

    random_player = get_random_player()

    radar_chart = radar(stats=stats, other_stats=other_stats,
                        categories=selected_headers)

    return render_template("comparison.html", player=player, season=season, selected_headers=selected_headers, other_player=other_player, stats=stats, other_stats=other_stats, other_season=other_season, attr=selected_headers, random_player=random_player, radar_chart=radar_chart)
