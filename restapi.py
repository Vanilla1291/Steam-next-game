from flask import Flask
from flask import request
from flask import render_template
import requests

app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def index():
	return render_template("index.html")


@app.route("/stat", methods = ["GET", "POST"])
def getOwnedGames():
	steam_id = ""
	if request.method == "POST":
		steam_id = str(request.form["SteamID"])
		ownedGamesURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=C12F3831CCC6A47C1FE4D87E45194A83&steamid=" + steam_id + "&format=json"
		r = requests.get(ownedGamesURL)
		print(r.json())
	else:
		print("Error")
	return render_template("stats.html", id=steam_id)

