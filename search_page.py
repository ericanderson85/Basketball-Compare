from flask import Blueprint, render_template, request, redirect, url_for
from random import choice
import csv
import os

search = Blueprint(__name__, "search")


@search.route("/search")
def search_for_player():
    args = request.args
    search = args.get("search")
    random_player = choice(os.listdir("cache/")).split(".")[0]
    search_results = []
    large = False
    with open('players.csv', "r", newline='', errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if search.lower() in row["Name"]:
                search_results.append(row)
        if len(search_results) == 1:
            return redirect(url_for("player_page.player_profile",
                                    id=search_results[0]["ID"]))
        for player in search_results:
            player["Name"] = player["Name"].title()
        if len(search_results) > 36:
            large = True
            search_results = search_results[:36]

    return render_template("search.html", search_results=search_results, random_player=random_player, player=None, large=large)
