from nbaplayer import NBAPlayer
from nba_api.stats.static import players


player_count = 0
season_count = 0

for player in players.get_players():
    player_count += 1
    for season in NBAPlayer(f"{player['id']}.json").seasons():
        season_count += 1

print("number of players:", player_count)
print("number of seasons:", season_count)
