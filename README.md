# Connected_Temperature

CONNECT THE SENSOR:

connect the data wired of your sensor to the GPIO4 of your raspberry

if you have a problem https://learn.adafruit.com/downloads/pdf/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging.pdf

INSTALL THE SERVER:

git clone https://github.com/raffi3438/Connected_Temperature.git

cd Connected_Temperature



INSTALL THE LIBRARY FOR THE SENSOR:

git clone https://github.com/adafruit/Adafruit_Python_DHT.git

cd Adafruit_Python_DHT

sudo apt-get update

sudo apt-get install build-essential python-dev

sudo python setup.py install

cd ../


RUN THE SERVER:

sudo python ./Server.py

if you want run the server from an other repertory that Connected_Temperature (cd the_path_of_Connected_Temperature && sudo python ./Server.py)

i.e (cd /home/pi/Connected_Temperature && sudo python ./Server.py)


ENJOY:

go on your favorite browser and write the url ip_of_your_raspberry:8080
