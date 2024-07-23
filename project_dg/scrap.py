import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import streamlit as st
import plotly.express as px


API_KEY = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={1c9e7651c6b2f39dc9b4daaa11e2d2a7}"
BASE_URL = "http://api.openweathermap.org/data/2.5"
st.title("Weather App")
st.image(("https://images.theconversation.com/files/442675/original/file-20220126-17-1i0g402.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1356&h=668&fit=crop"))
st.header("Select a Location:")
locations = ["New York", "India", "Paris", "Tokyo", "France"]
selected_location = st.selectbox("Location", locations)
def get_weather_data(location):
    para = {
        "q": location,
        "units": "metric",
        "apiid": API_KEY
    }
    response = requests.get(f"{BASE_URL}/weather", para=para)
    data = response.json()
    return data

def get_forecast_data(location):
    para={
        "q":location,
        "unnits":metric,
        "apiid":API_KEY
    }
    response = requests.get(f"{BASE_URL}/forecast", para=para)
    data = response.json()
    return data

st.header("check the current weather")


weather_data = get_weather_data(selected_location)


# para = {"q": location, "units": "metric", "appid": API_KEY}
# response = requests.get(f"{BASE_URL}/weather", para=para)