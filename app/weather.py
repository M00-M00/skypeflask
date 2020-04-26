from flask import render_template
import requests
import json

location = "Edinburgh"
getLocationIdUrl = 'https://www.metaweather.com/api/location/search/?query=' + location

getLocationId = requests.request("GET", getLocationIdUrl)
woeid = json.loads(getLocationId.text)[0]["woeid"]

getWeatherUrl = 'https://www.metaweather.com/api/location/' + str(woeid)

getWeather = requests.request("GET", getWeatherUrl)

tempData = json.loads(getWeather.text)["consolidated_weather"][0]

CurrentTemp = tempData["the_temp"]
WeatherState = tempData["weather_state_name"]
WindSpeed = tempData["wind_speed"]




iconDict = {
    "Name":"Abbreviation",
    "Snow":"sn",
    "Sleet":"sl",
    "Hail":"h"	,
    "Thunderstorm" :"t",
    "Heavy Rain":"hr",
    "Showers":"s"	,
    "Heavy Cloud":"hc",
    "Light Cloud":"lc"	,
    "Clear":"c"
            }

iconUrl = 	"https://www.metaweather.com/static/img/weather/png/{}.png".format(iconDict[WeatherState])
