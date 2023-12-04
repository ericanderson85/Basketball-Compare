from flask import Blueprint, render_template, request
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
    with open('players.csv', "r", newline='', errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if search.lower() in row["Name"]:
                search_results.append(row)
        for player in search_results:
            player["Name"] = player["Name"].title()
        if len(search_results) > 20:
            search_results = search_results[:20]

    return render_template("search.html", search_results=search_results, random_player=random_player, player=None)
