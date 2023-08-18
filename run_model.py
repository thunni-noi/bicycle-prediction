import pickle
from google_drive_downloader import GoogleDriveDownloader as gdd
import streamlit as st
import pathlib

if st.secrets['current_platform'] != "pc" :
    pathlib.WindowsPath = pathlib.PosixPath
    
    
model_path = pathlib.Path('model/main_model.pkl')
if not model_path.exists():
    gdd.download_file_from_google_drive('1-_ASCNLnejh4BcERp8vPoFxPAU_ZedqT', model_path)

model = pickle.load(open(model_path, 'rb'))
#acceptable list
seasonList = ['Spring','Summer','Fall','Winter']
weatherList = ['Clear','Cloudy','Rain','Heavy Rain']
inputList = ['season','mnth','hr','workingday','weathersit','temp','hum','windspeed','cluster','id']
def start_predict(weatherData, month, hr, workingday=True):
    if month <= 2 : season = seasonList[3]
    elif month <= 6 : season = seasonList[1]
    elif month <= 10 : season = seasonList[2]
    else : season = seasonList[0]
    temp = round(weatherData['temp'] / 41, 2)
    hum = round(weatherData['hum'] / 100, 2)
    windspeed = round(weatherData['windspeed'] / 67, 4)
    
    parameter = {'season' : season, 'mnth' : month - 1, 'hr' : hr-1, 'workingday' : workingday, 'weathersit':weatherData['weathersit'],'temp' : temp, 'windspeed' : windspeed , 'id' : 0}
    prediction = model.predict(parameter)
    return prediction



if __name__ == "__main__":
    #test = {'season' : seasonList[0], 'mnth' : 5, 'hr': 18, 'workingday' : "True", "weathersit":weatherList[0], 'temp':0.4, 'hum':0.4, 'windspeed' : 0.5, 'id' : 0}
    print(model.predict([[0.070947,1.525049,-1.692812,0.314403,-1.440639]]))
    print('OK')