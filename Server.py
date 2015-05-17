#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from Temperature import *
from Forecast import *
from IpGeoLoc import geoLoc
import time
from threading import Timer
from threading import Lock
import os

import sys
import Adafruit_DHT

SENSOR = 22
PIN = 4

PORT_NUMBER = 8080
data = []
lock = Lock()
continu = True
forecast = None

page = None

def readPageHmtl():
        page = ""
        try:
                myFile = mon_fichier = open("./page.html", "r")
                page = myFile.read()
                myFile.close()
        except Exception as e:
                print "Error : if you want run the server from an other repertory that Connected_Temperature write (cd the_path_of_Connected_Temperature && sudo python ./Server.py) i.e (cd /home/pi/Connected_Temperature && sudo python ./Server.py)"      
                page = "Error : if you want run the server from an other repertory that Connected_Temperature write (cd the_path_of_Connected_Temperature && sudo python ./Server.py) i.e (cd /home/pi/Connected_Temperature && sudo python ./Server.py)"
        return page

def refreshTemperature():
        if continu:
                humidity, temp = Adafruit_DHT.read_retry(SENSOR, PIN)
		temperature = Temperature(time.time(), temp, humidity)
		#temperature = Temperature(time.time(), random.randint(18, 25))
                #temp = 1
		if temp is not None:
                	lock.acquire()
                	Temperature.addNewValue(data, temperature)
                	lock.release()
		else:
			print 'Failed to get temperature'
                
                Timer(Temperature.REFRESH_DELAI() ,refreshTemperature, ()).start()

def refreshForecast():
        if continu:
                forecast.refresh()
                Timer(Forecast.REFRESH_DELAI() ,refreshForecast, ()).start()

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                if self.path == "/temperature":
                        res = self.responseTemperature()
                elif self.path == "/forecast":
                        res = self.responseForecast()
                else:
                        res = self.responseHome()
                        
                # Send the html message
                self.wfile.write(res)
                return

        def responseHome(self):
                return page

        def responseTemperature(self):
                lock.acquire()
                res = Temperature.tabToJsonReversed(data)
                lock.release()
                return res

        def responseForecast(self):
                lock.acquire()
                res = forecast.toJson(data[0])
                lock.release()
                return res

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Connected Temperature will start server on port' , PORT_NUMBER , 'in 1 minute'

	#wait 1 min before the first measure to have the correct time (cause of the network)
	time.sleep(60)

	lock.acquire()
	data = Temperature.initTab()
	lock.release()

	location = geoLoc()
	forecast = Forecast(location[0], location[1], location[2])
	
	refreshTemperature()
	refreshForecast()

	page = readPageHmtl()
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the server'
	continu = False
	server.socket.close()
