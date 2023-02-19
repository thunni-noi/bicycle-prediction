from pypmml import Model
import pathlib

pathlib.WindowsPath = pathlib.PosixPath
model = Model.load('model\Decision70.pmml')
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
    test = {'season' : seasonList[0], 'mnth' : 5, 'hr': 18, 'workingday' : "True", "weathersit":weatherList[0], 'temp':0.4, 'hum':0.4, 'windspeed' : 0.5, 'id' : 0}
    prediction = model.predict(test)
    print(prediction['prediction(cluster)'])