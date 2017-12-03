#/usr/bin/python3
import googlemaps
import json
from datetime import datetime
import time

gmaps = googlemaps.Client(client_id='YOUR CLIENT ID', key='YOUR SECRET KEY')

with open('Location History.json', encoding='utf-8-sig') as json_file:
   json_data = json.loads(text)

ret={}
cache={}
total=len(json_data['locations'])
count = 0
for punto in json_data['locations']:
    print(count,"/",total," locations checked")
    count=count+1
    ms=punto['timestampMs']
    month= str(datetime.datetime.fromtimestamp(float(ms)/1000.0).month)
    if len(month)==1:
       month="0"+month
    day = str(datetime.datetime.fromtimestamp(float(ms)/1000.0).day)
    if len(day)==1:
       day="0"+day
    date = str(datetime.datetime.fromtimestamp(float(ms)/1000.0).year) + month + day
    lat = float(punto['latitudeE7'])/10000000
    lon = float(punto['longitudeE7'])/10000000
    loc = None
    ck = str(round(lat))+str(round(lon))
    if (ck) in cache:
        print("Found ", ck, " in cache, representing: ",lat," / ", lon)
        loc = cache[ck]
    else:
        loc = gmaps.reverse_geocode((lat, lon))[0]['address_components']
        cache[ck]=loc
        print('Called gmaps')
        time.sleep(1)
    for line in loc:
        if 'country' in line['types']:
           if 'United Kingdom' in line['long_name']:
              print("Set in UK on Date ", date)
              ret[date]=True
           else:
              print("Not in UK: " + line['long_name'])
              ret[date]=False
summary={}
for date in ret:
   year = date[0:4]
   ty = None
   if date > (year + "0406"):
      ty = year + "/" + str((int(year)+1))
   else:
      ty = (str(int(year)-1)) + "/" + year
   try:
      summary[ty]['daysRecorded']=summary[ty]['daysRecorded']+1
      if ret[date] == True:
         summary[ty]['inUK']=summary[ty]['inUK']+1
   except KeyError:
      summary[ty]={}
      summary[ty]['daysRecorded']=1
      if ret[date] == True:
         summary[ty]['inUK']=1
