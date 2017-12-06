import requests 
import json
import plotly
import spotipy
import facebook

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
access_token = "EAACEdEose0cBAMFRMZCjaqX1nFwZC6zNmg5ZCn4ZBpz4qwbfKuD1ucD3a8Jg3bptvHxANH1GVzZCB22mlrrHcLgwK6LfqkBV54ZCwzcW6JBdNHW0GLcvZAzlthxBOztlTw672MiE5PuasNZAy4IxayIqcMRsf8BXoUZBWFQdNhki3rib57HuwYnvx0Cd9AcuwgZBoZD"
r = requests.get("https://graph.facebook.com/v2.3/me/feed",params={"limit":2, "access_token":access_token})


#access_token = None
#if access_token is None:
    #access_token = input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

graph = facebook.GraphAPI(access_token)
user = graph.get_object('me') 
likes = graph.get_connections('me','likes')
print(json.dumps(likes, indent = 4))

