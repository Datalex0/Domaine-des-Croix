import streamlit as st
import pandas as pd
import bz2
import pickle
import _pickle as cPickle
import plotly_express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Analyse Comparative",
                   page_icon=":wine_glass:",
                   layout='wide')

# Fonction titre centré
def centered_text(text):
    st.markdown(f"<h1 style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)
centered_text("Analyse du Marché du Vin")

# Import Dataframe
def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data
df_vins = decompress_pickle('SRC/df_vins.pbz2')
# df_vins.dropna(subset=['year'], inplace=True)
# st.write(df_vins['year'].isna().any())

# Boutons Radio choix Zoom
zoom = st.sidebar.radio(
    "Choisissez un niveau de zoom :",
    ('France entière', 'Bourgogne', 'Pinots Noirs de Bourgogne'))

# Coordonnées du centre de la France
latitude_fr = 46.603354
longitude_fr = 1.888334
zoom_fr = 6

# Coordonnées du centre de la Bourgogne
latitude_bg = 47.316667
longitude_bg = 5.016667
zoom_bg = 8

if zoom == 'France entière':
    latitude=latitude_fr
    longitude=longitude_fr
    zoom_start=zoom_fr
    df=df_vins
elif zoom == 'Bourgogne' :
    latitude=latitude_bg
    longitude=longitude_bg
    zoom_start=zoom_bg
    df=df_vins[
        df_vins['province']=='Burgundy'
    ]
else :
    latitude=latitude_bg
    longitude=longitude_bg
    zoom_start=zoom_bg
    df=df_vins[
        (df_vins['province']=='Burgundy') & (df_vins['variety']=='Pinot Noir')
    ]


# Double Curseur Millésime
min_annee, max_annee = st.sidebar.slider(
"Sélectionnez les millésimes à étudier",
min_value = 1900,
max_value = 2023,
value = (1900,2023)
)

df = df[
    (df['year']<=max_annee) & (df['year']>=min_annee)
]



# Création de la carte
m = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)



html=f"""
    <h3 align=center>Analyse des vins du marché : </h3>
    <p></p>
    <ul>
        <li>Nombre de vins : {len(df)}</li>
        <br>
        <li>Note Moyenne : {round(df['points'].mean(),1)}</li>
        <br>
        <li>Note Domaine des Croix 2016 Corton Grèves : 94</li>
        <br>
        <li>Année Moyenne : {round(df['year'].mean())}</li>
        <br>
        <li>Année Domaine des Croix 2016 Corton Grèves : 2016</li>
        <br>
        <li>Prix Maximum : {round(df['price'].max(),1)}</li>
        <br>
        <li>Prix Moyen : {round(df['price'].mean(),1)}</li>
        <br>
        <li>Prix Minimum : {round(df['price'].min(),1)}</li>
        <br>
    </ul>
    </p>  
    """
iframe = folium.IFrame(html=html, width=300, height=420)
popup = folium.Popup(iframe, max_width=2650)

folium.Marker(location=[latitude, longitude],
  popup=popup,
  icon=folium.Icon(color="white", icon_color="red", icon="wine-bottle", prefix="fa")    
  ).add_to(m)

# Taille de la map + zoom
st_data = st_folium(m, width=1000)
