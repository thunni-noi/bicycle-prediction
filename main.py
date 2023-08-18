import streamlit as st
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium
from folium.features import CustomIcon
from weather_api import get_weather
import time

st.set_page_config(
    page_title="Bicycle prediction",
    page_icon='https://s3-ap-northeast-1.amazonaws.com/killy-image/linestamp/1f/1f13/1f131746571cc91986f8b868ed2946789402c741',
    layout='wide',
    menu_items={
        'Report a bug' : 'https://github.com/thunni-noi/bicycle-prediction/issues',
        'About' : 'https://github.com/thunni-noi/bicycle-prediction'
    }
)

#?init
if 'location' not in st.session_state: st.session_state['location'] = None
    

@st.cache_data(experimental_allow_widgets=True)
def get_location_data():
    loc = get_geolocation()
    time.sleep(3)
    try :
        return loc['coords']['latitude'], loc['coords']['longitude']
    except:
        st.warning('Cannot fetch your gps data! ; Please enable gps then refresh the page.')
        st.button('Refresh GPS Data', on_click=get_location_data.clear)
        return [0, 0]
    
    
latitude, longitude = get_location_data()


st.title('AirWise')
st.header('Forecasting PM2.5 Prowess with WeatherWisdom')
#st.sidebar.button('Resel all', on_click=st.experimental_rerun)
st.caption(f'Your current latitude is {latitude} and longitude is {longitude}')
st.subheader('Pick your location to fetch the weather from.')

m = folium.Map(location=[latitude, longitude], zoom_start=16)
folium.Marker(
    [latitude, longitude],
    popup="Current Location",
    tooltip="Current Location",
    icon=folium.Icon(icon='diamond',icon_color='white', color='blue', prefix='fa')
).add_to(m)
m.add_child(folium.LatLngPopup())

f_map = st_folium(m, width=725)
    
if f_map.get("last_clicked"):
    selected_latitude = f_map['last_clicked']['lat']
    selected_longitude = f_map['last_clicked']['lng']
    
form = st.form("Position entry form")

submit = form.form_submit_button()

if submit:
    st.success(f"Stored position: {selected_latitude}, {selected_longitude}")
    st.write(get_weather(selected_latitude, selected_longitude))