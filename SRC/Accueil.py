import streamlit as st
import pandas as pd
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Accueil",
                   page_icon=":wine_glass:",
                   layout='wide')

#Importation image accueil
#image = Image.open('C:/Users/murai/OneDrive/Bureau/DATA/Datathon2/Logo_Emmaüs_Connect.png')
#st.image(image)

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
    <h3 style="font-size: 24px; color: #8F260F;">Rappel du contexte :</h3>
</div>
        <br>
    <ul>
    <div style="background-color: rgba(400, 400, 400, 0.7); padding: 10px;">
    <p style="color: #8F260F;"><b>
        Vous êtes un vigneron situé dans la région de Bourgogne 
        <br>
        et produisant le Domaine des Croix 2016 Corton Grèves, un vin de cépage Pinot Noir.
        <br>
        <br>
        Vous souhaitez vous installer sur le marché américain,
        <br>
        Vous m'avez pour cela mandaté afin de vous aider à définir un tarif pour vos bouteilles
        <br>afin d'être compétitif sur ce nouveau marché.
        <br>
        <br>
        Pour cela, je vais vous présenter les éléments suivants :
        <br>
        - Une étude de marché générale
        <br>
        - Une étude du marché des Pinots Noirs
        <br>
        - Une étude des descriptions réalisées par les oenologues
        <br>
        - Une analyse comparative des vins à plusieurs niveaux
        <br>
        - Une proposition de tarif
        <br></b></p>
    </div></p></ul>
    
    """, unsafe_allow_html=True)