from flask import render_template, request, Blueprint, redirect, url_for
from player_page import player
from search_page import search
from nbaplayer import NBAPlayer
import json


compare = Blueprint(__name__, "compare")


@compare.route("/compare")
def compare_player():
    args = request.args
    player_id = args.get("id")
    player = NBAPlayer(f"{player_id}.json")
    stats = player.get_stats_per_game()
    if args.get("season") == "all":
        season = player.seasons()
    else:
        season = args.get("season", None)

    return render_template("compare.html", player=player, stats=stats, season=season)


@compare.route('/process_headers')
def process_headers():
    selected_headers = request.args.get('selected_headers')
    player_id = request.args.get('player_id')
    season = request.args.get('season')
    return redirect(url_for('comparison_page.player_comparison', s=selected_headers, id=player_id, season=season))
