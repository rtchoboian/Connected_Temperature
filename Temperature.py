# -*- coding: cp1252 -*-

from time import sleep, time
import random
from json import JSONEncoder

class Temperature:    
    @staticmethod
    def TAB_SIZE_MAX():
        return 288 #measure every 5 minutes during 24 hours

    @staticmethod
    def TEMPERATURE_UNITY():
        return "°C"

    @staticmethod
    def HUMIDITY_UNITY():
        return "%"

    @staticmethod
    def REFRESH_DELAI():
        return 300 #60 secondes * 5 minutes
    
    def __init__(self, date, value, humidity):
        self.date = date
        self.value = value
        self.humidity = humidity

    def valueToString(self):
        return '{0:0.1f}'.format(self.value)

    def humidityToString(self):
        return '{0:0.1f}'.format(self.humidity)

    def toJson(self):
        return '{"temp":' + self.valueToString() + ',"time":' + str(self.date)+ '}'


    @staticmethod
    def tabToJson(tabOfTemperatures):
        res = ""
        first = True
        for i in range(len(tabOfTemperatures)):
            temp = tabOfTemperatures[i]
            if (temp != None):
                if first:
                    first = False
                else:
                    res += ", "
                    
                res += temp.toJson()
        return res

    @staticmethod
    def tabToJsonReversed(tabOfTemperatures):
        res = []
        for x in reversed(range(len(tabOfTemperatures))):
            temp = tabOfTemperatures[x]
            if temp != None:
                res.append(temp.toJson())
        return '[ ' + ', '.join(res) + ' ]'

    @staticmethod
    def initTab():
        tabOfTemperatures = []
        for i in range(Temperature.TAB_SIZE_MAX()):
            tabOfTemperatures.append(None)
        return tabOfTemperatures

    @staticmethod
    def initTab2():
        tabOfTemperatures = Temperature.initTab()
        for i in range(Temperature.TAB_SIZE_MAX()):
            Temperature.addNewValue(tabOfTemperatures, Temperature(time() + i*60*5, random.randint(18, 25))) #add 5 min each elem
        return tabOfTemperatures
     
    @staticmethod
    def addNewValue(tabOfTemperatures, temperature):
        #right shift
        for i in reversed(range(Temperature.TAB_SIZE_MAX() - 1)): #delete the last elem
            tabOfTemperatures[i+1] = tabOfTemperatures[i]
        #add the new value
        tabOfTemperatures[0] = temperature
