from flask import Flask, render_template
from player_page import player
from search_page import search
from compare_page import compare
from comparison_page import comparison
from random import choice
import os

app = Flask(__name__)
app.register_blueprint(player, url_prefix="/")
app.register_blueprint(search, url_prefix="/")
app.register_blueprint(compare, url_prefix="/")
app.register_blueprint(comparison, url_prefix="/")


@app.route("/")
def home():
    random_player = choice(
        os.listdir("static/images/")).split(".")[0]
    return render_template("index.html", random_player=random_player, player=None)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
