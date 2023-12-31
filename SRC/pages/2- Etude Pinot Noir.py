import streamlit as st
import pandas as pd
import bz2
import pickle
import _pickle as cPickle
import plotly_express as px

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Etude Pinot Noir",
                   page_icon=":wine_glass:",
                   layout='wide')

# Titre centré
st.markdown(f"<h1 style='text-align: center;'>Analyse du marché des Vins de cépage Pinot Noir</h1>", unsafe_allow_html=True)

# Import Dataframe
def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data
df_vins = decompress_pickle('SRC/df_vins.pbz2')

df_pn = df_vins[
    df_vins['variety']=='Pinot Noir'
]

# Diviser l'espace d'affichage en 2 colonnes
col1, col2 = st.columns(2)


# Afficher le premier graphique dans la première colonne
with col1:
    counts = df_pn['country'].value_counts().head(10)
    #counts = counts.reindex(counts.index[::-1])
    fig = px.bar(df_pn, y=counts.index, x=counts.values, color=counts.index, title='Nombre de Pinot Noir différents par Pays', width=600, height=600)
    # Mise à jour des libellés des axes
    fig.update_layout(yaxis_title='Pays', xaxis_title='Nombre de vins')
    # Mise à jour du titre
    fig.update_layout(title_font=dict(size=16))
    # Mise à jour de la légende
    fig.update_layout(legend_title='Pays')
    fig.update_layout(legend=dict(font=dict(size=16)))
    # Affichage du nombre dans les barres
    fig.update_traces(texttemplate='%{x}', textposition='auto')
    # Afficher le graphique
    st.plotly_chart(fig)

# Afficher le deuxième graphique dans la deuxième colonne
with col2:
    fig2 = px.pie(df_pn, values=counts.values*100/counts.values.sum(), names=counts.index, title='Pourcentage que représente chaque pays dans la répartition des Pinot Noir', hover_name=counts.index, width=600, height=600, hole=0.5)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_traces(pull=[0.2, 0, 0, 0, 0, 0])
    fig2.update_layout(title_font=dict(size=16))
    fig2.update_layout(legend=dict(font=dict(size=16)))
    # Mise à jour du titre de la légende
    fig2.update_layout(legend_title='Pays')
    st.plotly_chart(fig2)


# Ligne de séparation
st.write("***")


col3, col4 = st.columns(2)

with col3:
    mean_points = df_pn.groupby('country')['points'].mean().sort_values(ascending=False).head(10)
    mean_points = mean_points.reindex(mean_points.index[::-1])
    fig3 = px.bar(df_pn, y=mean_points.index, x=mean_points.values, color=mean_points.index, title='Top 10 des Pays ayant les Pinot Noir les mieux Notés', width=600, height=600)
    # Mise à jour des libellés des axes
    fig3.update_layout(yaxis_title='Pays', xaxis_title='Note moyenne')
    # Mise à jour du titre de la légende
    fig3.update_layout(legend_title='Pays')
    # Affichage du nombre dans les barres
    fig3.update_traces(texttemplate='%{x:.2f}', textposition='auto')
    st.plotly_chart(fig3)

with col4:
    mean_points = df_pn['year'].value_counts()
    fig4 = px.bar(df_pn, x=mean_points.index, y=mean_points.values, color=mean_points.values, title='Répartition des Millésimes de Pinot Noir', width=700, height=600)
    # Mise à jour des libellés des axes
    fig4.update_layout(xaxis_title='Millésimes', yaxis_title='Volume de Vins')
    # Supprimer la légende
    fig4.update_layout(showlegend=False)
    # Affichage du nombre dans les barres
    fig4.update_traces(texttemplate='%{y:.0f}', textposition='auto')
    st.plotly_chart(fig4)



# Ligne de séparation
st.write("***")



dico_mean = {'Moyenne des notes : ':round(df_pn['points'].mean(),2), 'Moyenne des prix : ':round(df_pn['price'].mean(),2)}
col_7, col_8 = st.columns(2)
col_7.metric(label='Moyenne des notes', value=round(df_pn['points'].mean(),2))
col_8.metric(label='Moyenne des prix', value=f"${round(df_pn['price'].mean(),2)}")


# Ligne de séparation
st.write("***")



col5, col6 = st.columns(2)


with col5:
    fig5 = px.box(df_pn, y=['points'], width=600)
    # Mise à jour des libellés des axes
    fig5.update_layout(xaxis_title='Pinot Noir', yaxis_title='Notes')
    # Mise à jour du titre de la légende
    fig5.update_layout(title='Répartition des Notes pour le Pinot Noir')
    st.plotly_chart(fig5)
    

with col6:
    fig6 = px.box(df_pn, y=['price'], range_y=[0,100], width=600)
    # Mise à jour des libellés des axes
    fig6.update_layout(xaxis_title='Pinot Noir', yaxis_title='Prix ($)')
    # Mise à jour du titre de la légende
    fig6.update_layout(title='Répartition des Prix pour le Pinot Noir (< $100)')
    st.plotly_chart(fig6)
