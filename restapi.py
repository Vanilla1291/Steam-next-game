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
		ownedGamesURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=C12F3831CCC6A47C1FE4D87E45194A83&steamid=" + steam_id + "&include_appinfo=true"+ "&format=json"
		try:
			r = requests.get(ownedGamesURL) 
			ownedGames = r.json() #json returns time played in minutes. Doesn't really matter cause all I need is playtime_forever to be 0
			getUnplayedGames(ownedGames)
		except:
			return "<h1>An Error has Occured</h1>"
	else:
		print("Error")
	return render_template("stats.html", games=ownedGames)



def getUnplayedGames(games):
	unplayed = []
	#"response""games""this one goes through each game" so 0 is the first game alphabetically 
	print(len(games["response"]["games"])) # 134 which is how many games I have, perfect

	for i in range(len(games["response"]["games"])):#looks at how many games you have to loop through and check where the game time is 0
		if games["response"]["games"][i]["playtime_forever"] == 0:
			unplayed.append(games["response"]["games"][i]["name"])
	print(unplayed)

