import streamlit as st
import plotly.express as px
#from backend import get_data

import requests

API_KEY = "03bc4b3fbc4efe09a0cde4eeeba23e89"


def get_data(place, forecast_days=None):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    nr_values = 8 * forecast_days
    filtered_data = filtered_data[:nr_values]
    return filtered_data

st.title("الطقس الأيام القادمة")
place = st.text_input("المكان ")
days = st.slider("عدد الأيام", min_value=1, max_value=12,
                 help="عدد الأيام القادمة التي تريدها لتوقع الطقس")
option = st.selectbox("المعيار",
                      ("درجة الحرارة", "السماء"))
st.subheader(f"الطقس الأيام  {days} القادمة في {place}")

if place:
    
    try:
        filtered_data = get_data(place, days)

        if option == "درجة الحرارة":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            
            figure = px.line(x=dates, y=temperatures, labels={"x": "الأيام", "y": "درجة الحرارة (C)"})
            st.plotly_chart(figure)

        if option == "السماء":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115, caption=dates)

    except KeyError:
        st.write("المكان المحدد غير صحيح")


