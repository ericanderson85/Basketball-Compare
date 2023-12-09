import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
import time
import os
from nbaplayer import NBAPlayer


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


i = 0
for player in players.get_active_players()[229:]:
    id = player['id']
    # Control the frequency of API calls
    time.sleep(0.5)
    updated_stats = playercareerstats.PlayerCareerStats(id).get_dict()
    updated_info = commonplayerinfo.CommonPlayerInfo(id).get_dict()
    updated_json = [updated_stats, updated_info]
    with open(f"cache/{id}.json", "w") as file:
        json.dump(updated_json, file)
    print(f"{i} : {id}")
    i += 1

all_seasons = []
indices = []
for file in os.listdir("cache/"):
    if file[-5:] != ".json":
        continue
    current_player = NBAPlayer(file)
    simple = current_player.get_stats_simple()
    seasons = len(current_player.seasons())
    curr_season = []
    curr_index = []
    for i in range(seasons):
        curr_season.append(normalize(simple[i][2]))
        curr_index.append(simple[i][0:2])
    all_seasons.extend(curr_season)
    indices.extend(curr_index)

with open('tree_format.json', 'w') as tree:
    tree.write(json.dumps(all_seasons))

with open('index.json', 'w') as index:
    index.write(json.dumps(indices))
