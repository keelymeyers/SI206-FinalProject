import requests 
import json
import plotly

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

def get_playlist_info(x):
	playlist_url = "https://api.spotify.com/v1/users/keelymeyers/playlists/6zJ9XA4stWwQZU0MPU3y79/tracks"
	d = {"keelymeyers", "6zJ9XA4stWwQZU0MPU3y79"}
	
	playlist_info = get_with_caching(playlist_url, d, saved_cache, cache_fname)
	print(playlist_info)
	print (json.loads(playlist_info))
	return json.loads(playlist_info)