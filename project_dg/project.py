import requests
import math
import json
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go



def load_data():
    df = pd.read_csv("weather_data.csv")
    df.drop_duplicates(subset=['Location'])
    df.dropna(subset=['Location'])
    cols_to_rename ={'Location': 'LOCATION','Precipitation_mm':'TEMPERATURE', 'Humidity_pct':'HUMIDITY', 'Wind_Speed_kmh':'WIND TEMPERATURE'}
    df = df.rename(columns=cols_to_rename)
    cols_to_drop = ['Date_Time']
    df = df.drop(columns=cols_to_drop)
    df = df.set_index('LOCATION')
    
    return df
def get_weather(city):
    api_key = "b3c62ae7f7ad5fc3cb0a7b56cb7cbda6"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
    
    try:
        data = json.loads(response.text)
        if data['cod'] != 200:
            print(f"Error: {data['message']}")
    except json.JSONDecodeError as err:
        print(f"Error: Failed to parse response JSON - {err}")
    except KeyError as err:
        print(f"Error: {err}")
        return data   
    

    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    
    # Convert temperature from Kelvin to Celsius
    temperature = round(temperature - 273.15, 2)
    
    # Print the weather forecast
    st.write(f"Weather in {city}: {weather_description}")
    st.write(f"Temperature: {temperature}°C")
    st.write(f"Humidity: {humidity}")
    st.write(f"Pressure: {pressure}")

# configure the layout
st.set_page_config(
    layout="wide",
    page_title ="Weather app",
    page_icon="🌡️",
)

st.header("CHECK THE CURRENT WEATHER")
# st.image("https://imgs.search.brave.com/Kul6Ev7J4xhHC22X35SnjP0y-Jrfjikogek-IZDWEkM/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTI2/MzU2MjM4Ni9waG90/by9iZWF1dGlmdWxs/eS1zdHJ1Y3R1cmVk/LXRodW5kZXJzdG9y/bS1pbi1idWxnYXJp/YW4tcGxhaW5zLmpw/Zz9zPTYxMng2MTIm/dz0wJms9MjAmYz1y/d2t3RzF1MGVXbE92/T3h5NUdSOG41eE5z/UXR6SS1LdXRuWnNR/eFRNM0VjPQ")
st.image("https://images.theconversation.com/files/442675/original/file-20220126-17-1i0g402.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1356&h=668&fit=crop")
city = st.text_input("Enter city name")
if st.button("Get Weather"):
    get_weather(city)



# loading the data
with st.spinner("Loading Data..."):
    df = load_data()
    st.sidebar.success("Data Loaded Successfully! 🎉")


# creating the ui interface
st.title("Weather Data Analysis")
st.write("This is a simple weather data analysis app that uses the data from the [Weather Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data) dataset from Kaggle.")
st.write("The app allows you to explore the data and visualize the trends in temperature, humidity,and wind speed over time.")
st.write("You can also use the app to compare the weather data for different locations and see how the weather conditions vary across different regions.")


c1, c2,c3  = st.columns([2,1,1])
with c1:
    st.write("Select the location you want to explore:")
    location = st.selectbox("Location", df.index)
with c2:
    st.write("Select the parameter you want to visualize:")
    parameter = st.selectbox("Parameter", df.columns)
with c3:
    st.write("Select the time period you want to visualize:")
    start_date = st.date_input("Start Date", value=pd.to_datetime('2010-01-01').date())
    end_date = st.date_input("End Date", value=pd.to_datetime('2020-12-31').date())

c1.header("Top 10 cities")
top_10 = df.head(10)['Temperature_C']
c1.dataframe(top_10,use_container_width=True)
figTopTen = px.bar(top_10, x=top_10.index, y='total')
                                                                    