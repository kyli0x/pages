#!/usr/bin/python3
import sys
import io
import requests
import json
import folium
from folium import plugins
import pandas as pd

# loading map & setting default start location
m = folium.Map(
    location=[33.988502832268956, 118.4693287776317],
    show=True,
    control_scale=True,
    prefer_canvas=False,
    disable_3d=True,
    crs='EPSG3857',
    max_bounds=True,
    min_zoom=3,
    max_zoom=18,
    zoom_start=6,
)

# set bounderies of map panning
m.fit_bounds([[33.98813901349684, -118.46677927707837], [0, -1.0]])

folium.TileLayer(
    tiles='OpenStreetMap',
).add_to(m)

# add extra layers - satellite view
folium.TileLayer( 
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri.WorldImagery',
    control_scale=True,
    prefer_canvas=True,
    disable_3d=True,
    crs='EPSG3857',
    max_bounds=True,
    min_zoom=3,
    max_zoom=18
).add_to(m)

# layer control settings
folium.LayerControl(
    position='topright',
    collapsed=True
).add_to(m)

# add popup lat/lng when clicking on map
m.add_child(folium.LatLngPopup())

# global tooltip
tooltip = 'Click for more info'

# custom marker icons
imgurl = 'https://raw.githubusercontent.com/kyli0x/skatemaps/main/logo.png'
logoIcon = folium.features.CustomIcon(imgurl, icon_size=(30, 30)) 

# default markers
popup9club = 'The Nine Club<br>313 Grand Blvd<br>PO Box 225<br>Venice, CA 90294<br>https://www.thenineclub.com'
folium.Marker([33.988502832268956, -118.4693287776317],
                popup=popup9club, parse_html=True,
                tooltip='The Nine Club',
                icon=logoIcon
                ).add_to(m)

# read saved places data
savedplaces = pd.read_csv('savedplaces.csv', usecols=['lat', 'lon', 'Address', 'PlaceName'])

# add a marker for each saved place
for i in range(0,len(savedplaces)):
    folium.Marker(
        location=[savedplaces.iloc[i]['lat'], savedplaces.iloc[i]['lon']],
        popup=savedplaces.iloc[i]['Address'],
        icon=folium.Icon(color='blue', icon='info-sign'),
        tooltip=savedplaces.iloc[i]['PlaceName']
    ).add_to(m)

# save map data to data object
data = io.BytesIO()
m.save(data, close_file=False)
m.save('skatemaps.html')
