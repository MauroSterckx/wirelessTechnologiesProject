import requests
import pandas as pd
import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static

# Titel van de Streamlit app
st.title('Interactieve Heatmap van TPMS Data')

# Data ophalen
url = 'https://wireless.maurosterckx.be/api/markers'
response = requests.get(url)
data = response.json()

# Data omzetten naar een DataFrame
df = pd.DataFrame(data)
df['pressure'] = df['tpms_data'].apply(lambda x: x['pressure'])
df['latitude'] = df['lat']
df['longitude'] = df['lng']

# Verwijder NaN waarden uit de DataFrame
df = df.dropna(subset=['latitude', 'longitude', 'pressure'])

# Kaart weergeven met Folium
m = folium.Map(location=[51.466, 4.470], zoom_start=13)
heat_data = [[row['latitude'], row['longitude'], row['pressure']] for index, row in df.iterrows() if not pd.isna(row['latitude']) and not pd.isna(row['longitude']) and not pd.isna(row['pressure'])]
HeatMap(heat_data).add_to(m)

# Folium kaart statisch weergeven in Streamlit
folium_static(m)

# Data tabel weergeven
st.dataframe(df)
