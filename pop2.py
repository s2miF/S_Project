#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 07:55:01 2024

@author: SamiFahad
"""

import numpy as np
import pandas as pd 
import pickle as pi
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
import openpyxl
import s2m
from s2m import main
import requests
import time

st.set_page_config(
   page_title="SAJ Project",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

#---------include the model predict start
lm = pi.load(open('dtr_pkl', 'rb'))
#---------include the model predict end


#------include the dataset start
df = pd.read_excel('pop.xlsx')
#------include the dataset end


#---------use GroupBy To prepare visualization start
grouped_data = df.groupby(['Year','Gender'])['Population'].sum().reset_index()
groupe_data = df.groupby(['Year','Region'])['Population'].sum().reset_index()
#--------use GroupBy To prepare visualization end

#-------------- side bar start
st.sidebar.image('sloogo.png', use_column_width=True)
st.sidebar.header("هل تريد التنبؤ أم تحليل البيانات")
ch = st.sidebar.selectbox("إختر من القائمة المنسدلة", ("الصفحة الرئيسية","تنبؤ" , "رسم بياني","معرفة الطقس")) # choice from two op
#------------- side bar end


#-------select box start!
#------- if user select predictaiton the population 
if ch == "تنبؤ":
    st.title("عدد السكان في المملكة العربية السعودية")
    
    main()
#------ if the user unselect 
if ch == "الصفحة الرئيسية":
        progress_text = "يتم تحميل الصفحة ليتم عرض البيانات التي تريدها :sunglasses:"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        st.balloons()
        long_text = "مرحباً بك في مشروع معسكر علوم البيانات لتحليل وتنبوء عدد سكان المملكة العربية السعودية والطقس :balloon: " 

        with st.container(height=50):
            st.markdown(long_text)
        st.warning("الرجاء الإختيار من القائمة المنسدلة البيانات المراد عرضها")
if ch == "معرفة الطقس":
        st.warning("التنبؤ بالطقس")
        
        API_KEY = "03bc4b3fbc4efe09a0cde4eeeba23e89"


        def get_data(place, forecast_days=None):
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            filtered_data = data["list"]
            nr_values = 8 * forecast_days
            filtered_data = filtered_data[:nr_values]
            return filtered_data

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

# if user select the visual
if ch == "رسم بياني":
    
    choice = st.selectbox("اختر الرسم المراد",("None","line chart","bar chart","scatter chart"))
    if choice == "None":
        st.warning("إختر من القائمة المنسدلة الرسم المراد")
    if choice == "line chart":
        st.info("المعروض أدناه الرسم الخطي الذي يبين عدد السكان على مر السنين")
        figure = px.line(x=grouped_data['Year'], y=grouped_data['Population'],
                     labels={"x": "years", "y": "population"},color=(grouped_data['Gender']),
                     width=(1000),height=(500))
        st.plotly_chart(figure)
    if choice == "bar chart":
        st.info("المعروض أدناه الرسم الخطي الذي يبين عدد السكان على مر السنين")
        figure = px.bar(x=groupe_data['Region'], y=groupe_data['Population'],
                     labels={"x": "Region", "y": "population"},color=(groupe_data['Year'])
                     ,hover_name=(groupe_data['Year']),width=(1000),height=(500),
                     color_continuous_scale=(px.colors.sequential.Viridis))
        st.plotly_chart(figure)
    if choice == "scatter chart":
        st.info("المعروض أدناه الرسم الخطي الذي يبين عدد السكان على مر السنين")
        figure = px.scatter(x=groupe_data['Region'], y=groupe_data['Population'],
                     labels={"x": "Region", "y": "population"},color=(groupe_data['Year'])
                     ,hover_name=(groupe_data['Year']),width=(1000),height=(500),
                     color_continuous_scale=(px.colors.sequential.Viridis))
        st.plotly_chart(figure)
        
    
