import json
from urllib2 import URLError, Request, urlopen

def get_time_in_minutes(milliseconds):
    minutes, reminder = divmod(milliseconds, 60000)
    if reminder >= 50:
        minutes += 1
    return minutes

def meter_to_mile(meters):
    miles = meters / 1609.344
    return round(miles, 2)

def distance_for_a_destination(source_latitude, source_longitude, destination_latitude, destination_longitude):
    source = str(source_latitude) + ',' + str(source_longitude)
    destination = str(destination_latitude) + ',' + str(destination_longitude)
    request_string = "http://localhost:8989/route?point=" + source + "&point=" + destination + "&optimize=true&vehicale=car"
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meter_to_mile(paths[0]["distance"])
        time = get_time_in_minutes(paths[0]["time"])
        result = [distance, time]
    except Exception:
        result = [-1, -1]
    return result

def distance_for_multiple_destinations(source_latitude, source_longitude, first_destination_latitude, first_destination_longitude, second_destination_latitude, second_destination_longitude):
    source = str(source_latitude) + ',' + str(source_longitude)
    first_destination = str(first_destination_latitude) + ',' + str(first_destination_longitude)
    second_destination = str(second_destination_latitude) + ',' + str(second_destination_longitude)
    request_string = "http://localhost:8989/route?point=" + source + "&point=" + first_destination + "&point=" + second_destination + "&optimize=true&vehicale=car"
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meter_to_mile(paths[0]["distance"])
        time = get_time_in_minutes(paths[0]["time"])
        result = [distance, time]
    except Exception:
        result = [-1, -1]
    return result

def distance_from_jfk(*cordinates):
    queryString = str(cordinates[0][0]) + ',' + str(cordinates[0][1])
    for i in range(2,len(cordinates[0]),2):
        queryString+="&point=" + str(cordinates[0][i]) + ',' + str(cordinates[0][i+1])
    queryString+="&optimize=true&vehicle=car"    
    request_string = "http://localhost:8989/route?point=" + queryString
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meter_to_mile(paths[0]["distance"])
        time = get_time_in_minutes(paths[0]["time"])
        result = [distance, time]
    except Exception:
        result = [-1, -1]
    return result

def get_coordinates(*cordinates):
    queryString = str(cordinates[0][0]) + ',' + str(cordinates[0][1])
    for i in range(2,len(cordinates[0]),2):
        queryString+="&point=" + str(cordinates[0][i]) + ',' + str(cordinates[0][i+1])
    queryString+="&optimize=true&vehicle=car&points_encoded=false"    
    request_string = "http://localhost:8989/route?point=" + queryString
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        result = paths[0]["points"]
    except Exception:
        result = [-1, -1]
    return result

def distance_from_source(*cordinates):
    queryString = str(cordinates[0][0]) + ',' + str(cordinates[0][1])
    for i in range(2,len(cordinates[0]),2):
        queryString+="&point=" + str(cordinates[0][i]) + ',' + str(cordinates[0][i+1])
    queryString+="&optimize=true"    
    request_string = "http://localhost:8989/route?point=" + queryString
    request = Request(request_string)
    try:
        response = urlopen(request)
        output = json.loads(response.read())
        paths = output["paths"]
        distance = meter_to_mile(paths[0]["distance"])
        time = get_time_in_minutes(paths[0]["time"])
        result = [distance, time]
    except Exception:
        result = [-1, -1]
    return result       
#print distance_from_jfk(40.737015, -73.98833, 40.774783, -74.02082)
#print distance_from_jfk((40.737015, -73.98833, 40.774783, -74.02082, 40.744759, -74.060325))    
