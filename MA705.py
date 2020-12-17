from urllib.request import urlopen
import numpy as np
import streamlit as st
import json
# import datetime
import altair as alt
import plotly.express as px
import pandas as pd
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


st.title("MA705 Project - Sandhat Bylapudi")
datafile = "Covid14Dec.csv"                      #Primary dataset file 
df = pd.read_csv(datafile)
df['casrn'] = df['casrn'].apply(lambda x: str(x).zfill(5))
df = df.fillna(0)
# st.map(df)

first = st.radio("Select Data for Map", ("Number of Cases", "Number of Deaths"))
if first == "Number of Cases":
    fig = px.choropleth_mapbox(df, geojson=counties, locations='casrn', color='Cases',
                               color_continuous_scale="thermal",
                               range_color=(0, 512872),
                               mapbox_style="carto-positron",
                               zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5,
                               labels={'Cases':'Number of Cases'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.choropleth_mapbox(df, geojson=counties, locations='casrn', color='Deaths',
                               color_continuous_scale="thermal",
                               range_color=(0, 8269),
                               mapbox_style="carto-positron",
                               zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5,
                               labels={'Deaths':'Number of Deaths'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

df['lon'] = df['sid'].str.split(',').str.get(0).astype(float)
df['lat'] = df['sid'].str.split(',').str.get(-1).astype(float)
df['countyname'] = df['name'].str.split(',').str.get(-1)
df['name']= df['name'].str.split(',').str.get(0)
state = st.selectbox('Select state', df['name'].unique())
df= df.loc[df['name'] == state].reset_index()

county = st.selectbox('Select county', df['countyname'].unique())
df= df.loc[df['countyname'] == county].reset_index()
fip = df['casrn'][0]
fip = int(fip)
fipst = str(fip)
# st.dataframe(df)
if st.checkbox("Show Graphs"):
    second = st.radio("Select Data for Graphs", ("Number of Cases", "Number of Deaths"))
    deathdf = pd.read_csv('deathsnew2.csv')
    casesdf = pd.read_csv('casesnew2.csv')
    newdf = pd.DataFrame(data=deathdf,columns=[fipst, 'Date'])
    newdf.columns.values[0] = 'Deaths'
    cnewdf = pd.DataFrame(data=casesdf,columns=[fipst, 'Date'])
    cnewdf.columns.values[0] = 'Cases'
    if second == "Number of Cases":
     
        st.title(f"Number of cases in {county}, {state}")
        base2 = alt.Chart(cnewdf).mark_line(point=True).encode(
            x = alt.X('Date:T'),
            y='Cases:Q'
        ).properties(
            width=600,
            height=400
        )
        
        st.write(base2)
    else:
        st.title(f"Number of Deaths in {county}, {state}")
        base = alt.Chart(newdf).mark_line(point=False).encode(
            x = alt.X('Date:T'),
            y='Deaths:Q'
        ).properties(
            width=600,
            height=400
        )
        
        st.write(base)

