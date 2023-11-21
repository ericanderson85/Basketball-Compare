import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
import time

for player in players.get_active_players():
    id = player['id']
    # Control the frequency of API calls
    time.sleep(1)
    updated_stats = playercareerstats.PlayerCareerStats(id).get_dict()
    time.sleep(1)
    updated_info = commonplayerinfo.CommonPlayerInfo(id).get_dict()
    updated_json = [updated_stats, updated_info]
    with open(f"cache/{id}.json", "w") as file:
        json.dump(updated_json, file)
