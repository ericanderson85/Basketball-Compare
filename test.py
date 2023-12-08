from nbaplayer import NBAPlayer
import os
import pandas as pd


ids = []
for file in os.listdir("cache/"):
    if file[-5:] == ".json":
        player = NBAPlayer(file)
        if player.get_info()["GREATEST_75_FLAG"] == "Y":
            ids.append(player.player_id)

df = pd.read_csv('modified_file.csv')

weights = []
for id in ids:
    player_data = df[df['ID'] == id]
    if not player_data.empty:
        player_name = player_data.iloc[0]['Name']
        player_weight = player_data.iloc[0]['Weight']
        weights.append([player_name, player_weight])

weights.sort(key=lambda x: x[1], reverse=True)
for player_name, player_weight in weights:
    print(f"Player: {player_name}, Weight: {player_weight}")
