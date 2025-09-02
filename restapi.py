from flask import Flask
from flask import request
from flask import render_template
import requests
import csv

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
			unplayed = getUnplayedGames(ownedGames)
			recently = getRecentGames(steam_id)
			recentTags = getRecentTags(recently)
			weights = calculateWeights(unplayed, recentTags)
			sortedGames = sorted(weights, key=weights.get, reverse=True)
			topGames = sortedGames[0] + ", " + sortedGames[1]
			

		except Exception as e:
			print(e)
			return "<h1>An Error has Occured. Please make your profile public.</h1>"
	else:
		print("Error")
	return render_template("stats.html", games=topGames)



def getUnplayedGames(games):
	unplayed = {}
	#"response""games""this one goes through each game" so 0 is the first game alphabetically 
	
	for i in range(len(games["response"]["games"])):#looks at how many games you have to loop through and check where the game time is 0
		if games["response"]["games"][i]["playtime_forever"] == 0:
			unplayed[games["response"]["games"][i]["name"]] = games["response"]["games"][i]["appid"]
	return unplayed

def getRecentGames(steam_id):
	recentDict = {}
	recentGamesURL =  "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=C12F3831CCC6A47C1FE4D87E45194A83&steamid=" + steam_id + "&format=json"
	recentGames = requests.get(recentGamesURL).json()
	for i in range(len(recentGames["response"]["games"])):
		recentDict[recentGames["response"]["games"][i]["name"]] = recentGames["response"]["games"][i]["appid"]
	return recentDict


def getRecentTags(recent):
	tagCount = {}
	tagsURL = "http://steamspy.com/api.php?request=appdetails&appid="
	for i in recent:
		r = requests.get(tagsURL + str(recent[i])).json()
		for j in r["tags"]: #ouch this has got some terrible time complexity
			if j in tagCount.keys():
				tagCount[j] = tagCount[j] + 1
			else:
				tagCount[j] = 1
	return tagCount
	

def calculateWeights(unplayed, recentTags):
	tagsURL = "http://steamspy.com/api.php?request=appdetails&appid="
	pointsDict = {}
	points = 0
	for i in unplayed:
		r = requests.get(tagsURL + str(unplayed[i])).json() # gets the tags of a single game
		points = 0
		for j in r["tags"]:
			if j in recentTags.keys():
				points += recentTags[j]
		pointsDict[i] = points
	return pointsDict



	


# look at recently played games genre tags and add them in a counter. So for example, say you play two horror games, then the horror tag weighting would be 2.
#So then your most played genre would be up top. Which means that any games with that genre are more likely to be recommended to play.
#Essentially you get every unplayed game, get its tags and add points to it by adding how many times said tag has appeared in your recently played. So if you haven't played
#a 2D game but have played 4 2D games recently then any 2D game will get 4 points

