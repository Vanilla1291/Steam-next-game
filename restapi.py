from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def index():
	return render_template("index.html")


@app.route("/stat", methods = ["GET", "POST"])
def getOwnedGames():
	if request.method == "POST":
		steam_id = str(request.form["SteamID"])
	return render_template("stats.html", id=steam_id)

