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
st.set_page_config(page_title="Proposition de Tarif",
                   page_icon=":wine_glass:",
                   layout='wide')

# Titre centré
st.markdown(f"<h1 style='text-align: center;'>Proposition de valeur</h1>", unsafe_allow_html=True)

# Import du Dataframe
def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data
df_pn = decompress_pickle('df_pn.pbz2')

# Explication du principe
st.title("Principe :")
st.write("Etude du marché des vins aux Etats-Unis en fonction de la Note du Vin, de son Millésime, de son Pays de Production et de son Cépage,")
st.write("Suppression des vins dont le prix n'était pas indiqué et qui n'étaient donc pas pertinents pour notre étude,")
st.write("Il restait au final 110.160 Vins à étudier.")

# Ligne de séparation
st.write("***")

# Scores
st.title("Scores du modèle :")
col_1, col_2 = st.columns(2)
col_1.metric(label="Score de l'ensemble d'entraînement", value='0.72')
col_2.metric(label="Score de l'ensemble de test", value='0.69')
st.write("Cela signifie que la probabilité de prévoir le juste tarif est de 69%")

# Ligne de séparation
st.write("***")

st.title("Prix prédit par l'algorithme : $58.08")

# Ligne de séparation
st.write("***")

col_3, col_4 = st.columns(2)
col_3.metric(label='Moyenne de prix des Vins', value='$36.39')
col_4.metric(label='Moyenne de prix des Vins bourguignons de cépage Pinot Noir', value='$72.26')

col_5, col_6 = st.columns(2)
col_5.metric(label='Moyenne de prix des Vins sans ceux de prix abérrant (+73.5)', value='$30.75')
col_6.metric(label='Moyenne de prix des Vins bourguignons de cépage Pinot Noir sans ceux de prix abérrant (+146.5)', value='$53.53')





# Ligne de séparation
st.write("***")

st.title('Prix des Vins aux Etats-Unis en fonction de leur Note')

col_7, col_8 = st.columns(2)
with col_7 :
    image = Image.open('C:/Users/murai/OneDrive/Bureau/DATA/CERTIF/Lineplot prix Vins.png')
    st.image(image)
    
with col_8 :
    image = Image.open('C:/Users/murai/OneDrive/Bureau/DATA/CERTIF/Lineplot prix PN BG.png')
    st.image(image)


# Ligne de séparation
st.write("***")

st.title('En conclusion :')
st.write('Au regard de la Note du Domaine des Croix 2016 Corton Grèves (94/100),')
st.write('il est tout à fait possible de se positionner sur le segment des vins Haut de Gamme,')
st.write('auquel cas il faudrait prévoir de fixer le tarif autour des $80.')
st.write('Dans le cas contraire, toujours au regard de la note, fixer le prix entre $55 et $60 serait une fourchette raisonnable.')