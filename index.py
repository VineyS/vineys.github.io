######################
### IMPORT MODULES ###
######################

from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
import json


#####################
### CONFIGURATION ###
##################### 

app = Flask(__name__)

fp = open('value.json', 'r')
val = json.load(fp)
print(val)

#####################
###  VAR FILLING  ###
#####################

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true" 
app.config["DISCORD_CLIENT_ID"] = int(val["client_id"])
app.config["DISCORD_CLIENT_SECRET"] = val["client_secret"]
app.config["DISCORD_REDIRECT_URI"] = val["redirect_uri"]
app.config["DISCORD_BOT_TOKEN"] = val["token"]

discord = DiscordOAuth2Session(app)

#####################
###   WEB PAGES   ###
#####################

@app.route("/")
def home():
  if not discord.authorized:
    return render_template("index.html")


if __name__ == "__main__":
  app.run(host = "0.0.0.0" , port = 5000 , debug = True)