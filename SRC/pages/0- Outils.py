import streamlit as st
import pandas as pd
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Accueil",
                   page_icon=":wine_glass:",
                   layout='wide')

# Initialisation du fond d'écran
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('pages/fond ecran.jpg')

 
# Titre centré
st.markdown(f"<h1 style='text-align: center;'>Domaine des Croix</h1>", unsafe_allow_html=True) 
    
st.markdown(f"""
<div style="background-color: rgba(400, 400, 400, 0.7); padding: 10px;">
    <h3 style="font-size: 24px; color: #8F260F;">Les Outils utilisés : </h3>
</div>
        <br>
    <ul>
    <div style="background-color: rgba(400, 400, 400, 0.7); padding: 10px;">
    <p style="color: #8F260F;"><b>
        <br>
        - Visual Studio Code pour le code
        <br>
        - Langage Python
        <br>
        - Streamlit comme outil de présentation
        <br>
        - Plotly Express, Matplotlib et Seaborn pour les visualisations
        <br>
        - Folium pour générer une carte
        <br>
        - NLTK pour l'analyse des descriptions
        <br>
        - Scikit-Learn pour la proposition de valeur
        <br></b></p>
    </div></p></ul>
    
    """, unsafe_allow_html=True)
