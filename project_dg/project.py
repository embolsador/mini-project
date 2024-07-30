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


@st.cache_data
def load_data():
    df = pd.read_csv("weather_data.csv")
    df.drop_duplicates(subset=['Location'])
    df.dropna(subset=['Location'])
    cols_to_rename ={'Location': 'LOCATION','Temperature_C':'TEMPERATURE', 'Humidity_pct':'HUMIDITY', 'Wind_Speed_kmh':'WIND TEMPERATURE'}
    df = df.rename(columns=cols_to_rename)
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
    df = df.set_index('LOCATION')
    # df['total'] = df[location].sum(axis=1)
    # df.head()
    return df
    
def get_weather(city):
    api_key = "1c9e7651c6b2f39dc9b4daaa11e2d2a7"
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
st.subheader("Weather Data Analysis")
st.write("This is a simple weather data analysis that uses the data from the [Weather Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data) dataset from Kaggle.")
st.write("This allows you to explore the data and visualize the trends in temperature, humidity,and wind speed over time.")
st.write("You can also use the app to compare the weather data for different locations and see how the weather conditions vary across different regions.")

# description of weather analysis

c1, c2,c3  = st.columns([2,2,2])
with c1:
    st.write("Select the location you want to explore:")
    location = st.selectbox("Location", df.index.unique())
with c2:
    st.write("Select the parameter you want to visualize:")
    parameter = st.selectbox("Parameter", ['TEMPERATURE','HUMIDITY',])
with c3:
    st.write("Select the time period you want to visualize:")
    start_date = st.date_input("Start Date", value=pd.to_datetime('2010-01-01').date())
    end_date = st.date_input("End Date", value=pd.to_datetime('2020-12-31').date())

# c1.subheader("Top 10 cities")
# top_10 = df.head(10)['TEMPERATURE']
# c1.dataframe(top_10,use_container_width=True)
city_df = df[df.index==location]
st.write(city_df.columns.tolist())
cdf = city_df.set_index('Date_Time').resample('D')[parameter].mean()
fig = px.box(cdf, y=parameter)
c1.plotly_chart(fig)

c2.subheader("Top 10 cities")
top_10 = df.head(10)['HUMIDITY']
c2.dataframe(top_10,use_container_width=True)

c3.write("Here we can clearly see that the temperature and the humidity in the last 5 months of the year 2024 as per the data, this data is according to the different time and dateThe temperature is increasing and the humidity is decreasing, this is due to the climate change and the global warming, this is a very serious issue and we need to take action to stop this issue, we need to take action to stop this issue, we need to take action to stop this issue, we need to take action to stop this issue, we need to take action ")


# creating a histogram for high temperature
st.subheader("Temperature  analysis")
st.write("This is a area graph of the weather data for the selected location and time period.")
st.write("The area shows the distribution of the temperature data and allows you to see the trends and patterns in the data over time.")
st.write("You can use the area graph to compare the temperature, humidity etc. data for different locations and see how the weather conditions vary across different regions.")

# st.plotly_chart(fig,use_container_width=True)
st.write(df)

# selesct column for the histogram graqph
hist_column = st.selectbox("Select a column for histogram", df.columns)

fig, ax = plt.subplots()
df[hist_column].hist(ax=ax, bins=10)
ax.set_title(f'Histogram of {hist_column}')
ax.set_xlabel(hist_column)
ax.set_ylabel('Frequency')
st.pyplot(fig)




