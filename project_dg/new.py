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
        
    # Extract relevant weather information
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

st.header("Check the current weather")
st.image("https://imgs.search.brave.com/Kul6Ev7J4xhHC22X35SnjP0y-Jrfjikogek-IZDWEkM/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTI2/MzU2MjM4Ni9waG90/by9iZWF1dGlmdWxs/eS1zdHJ1Y3R1cmVk/LXRodW5kZXJzdG9y/bS1pbi1idWxnYXJp/YW4tcGxhaW5zLmpw/Zz9zPTYxMng2MTIm/dz0wJms9MjAmYz1y/d2t3RzF1MGVXbE92/T3h5NUdSOG41eE5z/UXR6SS1LdXRuWnNR/eFRNM0VjPQ")
city = st.text_input("Enter city name")
if st.button("Get Weather"):
    get_weather(city)



# st.header("City wise visualization")
# c1, = st.column(1)
# c1.write("Select the city to see the visualization")
# city = c1.selectbox("Select the city",["London", "Paris", "Tokyo",
#                                         "New York", "Sydney", "Beijing", "Delhi", "Mumbai
#                                         "Kolkata", "Chennai", "Hyderabad", "Bangalore", "Ahmedabad",
#                                         "Kochi", "Pune", "Jaipur", "Lucknow", 
#                                         "Kanpur", "Nagpur", "Patna", "Indore",
#                                         "Bhopal", "Surat", "Pune", "Ludhiana",
#                                         "Agra", "Nashik", "Faridabad", "Meerut",
#                                         "Ranchi", "Kota", "Vadodara", "Ghaziabad",
#                                         "Gurgaon", "Kalyan", "Noida", "Amritsar",
#                                         "Varanasi", "Allahabad", "Coimbatore", "Jabal",
#                                         "Pimpri-Chinchwad", "Raipur", "Srinagar",
#                                         "Aurangabad", "Vijayawada", "Jodhpur",
#                                         "Madurai", "Thane", "Bhubaneswar", "Gwalior",
#                                         "Solapur", "Dehradun", "Kozhikode", "Dhan",
#                                         "Bareilly", "Aligarh", "Jalandhar", "Bhiw",
#                                         "Rajkot", "Warangal", "Guntur", "Nello",
#                                         "Bhilai", "Amravati", "Bikaner", "Jhansi",
#                                         "Gaya", "Jamshedpur", "Bhilwara", "Kollam"]
# )
# if st.button("Get Weather"):
#     get_weather(city)


                                        


