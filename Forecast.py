import urllib2
import json
from json import JSONEncoder
import time
from ForecastDay import ForecastDay
from Temperature import Temperature

class Forecast:
    @staticmethod
    def REFRESH_DELAI():
        return 3600 #60 secondes * 60 minutes
    
    def __init__(self, latitude, longitude, city):
        self.latitude = latitude
        self.longitude = longitude
        self.geoloc = city
        self.lastUpdateTempNowTime = None
        self.tempNow = None
        self.today = None
        self.tomorrow = None

    def __repr__(self):
        return "geoloc: " + str(self.geoloc) + ", coordinates: (" + str(self.latitude) + "," + str(self.longitude) + ") tempNow: " + str(self.tempNow) + "(" + str(self.lastUpdateTempNowTime) + "), today: (" + str(self.today) + "), tomorrow: (" + str(self.tomorrow) + ")"
    
    def __str__(self):
        return self.__repr__()

    def toJson(self, tempInNow):
        if self.geoloc != None:
            geoloc = str(self.geoloc)
        else:
            geoloc = "null "
            
        if self.latitude != None:
            lat = str(self.latitude)
        else:
            lat = "null "

        if self.longitude != None:
            lon = str(self.longitude)
        else:
            lon = "null "

        if tempInNow != None:
            tempInNowValue = '{0:0.1f}'.format(tempInNow.value)
            luiTNT = str(tempInNow.date)
        else:
            tempInNowValue = "null "
            luiTNT = "null "
            
        if self.tempNow != None:
            tempNow =  '{0:0.1f}'.format(self.tempNow)
        else:
            tempNow = "null "

        if self.lastUpdateTempNowTime != None:
            #luTNT = ', "lastUpdateTempNowTime":' + luTNT
            luTNT =  str(self.lastUpdateTempNowTime)
        else:
            #luTNT = ""
            luTNT = "null "
            
        if self.today != None:
            todayJson = self.today.toJson()
        else:
            todayJson = "null "
            
        if self.tomorrow != None:
            tomorrowJson = self.tomorrow.toJson()
        else:
            tomorrowJson = "null "
            
        return '{"coordinates": {"lat":' + lat + ', "lon":' + lon + '}, "geoloc": "' + geoloc + '", "tempOutNow": ' + tempNow + ', "lastUpdateTempOutNowTime":' + luTNT + ', "tempInNow": ' + tempInNowValue+ ', "lastUpdateTempInNowTime":' + luiTNT + ', "today": ' + todayJson + ', "tomorrow": ' +tomorrowJson + '}'


    def refresh(self):
        """this function may rise an exception if there is a problem with
        the server or the json"""
        self.refreshNow()
        self.refreshForecastDays()

    def refreshNow(self):
        """this function may rise an exception if there is a problem with
        the server or the json"""
        #http://api.openweathermap.org/data/2.5/weather?lat=45.7667&lon=4.8833&mode=json&units=metric
        requete = urllib2.Request('http://api.openweathermap.org/data/2.5/weather?lat=' + str(self.latitude)
                                  + '&lon=' + str(self.longitude)+ "&mode=json&units=metric")
        resultat = urllib2.urlopen(requete)
        resultatJson = json.loads(resultat.read())
        try:
            temp = resultatJson['main']["temp"]
            if temp != None:
                self.tempNow = temp
                self.lastUpdateTempNowTime = time.time()
        except Exception as e:
            self.tempNow = None
            self.lastUpdateTempNowTime = None

    def refreshForecastDays(self):
        """this function may rise an exception if there is a problem with
        the server or the json"""
        #http://api.openweathermap.org/data/2.5/forecast/daily?lat=45.7667&lon=4.8833&mode=json&units=metric&cnt=2
        requete = urllib2.Request('http://api.openweathermap.org/data/2.5/forecast/daily?lat=' + str(self.latitude) + '&lon=' + str(self.longitude) + "&mode=json&units=metric&cnt=2")
        resultat = urllib2.urlopen(requete)
        resultatJson = json.loads(resultat.read())
        try:
            results = resultatJson['list']
            day1 = results[0]
            today = ForecastDay(time.time(), day1['temp']['min'], day1['temp']['max'], day1['speed'], day1['weather'][0]['icon'], day1['weather'][0]['icon'])
            self.today = today
            day2 = results[1]
            tomorrow = ForecastDay(time.time(), day2['temp']['min'], day2['temp']['max'], day2['speed'], day2['weather'][0]['icon'], day2['weather'][0]['icon'])
            self.tomorrow = tomorrow
        except Exception as e:
            self.today = None
            self.tomorrow = None


if __name__ == '__main__':
   forecast = Forecast(48.858746, 2.349120, "Paris")
   forecast.refresh()
   print str(forecast)
   print forecast.toJson(Temperature(time.time, 14.585, 50.006))


