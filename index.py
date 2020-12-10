#import os#
from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
app = Flask(__name__)
import os
app.secret_key = b"random bytes representing flask secret key"
# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 747508486627393717    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "3dvR66Khglq_Ss3968yBQWr9wPTINNdU"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://lotusbot.tk/callback"                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "NzQ3NTA4NDg2NjI3MzkzNzE3.X0P5hw.IcwrYfsxVx2c4ksLxpz_wVhoc2I"                    # Required to access BOT resources.


discord = DiscordOAuth2Session(app)



HYPERLINK = '<a href="{}">{}</a>'


@app.route("/")
def home():
    if not discord.authorized:
        return render_template("index.html")
        #{HYPERLINK.format(url_for(".login"), "Login")} <br />
        #{HYPERLINK.format(url_for(".login_with_data"), "Login with custom data")} <br />
        #{HYPERLINK.format(url_for(".invite_bot"), "Invite Bot with permissions 8")} <br />
        #{HYPERLINK.format(url_for(".invite_oauth"), "Authorize with oauth and bot invite")}

    return render_template("index2.html")
    #{HYPERLINK.format(url_for(".me"), "@ME")}<br />
    #{HYPERLINK.format(url_for(".logout"), "Logout")}<br />
    #{HYPERLINK.format(url_for(".user_guilds"), "My Servers")}<br />
    #{HYPERLINK.format(url_for(".add_to_guild", guild_id=748423207891238933), "Add me to 748423207891238933.")}    
    #"""


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/login-data/")
def login_with_data():
    return discord.create_session(data=dict(redirect="/me/", coupon="15off", number=15, zero=0, status=False))


@app.route("/invite-bot/")
def invite_bot():
    return discord.create_session(scope=["bot"], permissions=8, guild_id=464488012328468480, disable_guild_select=True)


@app.route("/invite-oauth/")
def invite_oauth():
    return discord.create_session(scope=["bot", "identify"], permissions=8)


@app.route("/callback/")
def callback():
  data = discord.callback()
  redirect_to = data.get("redirect", "/")
  return redirect(redirect_to)

@app.route("/me/")
def me():
    user = discord.fetch_user()
    return f"""
    <html>
    <head>
    <title>{user.name}</title>
    <link rel="icon" href=" {url_for('static', filename='image/roxy.png')}">
    <meta name="viewport" content="width=device-width, initial-scale=1" /> 
    </head>
    <body><img src='{user.avatar_url or user.default_avatar_url}' />
    <p>Is avatar animated: {str(user.is_avatar_animated)}</p>
    <a href={url_for("my_connections")}>Connections</a>
    <br />
    </body>
    </html>
    """


@app.route("/me/guilds/")
def user_guilds():
    guilds = discord.fetch_guilds()
    return f"""
    <head>
    <title> Roxy </title>
     <link rel="icon" href=" {url_for('static', filename='image/roxy.png')}">
     <meta name="viewport" content="width=device-width, initial-scale=1" /> 
    </head>
    <p>All together, you are in {len(guilds)} guilds!<p>
    <hr>
    
    {"<br />".join([f'[ADMIN] {g.name}' if g.permissions.administrator else g.name for g in guilds])}
    """


@app.route("/add_to/<int:guild_id>/")
def add_to_guild(guild_id):
    user = discord.fetch_user()
    return user.add_to_guild(guild_id)


@app.route("/me/connections/")
def my_connections():
    user = discord.fetch_user()
    connections = discord.fetch_connections()
    return f"""
<html>
<head>
<title>{user.name}</title>
 <link rel="icon" href=" {url_for('static', filename='image/roxy.png')}">
 <meta name="viewport" content="width=device-width, initial-scale=1" /> 
</head>
<body>
{str([f"{connection.name} - {connection.type}" for connection in connections])}
</body>
</html>
"""


@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for(".home"))


@app.route("/secret/")
@requires_authorization
def secret():
    return os.urandom(16)


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = "5000", debug = True)
    
