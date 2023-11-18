from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
import json
import time

# Every NBA player ever
for player in players.get_players():
    id = player["id"]
    file_name = f"cache/{id}.json"
    # Limit the frequency of API calls
    time.sleep(1)
    stats = playercareerstats.PlayerCareerStats(id).get_dict()
    time.sleep(1)
    info = commonplayerinfo.CommonPlayerInfo(id).get_dict()
    combined_json = [stats, info]
    # Create the file
    with open(file_name, "w") as file:
        # Write the json to the file
        json.dump(combined_json, file)
