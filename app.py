from flask import Flask, render_template
from player_page import player
from search_page import search
from compare_page import compare
from comparison_page import comparison
from random_player import get_random_player
import csv

app = Flask(__name__)
app.register_blueprint(player, url_prefix="/")
app.register_blueprint(search, url_prefix="/")
app.register_blueprint(compare, url_prefix="/")
app.register_blueprint(comparison, url_prefix="/")


@app.route("/")
def home():
    # List of players for autocomplete
    players = []
    with open('players.csv', "r", newline='', errors="ignore") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            players.append(row)
    random_player = get_random_player()
    return render_template("index.html", random_player=random_player, players=players)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
