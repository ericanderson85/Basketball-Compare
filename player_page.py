from flask import Blueprint, render_template, request
from nbaplayer import NBAPlayer
from random import choice
import os


player = Blueprint(__name__, "player")


@player.route("/player")
def player_profile():
    args = request.args
    player = NBAPlayer(f"{args.get("id")}.json")
    info = player.get_info()
    position = info["POSITION"]
    team = info["TEAM_NAME"]
    height = info["HEIGHT"].split("-")
    country = info["COUNTRY"]
    random_player = choice(os.listdir("cache/")).split(".")[0]
    stats = player.get_stats_per_game()
    seasons = player.seasons()

    return render_template("players.html", player=player, height=height, position=position, team=team, country=country, stats=stats, seasons=seasons, random_player=random_player)
