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
st.set_page_config(page_title="Etude des Descriptions",
                   page_icon=":wine_glass:",
                   layout='wide')


# Fonction titre centré
def centered_text(text):
    st.markdown(f"<h3 style='text-align: center;'>{text}</h3>", unsafe_allow_html=True)


centered_text("Wordcloud représentant les mots qui reviennent le plus")

# Diviser l'espace d'affichage en 2 colonnes
col1, col2, col3 = st.columns(3)


# Afficher le premier wordcloud dans la première colonne
with col1:
    centered_text("dans l'ensemble des données")
    centered_text("")
    with open("SRC/text.pkl", 'rb') as file:
        text = pickle.load(file)
    # Chargement de l'image bouteille pour créer un masque
    bottle_mask = np.array(Image.open("SRC/pages/bouteille.jpg"))
    # Création du Wordcloud
    wordcloud = WordCloud(width=100, height=100, max_font_size=200, min_font_size=10, mask=bottle_mask)
    # Génération du wordcloud depuis la liste
    wordcloud.generate_from_text(text)
    st.image(wordcloud.to_array(), use_column_width=False, width=200)

# Afficher le deuxième wordcloud dans la deuxième colonne
with col2:
    centered_text("uniquement pour les Pinots Noirs") 
    with open("SRC/text_pn.pkl", 'rb') as file:
        text_pn = pickle.load(file)
    # Chargement de l'image bouteille pour créer un masque
    bottle_mask = np.array(Image.open("SRC/pages/bouteille.jpg"))
    # Création du Wordcloud
    wordcloud = WordCloud(width=100, height=100, max_font_size=200, min_font_size=10, mask=bottle_mask)
    # Génération du wordcloud depuis la liste
    wordcloud.generate_from_text(text_pn)
    st.image(wordcloud.to_array(), use_column_width=False, width=200)
    
    
# Afficher le troisième wordcloud dans la troisième colonne
with col3:
    centered_text("uniquement pour les vins de Bourgogne") 
    with open("SRC/text_bg.pkl", 'rb') as file:
        text_bg = pickle.load(file)
    # Chargement de l'image bouteille pour créer un masque
    bottle_mask = np.array(Image.open("SRC/pages/bouteille.jpg"))
    # Création du Wordcloud
    wordcloud = WordCloud(width=100, height=100, max_font_size=200, min_font_size=10, mask=bottle_mask)
    # Génération du wordcloud depuis la liste
    wordcloud.generate_from_text(text_bg)
    st.image(wordcloud.to_array(), use_column_width=False, width=200)
