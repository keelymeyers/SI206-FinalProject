import requests 
import json
import plotly
import facebook
import datetime
import sqlite3

## Facebook API ##
access_token = None
if access_token == None:
    access_token = input("\nPlease provide access token\n")

CACHE_FNAME = "cached_fbdata.json"

try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

def get_facebook_data(me):
    if me in CACHE_DICTION:
        print ("Using cached data")
        facebook_results = CACHE_DICTION[me]
    else:
        print ('getting data from internet')
        graph = facebook.GraphAPI(access_token)
        user = graph.get_object('me') 
        facebook_results = graph.get_connections('me','feed', limit=100)
        CACHE_DICTION[me] = facebook_results
        fw = open(CACHE_FNAME,"w")
        fw.write(json.dumps(CACHE_DICTION))
        fw.close() # Close the open file
    return facebook_results

feed = get_facebook_data("Keely Meyers")
#print(json.dumps(feed, indent=4))


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


def get_time_of_day(y):
    hour = int(y["created_time"][11:13])
    if hour >= 0:
        if hour < 6:
            time_of_day = "12:00am - 5:59am"
        elif hour >= 6:
            if hour < 12:
                time_of_day = "6:00am - 11:59am"
            elif hour >= 12:
                if hour < 18:
                    time_of_day = "12:00pm - 5:59pm"
                elif hour >= 18:
                    time_of_day = "6:00pm - 11:59pm"
                else:
                    return ("not a valid time")
    return time_of_day


# Breaking code down by weekday

#weekday_counts = {}
#for activity in feed["data"]:
    #if get_weekday(activity) not in weekday_counts:
        #weekday_counts[get_weekday(activity)] = 1
    #else:
       #weekday_counts[get_weekday(activity)] += 1


# Breaking code down by time of day

monday_counts={}
tuesday_counts={}
wednesday_counts={}
thursday_counts={}
friday_counts={}
saturday_counts={}
sunday_counts={}
for activity in feed["data"]:
    if get_weekday(activity) == 'Monday':
        if get_time_of_day(activity) not in monday_counts:
            monday_counts[get_time_of_day(activity)] = 1
        else:
            monday_counts[get_time_of_day(activity)] += 1
    elif get_weekday(activity) == 'Tuesday':
        if get_time_of_day(activity) not in tuesday_counts:
            tuesday_counts[get_time_of_day(activity)] = 1
        else:
            tuesday_counts[get_time_of_day(activity)] += 1
    elif get_weekday(activity) == 'Wednesday':
        if get_time_of_day(activity) not in wednesday_counts:
            wednesday_counts[get_time_of_day(activity)] = 1
        else:
            wednesday_counts[get_time_of_day(activity)] += 1
    elif get_weekday(activity) == 'Thursday':
        if get_time_of_day(activity) not in thursday_counts:
            thursday_counts[get_time_of_day(activity)] = 1
        else:
            thursday_counts[get_time_of_day(activity)] += 1
    elif get_weekday(activity) == 'Friday':
        if get_time_of_day(activity) not in friday_counts:
            friday_counts[get_time_of_day(activity)] = 1
        else:
            friday_counts[get_time_of_day(activity)] += 1
    elif get_weekday(activity) == 'Saturday':
        if get_time_of_day(activity) not in saturday_counts:
            saturday_counts[get_time_of_day(activity)] = 1
        else:
            saturday_counts[get_time_of_day(activity)] += 1
    elif get_weekday(activity) == 'Sunday':
        if get_time_of_day(activity) not in sunday_counts:
            sunday_counts[get_time_of_day(activity)] = 1
        else:
            sunday_counts[get_time_of_day(activity)] += 1


# To avoid key errors when using plotly #

weekday_dictionaries = [monday_counts, tuesday_counts, wednesday_counts, thursday_counts, friday_counts, saturday_counts, sunday_counts]
times = ["12:00am - 5:59am", "6:00am - 11:59am", "12:00pm - 5:59pm", "6:00pm - 11:59pm"]
for w in weekday_dictionaries:
    for t in times:
        if t not in w:
            w[t] = 0


## SQL Database ##

conn = sqlite3.connect('206_FinalProject.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (post_id TEXT, day_of_week TEXT, time_of_day TEXT)')
for post in feed["data"]:
    tup = (post["id"], get_weekday(post), get_time_of_day(post))
    cur.execute('INSERT INTO Facebook (post_id, day_of_week, time_of_day) VALUES (?, ?, ?)', tup)

conn.commit()


## Data Visualization ## 

import plotly 
plotly.tools.set_credentials_file(username='keelym', api_key='pcDVvvfhyFvMo2CRErMZ')


import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('keelym', 'pcDVvvfhyFvMo2CRErMZ')



trace1 = go.Bar(x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], y=[monday_counts["12:00am - 5:59am"], tuesday_counts["12:00am - 5:59am"], wednesday_counts["12:00am - 5:59am"], thursday_counts["12:00am - 5:59am"], friday_counts["12:00am - 5:59am"], saturday_counts["12:00am - 5:59am"], sunday_counts["12:00am - 5:59am"]], name="12:00am - 5:59am")
trace2 = go.Bar(x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], y=[monday_counts["6:00am - 11:59am"], tuesday_counts["6:00am - 11:59am"], wednesday_counts["6:00am - 11:59am"], thursday_counts["6:00am - 11:59am"], friday_counts["6:00am - 11:59am"], saturday_counts["6:00am - 11:59am"], sunday_counts["6:00am - 11:59am"]], name="6:00am - 11:59am")
trace3 = go.Bar(x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], y=[monday_counts["12:00pm - 5:59pm"], tuesday_counts["12:00pm - 5:59pm"], wednesday_counts["12:00pm - 5:59pm"], thursday_counts["12:00pm - 5:59pm"], friday_counts["12:00pm - 5:59pm"], saturday_counts["12:00pm - 5:59pm"], sunday_counts["12:00pm - 5:59pm"]], name="12:00pm - 5:59pm")
trace4 = go.Bar(x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], y=[monday_counts["6:00pm - 11:59pm"], tuesday_counts["6:00pm - 11:59pm"], wednesday_counts["6:00pm - 11:59pm"], thursday_counts["6:00pm - 11:59pm"], friday_counts["6:00pm - 11:59pm"], saturday_counts["6:00pm - 11:59pm"], sunday_counts["6:00pm - 11:59pm"]], name="6:00pm - 11:59pm")


data = [trace1, trace2, trace3, trace4]
layout = go.Layout(barmode='stack')

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='facebook-stacked-bar')














