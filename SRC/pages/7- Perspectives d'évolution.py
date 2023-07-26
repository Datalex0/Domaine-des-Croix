import streamlit as st
import pandas as pd
import bz2
import pickle
import _pickle as cPickle
import plotly_express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as np

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Perspectives",
                   page_icon=":wine_glass:",
                   layout='wide')

# Titre centré
st.markdown(f"<h1 style='text-align: center;'>Perspectives d'évolution</h1>", unsafe_allow_html=True)


st.markdown(f"""
<div style="background-color: rgba(400, 400, 400, 0.7); padding: 10px;">
    <h3 style="font-size: 24px; color: #8F260F;">Perspectives d'Evolution :</h3>
</div>
        <br>
    <ul>
    <div style="background-color: rgba(400, 400, 400, 0.7); padding: 10px;">
    <p style="color: #8F260F;"><b>
         - Ajouter des filtres et des informations à la carte pour d'autres comparaisons,
        <br>
        <br>
         - Traduire les titres de colonnes et les données en français pour les rendre plus lisibles,
        <br>
        <br>
         - Pousser l'exploration, notamment via les colonnes 'région' pour prioriser la meilleure région dans laquelle démarrer l'implantation,
        <br>
        <br>
         - Améliorer l'efficacité de l'algorithme de prédiction de prix,
        <br>
        <br>
         - Retravailler certains Graphiques pour les rendre plus agréables à regarder.
    """, unsafe_allow_html=True)
