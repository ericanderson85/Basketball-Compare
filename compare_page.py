from flask import render_template, request, Blueprint, redirect, url_for
from player_page import player
from search_page import search
from nbaplayer import NBAPlayer
import csv
from random_player import get_random_player
import json


compare = Blueprint(__name__, "compare")


@compare.route("/compare")
def compare_player():
    players = []
    with open('players.csv', "r", newline='', errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            players.append(row)
    args = request.args
    player_id = args.get("id")
    player = NBAPlayer(f"{player_id}.json")
    stats = player.get_stats_per_game()
    if args.get("season") == "all":
        season = player.seasons()
    else:
        season = args.get("season", None)
    random_player = get_random_player()

    return render_template("compare.html", player=player, stats=stats, season=season, random_player=random_player, players=players)


@compare.route('/process_headers')
def process_headers():
    selected_headers = request.args.get('selected_headers')
    if selected_headers == "%5B%5D":
        selected_headers = '%5B"PTS","AST","REB","BLK","STL"%5D'
    player_id = request.args.get('player_id')
    season = request.args.get('season')
    return redirect(url_for('comparison_page.player_comparison', s=selected_headers, id=player_id, season=season))
