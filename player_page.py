from flask import Blueprint, render_template, request
from nbaplayer import NBAPlayer
from random import choice
import os


player = Blueprint(__name__, "player")


@player.route("/player")
def player_profile():
    args = request.args
    player = NBAPlayer(f"{args.get("id")}.json")
    information = player.get_info()

    info = []

    info.append(information["POSITION"])

    try:
        info.append(f"{information["HEIGHT"].split(
            "-")[0]}'{information["HEIGHT"].split("-")[1]}\"")
    except:
        pass

    info.append(f"{information["WEIGHT"]} lbs")

    info.append(information["COUNTRY"])

    info.append(f"#{information["JERSEY"]}")

    if information["BIRTHDATE"] is not None:
        info.append(f"{information["BIRTHDATE"].split("T")[0].split("-")[1]}/{information["BIRTHDATE"].split(
            "T")[0].split("-")[2]}/{information["BIRTHDATE"].split("T")[0].split("-")[0]}")

    if information["DRAFT_YEAR"] == "Undrafted" or information["DRAFT_YEAR"] == "None":
        info.append("Undrafted")
    elif information["DRAFT_ROUND"] is None or information["DRAFT_NUMBER"] is None:
        info.append(f"{information["DRAFT_YEAR"]} NBA Draft")
    else:
        info.append(f"{information["DRAFT_YEAR"]} NBA Draft \n Round {
                    information["DRAFT_ROUND"]} Pick {information["DRAFT_NUMBER"]}")

    info.append(information["SCHOOL"])

    info = [x for x in info if x != "#" and x != " lbs"]

    random_player = choice(os.listdir("cache/")).split(".")[0]
    stats = player.get_stats_per_game()
    seasons = player.seasons()

    return render_template("players.html", player=player, stats=stats, seasons=seasons, info=info, random_player=random_player)
