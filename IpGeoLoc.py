import urllib2
import json
from json import JSONEncoder


def geoLoc():
    """this function may rise an exception if there is a problem with the server or the json
        return [lat, lon, cityName] or the location of Paris"""
    requete = urllib2.Request('http://ip-api.com/json')
    resultat = urllib2.urlopen(requete)
    resultatJson = json.loads(resultat.read())
    try:
        lat = resultatJson['lat']
        lon = resultatJson['lon']
        city = resultatJson['city']
        return [lat, lon, city]
    except Exception as e:
        return [48.858746, 2.349120, "Paris"];
    
if __name__ == '__main__':
   print geoLoc()
