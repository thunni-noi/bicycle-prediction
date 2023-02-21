import streamlit as st
from shapely.geometry import Point,Polygon
import geopandas as gpd
import pandas as pd
from weather_api import get_weather
from datetime import datetime, time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from run_model import start_predict
import pathlib
import base64

if st.secrets['current_platform'] != "pc" :
    pathlib.WindowsPath = pathlib.PosixPath

cur_month = datetime.now().month
cur_hr = cur_hr = (int(datetime.now().hour)+ 8) % 24 #utc+8

geolocator = Nominatim(user_agent='thunninoi')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

#init
if 'weather' not in st.session_state: st.session_state['weather'] = ""
if 'prediction' not in st.session_state: st.session_state['prediction'] = ""
if 'customMode' not in st.session_state: st.session_state['customMode'] = ""
workingday = False

st.set_page_config(
    page_title="Bicycle prediction",
    page_icon='https://s3-ap-northeast-1.amazonaws.com/killy-image/linestamp/1f/1f13/1f131746571cc91986f8b868ed2946789402c741',
    layout='wide',
    menu_items={
        'Report a bug' : 'https://github.com/thunni-noi/bicycle-prediction/issues',
        'About' : 'https://github.com/thunni-noi/bicycle-prediction'
    }
)


def clearPrediction() :
    st.session_state['prediction'] = ""
    
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    #print(base64_pdf)
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1080" height="720" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
#st.write(st.session_state['weather'])
st.title('#Bicycle usage prediction model!')
st.subheader('Summary')
st.write("Web App นี้เกิดจากการนำ dataset บน kaggle มาทำเป็น decision tree model มีความแม่นยำอยู่ที่ 70% เรามีความตั้งใจที่จะนำ model ตัวนี้มาใช้ทำนายจำนวนคนที่จะใช้งานระบบเช่าจักรยาน โดยมีตัวแปรเป็น สถานที่ และสภาพอากาศต่างๆ เราได้ดึงข้อมูลสภาพอากาศต่างๆ มาจาก API ของ OpenWeather โดยมีเป้าหมายเพื่อที่จะทำนายปริมาณคนที่จะใช้งานจักรยานในพื้นที่ๆนั้นเพื่อที่จะได้วางแผนล่วงหน้าเพื่อโอกาสมากที่สุดที่สามารถทำกำไรได้")
st.write('ข้อมูลโดยละเอียดสามารถอ่านได้บน[รายงาน](https://github.com/thunni-noi/bicycle-prediction/blob/main/slideshow/Bicycle-prediction-report.pdf)')
st.subheader("วิธีการใช้งาน:")
st.write("  1. เลือกวิธีในการรับข้อมูลมาประมวลผล หากต้องการเรียกข้อมูลอัตโนมัติให้เลือกสถานที่ผ่านช่อง 'Location' แล้วกด 'Fetch weather data' หากต้องการจะกรอกข้อมูลเองให้กดที่ช่อง 'Enable custom parameter'")
st.write("  2. หากวันนั้นเป็นวันทำงานให้กดที่ช่อง 'Workingday'")
st.write("  3. กด 'Predict' เพื่อเริ่มทำนาย")

if st.secrets['current_platform'] == 'pc' :
    show_pdf('slideshow/slideshow-compressed.pdf') 
else:
    slideshow_vdo = open("slideshow/slideshow.mp4", 'rb')
    st.write('Presentation Video :')
    st.video(slideshow_vdo.read())
#st.image('https://media.discordapp.net/attachments/540130478653702154/1076875909564473385/Michaelpatakos_greecebicycleseacalmfancypop_artvector_7023ffdf-6ae1-4499-9809-9513323c8c39.png?width=678&height=678')

st.header('Welcome to bicycle usage prediction website!')
st.subheader('Project by  ')
st.subheader(' > Jittaraboon Sapsintweelap No.23')
st.subheader(' > Tanapon Thongchamnong No.39')
                
st.markdown('Data is pulled from [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)')
st.markdown('Source code is available at [GitHub](https://github.com/thunni-noi/bicycle-prediction)')
st.session_state['customMode'] = st.sidebar.checkbox('Enable custom parameter?', value= False, on_change= clearPrediction())
if not st.session_state['customMode']:
    location_input = st.sidebar.text_input('Location (Input location name or coordinate)', "มหาวิทยาลัยศรีนครินทรวิโรฒ ประสานมิตร")
    if (len(location_input.split(',')) == 2): st.sidebar.text('Format : Coordinate')
    else : st.sidebar.text('Format : Location Name')

    location = geolocator.geocode(location_input)
    try :
        lat = location.latitude
        lon = location.longitude
        map_data = pd.DataFrame({'lat' : [lat], 'lon': [lon]})
        location_valid = True
    except AttributeError: 
        location_valid = False
        st.error("No location found! \n If you're trying to use coordinate pls use format 'latitude, longitude'")
        map_data = pd.DataFrame({'lat' : [0], 'lon': [0]})



    if location_valid or st.session_state['weather'] != "":
        sidecol1, sidecol2 = st.sidebar.columns([3, 5])
        fetchweatherlabel = "Fetch weather data "
        if st.session_state['weather'] != "" : fetchweatherlabel = "Refresh weather data "
        if sidecol1.button(fetchweatherlabel) or st.session_state['weather'] != "":
            
            col1, col2, col3 = st.sidebar.columns(3)
            weatherData = get_weather(lat, lon)
            #session state
            st.session_state['weather'] = weatherData
            if sidecol2.button('Predict'):
                predicted = start_predict(weatherData, cur_month, cur_hr, workingday)
                st.session_state['prediction'] = predicted
            
            #st.sidebar.write(f'Weather status : {weatherData["weathersit"]}')
            col1.metric("Temperature", f"{weatherData['temp']}°C")
            
            col2.metric("Wind (Meters per hour)", f"{weatherData['windspeed']}mph")
            
            col3.metric("Humidity", f"{weatherData['hum']}%")
            col2.text(f'Hour : {cur_hr}')
            col1.text(f'Month : {cur_month}')
            w1, w2 = st.sidebar.columns([1,3])
            w1.metric("Weather status", weatherData['weathersit'])
            image_url = f"http://openweathermap.org/img/wn/{weatherData['icon']}@2x.png"
            w2.image(image_url)
            workingday = col3.checkbox('Workingday?' ,value = False,)
        if st.session_state['prediction'] != "":
            st.sidebar.metric("Prediction", st.session_state['prediction']['prediction(cluster)'])
            
            
        

    st.map(map_data)
else:
    weathersit = st.sidebar.selectbox('Weather status ', ['Clear','Cloudy','Rain','Heavy Rain'])
    temperature = st.sidebar.number_input('Temperature (°C)', -50, 99,28)
    humidity = st.sidebar.number_input('Humidity (%)', 0, 100,50)
    wind_speed = st.sidebar.number_input('Wind Speed (meter per hour)', -50, 99,28)
    time = st.sidebar.time_input('Time (Nearest)')
    date = st.sidebar.date_input('Date')
    workingday = st.sidebar.checkbox('workingday?', False)
    weatherData = {'weathersit':weathersit, 'temp':temperature,'hum':humidity,'windspeed':wind_speed}
    sel_month = date.month
    sel_hr = time.hour
    #st.sidebar.columns(3)
    if st.sidebar.button('Predict'):
                predicted = start_predict(weatherData, sel_month, sel_hr, workingday)
                st.session_state['prediction'] = predicted
    print('OK')
    if st.session_state['prediction'] != "": st.sidebar.metric("Prediction", st.session_state['prediction']['prediction(cluster)'])
