import requests 
import json
import plotly
import spotipy
import facebook
import datetime
import facebook_info

CACHE_FNAME = "cached_data.json"
# Put the rest of your caching setup here:

try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = params)
    prepped = req.prepare()
    return prepped.url

def get_with_caching(base_url, params_diction, cache_diction, cache_fname):
    full_url = requestURL(base_url, params_diction)
    if full_url in cache_diction:
        #logging.info("retrieving cached result for " + full_url)
        return cache_diction[full_url]
    else:
        response = requests.get(base_url, params=params_diction)
        #logging.info("adding cached result for " + full_url)
        cache_diction[full_url] = response.text
        fobj = open(cache_fname, "w")
        pickle.dump(cache_diction, fobj)
        fobj.close()
        return response.text


## Facebook API ##
access_token = facebook_info.access_token
r = requests.get("https://graph.facebook.com/v2.3/me/feed",params={"limit":100, "access_token":access_token})


#access_token = None
#if access_token is None:
    #access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

graph = facebook.GraphAPI(access_token)
user = graph.get_object('me') 
feed = graph.get_connections('me','feed', limit=100)
#print(json.dumps(feed, indent = 4))


datetime.datetime.today()
datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
datetime.datetime.today().weekday()

today = datetime.datetime(2017, 12, 7)
weekday = today.weekday()
#print(weekday)


def get_weekday(x):

    year = x["created_time"][:4]
    #print(year)
    month = x["created_time"][5:7]
    #print(month)
    day = x["created_time"][8:10]
    #print(day)
    weekday_tuple = (year, month, day)
    day_of_week = datetime.datetime(int(year), int(month), int(day))
    weekday = day_of_week.weekday()
    if weekday == 0:
        weekday ="Monday"
    elif weekday == 1:
        weekday ="Tuesday"
    elif weekday == 2:
        weekday ="Wednesday"
    elif weekday == 3:
        weekday ="Thursday"
    elif weekday == 4:
        weekday ="Friday"
    elif weekday == 5:
        weekday ="Saturday"
    elif weekday == 6:
        weekday = "Sunday"
    else:
        print("NOT A VALID DATE")


    return weekday




for activity in feed["data"]:
    print(get_weekday(activity))



















#graph = facebook.GraphAPI(access_token)
#all_fields = ['name', 'created_at']
#all_fields = ','.join(all_fields)
#posts = graph.get_connections('me','likes', fields = all_fields, limit=100) 

#print(len(posts["data"]))
#print(json.dumps(posts, indent = 4))



##### Spotify API ####

## music3 playlist id: 6zJ9XA4stWwQZU0MPU3y79
## user id: 1e64d1a09838405e9eaa201d162bddf8



#username = "keelymeyers"
#playlist = "6zJ9XA4stWwQZU0MPU3y79"
#sp = spotipy.Spotify()
##sp_playlist = sp.user_playlist_tracks(username, playlist_id=playlist)
#tracks = sp_playlist['items']
#print (tracks)

#print(sp.current_user_recently_played(limit=100))


#import requests_oauthlib
#import webbrowser
#import json

#CLIENT_ID = "1e64d1a09838405e9eaa201d162bddf8"
#CLIENT_SECRET = "ade3635c31c4463980eeb2d1ec998f1f"
#AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'

# NOTE: you need to specify this same REDIRECT_URI in the Spotify API console
#REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'

#oauth = requests_oauthlib.OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)

#authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)#, access_type="offline", approval_prompt="force")

#webbrowser.open(authorization_url)
#authorization_response = raw_input('Enter the full callback URL')

# the OAuth2Session instance has a method that extracts what we need from the url, and does some other back and forth with spotify
#TOKEN_URL = 'https://accounts.spotify.com/api/token'
#token = oauth.fetch_token(TOKEN_URL, authorization_response=authorization_response, client_secret=CLIENT_SECRET)

# Now we can just use the get method from here on out to make requests to spotify endpoints
#r = oauth.get('https://api.spotify.com/v1/me')
#print (r.url)
#response_dict = json.loads(r.text)
#print (json.dumps(response_dict, indent=2))

#base_url = "https://api.spotify.com"










