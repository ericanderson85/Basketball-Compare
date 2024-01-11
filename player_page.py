from flask import Blueprint, render_template, request
from nbaplayer import NBAPlayer
from random_player import get_random_player
import csv

teams = ['MEM', 'MIN', 'DAL', 'WAS', 'PHX', 'SAC', 'MIL', 'MIH', 'WAT', 'LAC', 'BAL', 'NOK', 'UTA', 'OKC', 'SAS', 'PHI', 'BOS', 'NOH', 'CHA', 'KCK', 'GOS', 'ATL', 'SFW', 'DN', 'MNL', 'BKN',
         'DET', 'DEN', 'IND', 'VAN', 'CAV', 'TOR', 'SDR', 'SEA', 'POR', 'CAP', 'NJN', 'SDC', 'LAL', 'HOU', 'ORL', 'NYK', 'GSW', 'NOP', 'FTW', 'MIA', 'NYN', 'BLT', 'CHI', 'STL', 'PHW', 'CHH']


player = Blueprint(__name__, "player")


@player.route("/player")
def player_profile():
    players = []
    with open('players.csv', "r", newline='', errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            players.append(row)
    args = request.args
    player = NBAPlayer(f"{args.get("id")}.json")

    random_player = get_random_player()
    stats = player.get_stats_per_game()
    seasons = player.seasons()
    info = player.get_info()
    team = info['TEAM_ABBREVIATION']
    if team == "":
        team = stats[seasons[0]]["TEAM_ABBREVIATION"]
    if team not in teams:
        team = "SAS"

    return render_template("players.html", player=player, stats=stats, seasons=seasons, random_player=random_player, players=players, info=info, team=team)
