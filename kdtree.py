from scipy.spatial import KDTree
import numpy as np
from nbaplayer import NBAPlayer
import json


def normalize(data):
    return [
        round(100 * data[0] / 50.2, 1),
        round(100 * data[1] / 14.5, 1),
        round(100 * data[2] / 27.2, 1),
        round(100 * data[3] / 5.6, 1),
        round(100 * data[4] / 4.1, 1),
        round(100 * data[5] / 5.7, 1),
        round(100 * data[6] / 39.5, 1),
        round(100 * data[7] / 20, 1),
        data[8] if data[8] != 100 else 0,
        round(100 * data[9] / 13.2, 1),
        round(100 * data[10] / 5.5, 1),
        data[11] if data[11] != 100 else 0]


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


with open('index.json', 'r') as file:
    indices = json.load(file)
indices_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
player_id = 201939
player_season = 7
player_stats = normalize(NBAPlayer(f"{player_id}.json").get_stats_simple()[
    player_season][2])
compare_stats = np.array([player_stats[i] for i in indices_list])


with open('tree_format.json', 'r') as file:
    unfiltered_data = json.load(file)
    data = []
    for i in range(len(unfiltered_data)):
        if indices[i][0] != player_id:
            filtered_sublist = [unfiltered_data[i][j] for j in indices_list]
            data.append(filtered_sublist)
kdtree = KDTree(np.array(data))

index = kdtree.query(compare_stats)[1]
id, season = indices[index]
player = NBAPlayer(f"{id}.json")
print([player.get_stats_per_game()[season]])
