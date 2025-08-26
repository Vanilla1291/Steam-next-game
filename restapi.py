from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/stats")
def getOwnedGames():
	return "<p>Hello</p>"

