class ForecastDay:
    def __init__(self, lastUpdateTime, tempMin, tempMax, windSpeed, icon, message):
        self.lastUpdateTime = lastUpdateTime
        self.tempMin = tempMin
        self.tempMax = tempMax
        self.windSpeed = windSpeed
        self.icon = icon
        self.message = message


    def __repr__(self):
        return "tempMin: " + str(self.tempMin) + " tempMax: " + str(self.tempMax) + " windSpeed: " + str(self.windSpeed) + " icon " + self.icon + " message: " + self.message + ", lastUpdateTime: " + str(self.lastUpdateTime)

    def __str__(self):
        return self.__repr__()

    def toJson(self):
        return '{"tempMin": ' + '{0:0.1f}'.format(self.tempMin) + ', "tempMax": ' + '{0:0.1f}'.format(self.tempMax) + ', "windSpeed": ' + str(self.windSpeed) + ', "icon":" ' + self.icon + '", "message": "' + self.message + '", "lastUpdateTime": ' + str(self.lastUpdateTime) + "}"

if __name__ == '__main__':
    forecastday = ForecastDay(144455.5, 15, 25, 10, "10d", "rain")
    print forecastday
    print forecastday.toJson()
