from dotenv import load_dotenv   #load the .env file which has environmental variables (dynamic settings and ways to access software)
import os   #for loading the files (particular .env file)
import base64  #for encoding and decoding the base64 data
import json    #for json objects
from requests import post,get  #for HTTP requests
import random    #for randomizing the songs

"""
Steps to get the client id and secret:
1. make account
2. log into spotify developer website
3. go to dashboard
4. get the client id (visible) and the secret(visible by clicking show button)
"""
load_dotenv()   #load the .env file into current environment

client_id = os.getenv("CLIENT_ID") #get the Client ID of Spotify App
client_secret = os.getenv("CLIENT_SECRET")  #get the Client Secret of Spotify App

def get_token():  #get the access token using client credentials authorization flow
    auth_string = client_id + ":" + client_secret   
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")  #converts id:secret into bytes into base64 required by spotify api

    url = "https://accounts.spotify.com/api/token"     #spotify token endpoint
    headers = {
        "Authorization": "Basic " + auth_base64, #basic authorization - only username and password - identified by server - accessed by auth_base64
        "Content-Type": "application/x-www-form-urlencoded"  #used in spotify post request to identify type of content. it is a key:value pairs separated by &
    }
    data = {"grant_type": "client_credentials"}   #only client credentials used - only client id and secret
    result = post(url, headers=headers, data=data) #post request to spotify token api to get result
    json_result = json.loads(result.content)   #loads the json content part of result
    token = json_result["access_token"]     #gets the access token
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}  #for authorization to spotify app, the access token is used. 'bearer' is used to identify that token is an access token

def get_seeds(token, mood, seedTracks, seedArtists):  #seedtracks - tracks matching mood. seedartists - all artists of those songs
    url = "https://api.spotify.com/v1/search"   #endpoint for searching songs (like the search bar. random search can be done)
    headers = get_auth_header(token)  #get the authorization token
    query = f"?q={mood}&type=track&limit=5"   #query url: q for query. query item is the mood. search type are tracks. 5 tracks is limit

    query_url = url + query  #concatentate the urls
    result = get(query_url, headers=headers)   #get request to the url with the authorization token
    json_result = json.loads(result.content)["tracks"]["items"]  #load the json result and its tracks
    

    for item in json_result:     
        seedTracks.append(item["id"])   #put id of track is seedtracks
        for artist in item["artists"]:
            seedArtists.append(artist["id"])   #put id of artist in seedartists


def get_recommendation(token, seedTracks, seedArtists):
    url = "https://api.spotify.com/v1/recommendations"   #endpoint for recommended songs (like the filter button) based on track and artist given
    headers = get_auth_header(token)

    track = random.choice(seedTracks)   #randomly select a track
    artist = random.choice(seedArtists)  #randomly select an artist

    query = f"?limit=5&seed_artists={artist}&seed_tracks={track}"  #5 recommendations max. artist and track filters are given

    query_url = url + query   #concatenation of urls
    result = get(query_url, headers=headers)   #get request
    json_result = json.loads(result.content)["tracks"]  #parse the json response and get the <=5 tracks

    track = random.choice(json_result)   #get a random track from those tracks

    song_img_src = track["album"]["images"][2]["url"]  #gets the url of 3rd image of the album. 3rd is a good compromise between quality and load time
    song_url = track["external_urls"]["spotify"] #gets the external spotify url
    song_name = track["name"]    #gets the track name
    song_artists = []

    for artists in track["artists"]:
        song_artists.append(artists["name"]) #gets all artists

    

    song = [song_name, song_artists[0], song_url, song_img_src]  #only passes the first artist
    return song









