import requests
import json
import streamlit as st
API_KEY = st.secrets['openweather_api']

weatherConvert = {
    'Clear' : ["Clear"],
    "Cloudy" : ["Mist", "Clouds"],
    "Rain" : ["Drizzle", "Rain", "Snow", "Mist", 'Fog', 'Sand'],
    "Heavy Rain" : ["Thunderstorm", "Smoke", 'Haze', 'Dust', 'Ash', 'Squall', 'Tornado']
}

def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5//weather?lat={lat}&lon={lon}&units=metric&lang=en&Mode=weatherData&appid={API_KEY}&No Name=<string>"
    response = requests.request("GET", url, headers={}, data={})

    weatherData = json.loads(response.text)
    tempweathersit = weatherData['weather'][0]['main']
    temp = round(weatherData['main']['temp'], 2)
    hum = weatherData['main']['humidity']
    windspeed = round(weatherData['wind']['speed'], 4)
    for word,replacement in weatherConvert.items():
        if tempweathersit in replacement:
            weathersit = word
            break
    return {'weathersit':weathersit, 'temp':temp,'hum':hum,'windspeed':windspeed}


#13.74478887431261, 100.56404536486895

if __name__ == "__main__":
    print(get_weather(13.74478887431261, 100.56404536486895))