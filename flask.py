import os
from requests_oauthlib import OAuth2Session
import getpass
import os
import requests
import json
from flask import Flask, session, redirect, request, render_template


# Find all data on https://discord.com/developers
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Leave it like this!
base_discord_api_url = 'https://discord.com/api' # Leave it like this!
client_id = 000000000000 #client_id
client_secret = '' # client_secret
redirect_uri = '.../oauth_callback' #oauth_callback_url replace ...
scope = ['identify'] # scopes
token_url = 'https://discordapp.com/api/oauth2/token' #Leave it like this!
authorize_url = 'https://discordapp.com/api/oauth2/authorize' #Leave it like this!


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def home():
  return redirect("/login")


@app.route("/login")
def login():
    try:
        discord1 = OAuth2Session(client_id, token=session['discord_token'])
        response = discord1.get(base_discord_api_url + '/users/@me')
        return redirect("/")
    except:
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        login_url, state = oauth.authorization_url(authorize_url)
        session['state'] = state
        return redirect(login_url)



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/oauth_callback")
async def oauth_callback():
    try:
        discord1 = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
        token = discord1.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )
        session['discord_token'] = token

        discord1 = OAuth2Session(client_id, token=session['discord_token'])
        response = discord1.get(base_discord_api_url + '/users/@me')

        
        return f"{response.json()}"

    except:
        return redirect("/404")




app.run(debug=True)

