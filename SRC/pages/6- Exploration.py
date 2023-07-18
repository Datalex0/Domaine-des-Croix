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
st.markdown(f"<h1 style='text-align: center;'>Exploration</h1>", unsafe_allow_html=True)

# Import du Dataframe
link = "https://github.com/WildCodeSchool/wilddata/raw/main/wine_df.zip"
df = pd.read_csv(link)

df = df[['title', 'year', 'variety', 'country', 'province', 'points', 'price', 'description']]

# Double Curseur Millésime
min_annee, max_annee = st.sidebar.slider(
"Sélectionnez les millésimes à étudier",
min_value = 1900,
max_value = 2023,
value = (2000,2023)
)

# Double Curseur Note
min_note, max_note = st.sidebar.slider(
"Sélectionnez les notes à étudier",
min_value = 80,
max_value = 100,
value = (80,100)
)

# Double Curseur Prix
min_prix, max_prix = st.sidebar.slider(
"Sélectionnez les prix à étudier",
min_value = 2,
max_value = 1902,
value = (2,1902)
)

liste_pays=['Italy', 'Portugal', 'US', 'Spain', 'France', 'Germany',
       'Argentina', 'Chile', 'Australia', 'Austria', 'South Africa',
       'New Zealand', 'Israel', 'Hungary', 'Greece', 'Romania', 'Mexico',
       'Canada', 'Turkey', 'Czech Republic', 'Slovenia',
       'Luxembourg', 'Croatia', 'Georgia', 'Uruguay', 'England',
       'Lebanon', 'Serbia', 'Brazil', 'Moldova', 'Morocco', 'Peru',
       'India', 'Bulgaria', 'Cyprus', 'Armenia', 'Switzerland',
       'Bosnia and Herzegovina', 'Ukraine', 'Slovakia', 'Macedonia',
       'China', 'Egypt']
pays = st.sidebar.selectbox(
    'Pays', liste_pays, index=liste_pays.index('France')
)

liste_cepages=['White Blend', 'Portuguese Red', 'Pinot Gris', 'Riesling',
       'Pinot Noir', 'Tempranillo-Merlot', 'Frappato', 'Gewürztraminer',
       'Cabernet Sauvignon', 'Nerello Mascalese', 'Chardonnay', 'Malbec',
       'Tempranillo Blend', 'Meritage', 'Red Blend', 'Merlot',
       "Nero d'Avola", 'Chenin Blanc', 'Gamay', 'Sauvignon Blanc',
       'Viognier-Chardonnay', 'Primitivo', 'Catarratto', 'Inzolia',
       'Petit Verdot', 'Monica', 'Bordeaux-style White Blend', 'Grillo',
       'Sangiovese', 'Cabernet Franc', 'Champagne Blend',
       'Bordeaux-style Red Blend', 'Aglianico', 'Petite Sirah',
       'Touriga Nacional', 'Carmenère', 'Albariño', 'Petit Manseng',
       'Rosé', 'Zinfandel', 'Vernaccia', 'Rosato', 'Grüner Veltliner',
       'Viognier', 'Vermentino', 'Grenache Blanc', 'Syrah', 'Nebbiolo',
       'Shiraz-Cabernet Sauvignon', 'Pinot Blanc', 'Alsace white blend',
       'Barbera', 'Rhône-style Red Blend', 'Portuguese White', 'Graciano',
       'Tannat-Cabernet', 'Sauvignon', 'Sangiovese Grosso', 'Torrontés',
       'Prugnolo Gentile', 'G-S-M', 'Verdejo', 'Fumé Blanc', 'Furmint',
       'Pinot Bianco', 'Bonarda', 'Shiraz', 'Montepulciano', 'Moscato',
       'Grenache', 'Ugni Blanc-Colombard', 'Syrah-Viognier',
       'Blaufränkisch', 'Friulano', 'Assyrtico', 'Carignan-Grenache',
       'Sagrantino', 'Savagnin', 'Cabernet Sauvignon-Syrah', 'Prosecco',
       'Vignoles', 'Sparkling Blend', 'Muscat', 'Muscadelle',
       'Shiraz-Viognier', 'Garganega', 'Pinot Grigio', 'Tempranillo',
       'Zierfandler', 'Cortese', 'Mencía', 'Zweigelt', 'Melon',
       'Rhône-style White Blend', 'Vidal', 'Cannonau', 'Verdelho',
       'Marsanne', 'Scheurebe', 'Kerner', 'Syrah-Grenache', 'Dolcetto',
       'Vilana', 'Glera', 'Viura', 'Garnacha Tintorera', 'Pinot Nero',
       'Roter Veltliner', 'Pinotage', 'Sémillon', 'Pinot Noir-Gamay',
       'Antão Vaz', 'Cabernet Sauvignon-Carmenère', 'Verdejo-Viura',
       'Verduzzo', 'Verdicchio', 'Silvaner', 'Colombard', 'Carricante',
       'Sylvaner', 'Fiano', 'Früburgunder', 'Sousão', 'Roussanne',
       'Avesso', 'Cinsault', 'Chinuri', 'Tinta Miúda',
       'Muscat Blanc à Petits Grains', 'Portuguese Sparkling',
       'Monastrell', 'Xarel-lo', 'Greco', 'Trebbiano',
       'Corvina, Rondinella, Molinara', 'Port', 'Chenin Blanc-Chardonnay',
       'Insolia', 'Merlot-Malbec', 'Ribolla Gialla',
       'Cabernet Sauvignon-Merlot', 'Duras', 'Weissburgunder', 'Roditis',
       'Traminer', 'Papaskarasi', 'Tannat-Syrah', 'Marsanne-Roussanne',
       'Charbono', 'Merlot-Argaman', 'Prié Blanc', 'Sherry',
       'Provence red blend', 'Tannat', 'Zibibbo', 'Falanghina',
       'Garnacha', 'Negroamaro', 'Mourvèdre', 'Syrah-Cabernet',
       'Müller-Thurgau', 'Pinot Meunier', 'Cabernet Sauvignon-Sangiovese',
       'Austrian Red Blend', 'Teroldego', 'Pansa Blanca',
       'Muskat Ottonel', 'Sauvignon Blanc-Semillon', 'Claret',
       'Semillon-Sauvignon Blanc', 'Bical', 'Moscatel', 'Rosado',
       'Viura-Chardonnay', 'Baga', 'Malvasia Bianca',
       'Gelber Muskateller', 'Malbec-Merlot', 'Monastrell-Syrah',
       'Malbec-Tannat', 'Malbec-Cabernet Franc', 'Turbiana', 'Refosco',
       'Alvarinho', 'Manzoni', 'Aragonês', 'Agiorgitiko', 'Malagousia',
       'Assyrtiko', 'Ruché', 'Welschriesling', 'Tinta de Toro',
       'Cabernet Moravia', 'Rieslaner', 'Traminette', 'Chambourcin',
       'Nero di Troia', 'Lambrusco di Sorbara', 'Cesanese',
       'Feteasca Neagra', 'Lagrein', 'Tinta Fina', 'St. Laurent',
       'Marsanne-Viognier', 'Cabernet Sauvignon-Shiraz',
       'Syrah-Cabernet Sauvignon', 'Gewürztraminer-Riesling',
       'Pugnitello', 'Cerceal', 'Touriga Nacional Blend',
       'Austrian white blend', 'Tocai', 'Tinta Roriz',
       'Chardonnay-Viognier', 'Fernão Pires',
       'Cabernet Franc-Cabernet Sauvignon', 'Grenache-Syrah',
       'Seyval Blanc', 'Muscat Canelli', 'Cabernet Merlot',
       'Tempranillo-Cabernet Sauvignon', 'Arinto', 'Aragonez',
       'Merlot-Cabernet Franc', 'Syrah-Petite Sirah', 'Cabernet Blend',
       'Maturana', 'Pecorino', 'Rotgipfler', 'Kinali Yapincak',
       'Cabernet Franc-Carmenère', 'Magliocco', 'Gamay Noir',
       'Sauvignon Gris', 'Spätburgunder', 'Picpoul', 'Vidal Blanc',
       'Albanello', 'White Port', 'Arneis', 'Malvasia', 'Plavac Mali',
       'Lemberger', 'Saperavi', 'Altesse', 'Blanc du Bois',
       'Provence white blend', 'Nosiola', 'Dornfelder',
       'Roussanne-Viognier', 'Ojaleshi', 'Godello', 'Mondeuse',
       'Perricone', 'Pedro Ximénez', 'Auxerrois', 'Syrah-Merlot',
       'Albana', 'Muskat', 'Lambrusco', 'Cabernet Sauvignon-Malbec',
       'Tinto Fino', 'Malbec-Cabernet Sauvignon', 'Moschofilero',
       'Grechetto', 'Encruzado', 'Carignano', 'Cabernet Franc-Merlot',
       'Torbato', 'Syrah-Petit Verdot', 'Garnacha Blanca', 'Pallagrello',
       'Morava', 'Syrah-Mourvèdre', 'Aleatico', 'Carcajolu', 'Kisi',
       'Shiraz-Grenache', 'Palomino', 'Grenache-Carignan', 'Nascetta',
       'Siria', 'Malbec-Syrah', 'Asprinio', 'Feteascǎ Regalǎ',
       'Lambrusco Grasparossa', 'Marselan', 'Tocai Friulano', 'Schiava',
       'Alfrocheiro', 'Chardonnay-Semillon', 'Corvina', 'Norton',
       'Alicante Bouschet', 'Tokaji', 'Moscadello',
       'Cabernet Sauvignon-Tempranillo', 'Carignan', 'Loureiro-Arinto',
       'Cabernet-Syrah', 'Sauvignon Blanc-Chardonnay', 'Symphony',
       'Edelzwicker', 'Madeira Blend', 'Black Muscat', 'Grenache Noir',
       'Durella', 'Xinomavro', 'Tinto del Pais',
       'Merlot-Cabernet Sauvignon', 'Cercial', 'Johannisberg Riesling',
       'Petite Verdot', 'Passerina', 'Valdiguié',
       'Colombard-Sauvignon Blanc', 'Kangoun', 'Loureiro', 'Posip',
       'Uva di Troia', 'Gros and Petit Manseng', 'Jacquère',
       'Kalecik Karasi', 'Karasakiz', 'Mourvèdre-Syrah', 'Negrette',
       'Zierfandler-Rotgipfler', 'Clairette', 'Raboso', 'País', 'Mauzac',
       'Pinot Auxerrois', 'Chenin Blanc-Sauvignon Blanc', 'Diamond',
       'Marzemino', 'Tinta Barroca', 'Chardonnay-Sauvignon Blanc',
       'Castelão', 'Trebbiano Spoletino', 'Teran', 'Trepat', 'Freisa',
       'Neuburger', 'Sämling', 'Chasselas', 'Hárslevelü', 'Trincadeira',
       'Merlot-Tannat', 'Rkatsiteli', 'Melnik', 'Siegerrebe',
       'Trousseau Gris', 'Grenache Blend', 'Gros Manseng',
       'Portuguese Rosé', 'Brachetto', 'Mantonico', 'Ekigaïna',
       'Muskateller', 'Aligoté', 'Sangiovese Cabernet',
       'Touriga Nacional-Cabernet Sauvignon', 'Muscat Blanc', 'Argaman',
       'Viognier-Roussanne', 'Pallagrello Bianco', 'Bobal',
       'Malvasia Istriana', 'Cabernet Sauvignon-Cabernet Franc',
       'Baco Noir', 'Veltliner', 'Tempranillo-Tannat', 'Morillon',
       'Touriga Franca', 'Picolit', 'Barbera-Nebbiolo', 'Prieto Picudo',
       'Gaglioppo', 'Tokay', 'Sacy', 'Piedirosso', 'Piquepoul Blanc',
       'Mansois', 'Chardonnay-Sauvignon', 'Tempranillo-Garnacha',
       'Carmenère-Cabernet Sauvignon', 'Chenin Blanc-Viognier',
       'Susumaniello', 'Vitovska', 'Orange Muscat', 'Grauburgunder',
       'Carignane', 'Moscatel Roxo', 'Tannat-Merlot', 'Nerello Cappuccio',
       'Counoise', 'Macabeo', 'Mazuelo', 'Sauvignon-Sémillon',
       'Tinta del Pais', 'Vranec', 'Mavrud', "Cesanese d'Affile",
       'Moscato Giallo', 'Debit', 'Verdil', 'Cabernet',
       'Verduzzo Friulano ', 'Treixadura', "Loin de l'Oeil",
       'Coda di Volpe', 'Grenache-Mourvèdre', 'Forcallà', 'Viura-Verdejo',
       'Bombino Bianco', 'Pinot-Chardonnay', 'Syrah-Tempranillo',
       'Cabernet Sauvignon-Barbera', 'Merlot-Cabernet',
       "Muscat d'Alexandrie", 'Jaen', 'Tinta del Toro', 'Timorasso',
       'Pigato', 'Sangiovese-Cabernet Sauvignon', 'Shiraz-Cabernet',
       'Viognier-Gewürztraminer', 'Prunelard',
       'Sauvignon Blanc-Chenin Blanc', 'Gros Plant',
       'Malbec-Petit Verdot', 'Colombard-Ugni Blanc', 'Grignolino',
       'Garnacha-Syrah', 'Rufete', 'Tempranillo-Shiraz', 'Mtsvane',
       'Chardonnay-Pinot Gris', 'Marawi', 'Chardonnay-Pinot Blanc',
       'Mataro', 'Tinta Cao', 'Blauer Portugieser', 'Ugni Blanc',
       'Groppello', 'Semillon-Chardonnay', 'Irsai Oliver', 'Alvarelhão',
       'Poulsard', 'Grenache-Shiraz', 'Baga-Touriga Nacional', 'Carineña',
       'Pignoletto', 'Muscatel', 'Mavrodaphne', 'Ciliegiolo',
       'Viognier-Grenache Blanc', 'Greco Bianco',
       'Cabernet Sauvignon-Merlot-Shiraz', 'Sciaccerellu', 'Zelen',
       'Alicante', 'Emir', 'Rosenmuskateller', 'Tsolikouri', 'Narince',
       'Malbec-Cabernet', 'Touriga', 'Grecanico', 'Carmenère-Syrah',
       'Madeleine Angevine', 'Mavroudi', 'Pinot Blanc-Pinot Noir',
       'Muscat Hamburg', 'Tempranillo Blanco', 'Casavecchia',
       'Pinot Gris-Gewürztraminer', 'White Riesling', 'Tinto Velasco',
       'Hondarrabi Zuri', 'Nuragus', 'Xynisteri', 'Kadarka',
       'Sauvignon Musqué', 'Roussanne-Marsanne', 'Incrocio Manzoni',
       'Terrantez', 'Bual', 'Okuzgozu', 'Rivaner', 'Doña Blanca',
       'Graševina', 'Lambrusco Salamino', 'Sangiovese-Syrah',
       'Tannat-Cabernet Franc', 'Thrapsathiri', 'Fer Servadou', 'Mission',
       'Kekfrankos', 'Cococciola', 'Blauburgunder', 'Marquette',
       'Romorantin', 'Verdejo-Sauvignon Blanc', 'Braucol',
       'Malvasia-Viura', 'Savatiano', 'Cabernet Franc-Malbec',
       'Pallagrello Nero', 'Rebula', 'Vespolina', 'Shiraz-Malbec', 'Rebo',
       'Macabeo-Chardonnay', 'Tempranillo-Malbec', 'Tamjanika',
       'Trousseau', 'Bacchus', 'Syrah-Malbec', 'Syrah-Cabernet Franc',
       'Macabeo-Moscatel', 'Cariñena-Garnacha', 'Plyto',
       'Códega do Larinho', 'Sideritis', 'Çalkarası', 'Azal',
       'Moscatel Graúdo', 'Viosinho', 'Moschofilero-Chardonnay',
       'Paralleda', 'Rara Neagra', 'Malvasia di Candia', 'Maria Gomes',
       'Molinara', 'Malvar', 'Airen', 'Erbaluce', 'Muscat of Alexandria',
       'Verdosilla', 'Abouriou', 'Pinot Noir-Syrah', 'Nielluciu',
       'Malbec-Bonarda', 'Vespaiolo', 'Malbec-Carménère', 'Biancolella',
       'Sauvignon Blanc-Verdejo', 'Aidani', 'Garnacha-Monastrell',
       'Vinhão', 'Souzao', 'Roter Traminer', 'Moscatel de Alejandría',
       'Rolle', 'Tinta Francisca', 'Malvasia Nera', 'Orangetraube',
       'Riesling-Chardonnay', 'Žilavka', 'Portuguiser', 'Listán Negro',
       'Pinotage-Merlot', 'Muscadine', 'Maria Gomes-Bical', 'Grolleau',
       'Zlahtina', 'Syrah-Grenache-Viognier', 'Jacquez', 'Gouveio',
       'Canaiolo', 'Carignan-Syrah', 'Bombino Nero',
       'Chardonnay-Riesling', 'Malagouzia-Chardonnay', 'Mavrotragano',
       'Bovale', 'Frankovka', 'Shiraz-Roussanne', 'Cabernet-Shiraz',
       'Syrah-Carignan', 'Elbling', 'Gragnano', 'Garnacha Blend',
       'Pinot Blanc-Chardonnay', 'Schwartzriesling', 'Petit Meslier',
       'Bastardo', 'Vidadillo', 'Misket', 'Chardonnay Weissburgunder',
       'Other', 'Robola', 'Merlot-Shiraz', 'Malagouzia', 'Folle Blanche',
       'Malbec Blend', 'Merlot-Syrah', 'Tamianka', 'Cabernet Pfeffer',
       'Morio Muskat', 'Rabigato', 'Babić', 'Roviello', 'Yapincak',
       'Sauvignonasse', 'Viognier-Marsanne', 'Mandilaria', 'Meseguera',
       'Alvarinho-Chardonnay', 'Saperavi-Merlot', 'Pinot Blanc-Viognier',
       'Teroldego Rotaliano', 'Biancu Gentile', 'Garnacha-Tempranillo',
       'Xinisteri', 'Sauvignon Blanc-Sauvignon Gris',
       'Trebbiano di Lugana', 'Albarossa', 'Ryzlink Rýnský', 'Verdeca',
       'Cabernet Sauvignon Grenache', 'Tămâioasă Românească',
       'Black Monukka', 'Merlot-Grenache', 'Vranac', 'Tempranillo-Syrah',
       'Chardonel', 'Silvaner-Traminer', 'Uvalino',
       'Merseguera-Sauvignon Blanc', 'Cabernet-Malbec', 'Boğazkere',
       'Gelber Traminer', 'Vermentino Nero', 'Cayuga', 'Tinta Amarela',
       'Tinta Negra Mole', 'Moscato Rosa', 'Chelois',
       'Sauvignon Blanc-Assyrtiko', 'Muscadel', 'Shiraz-Tempranillo',
       'Roussanne-Grenache Blanc', 'Biancale', 'Ansonica',
       'Syrah-Bonarda', 'Durif', 'Franconia', 'Malbec-Tempranillo',
       'Nasco', 'Monastrell-Petit Verdot', 'Sirica', 'Vital', 'Espadeiro',
       'Apple', 'Pinot Grigio-Sauvignon Blanc', 'Blatina', 'Karalahna',
       'Feteasca', 'Sercial', 'Valvin Muscat', 'Malvasia Fina',
       'Roditis-Moschofilero', 'St. Vincent', 'Chancellor', 'Premsal',
       'Jampal', 'Tokay Pinot Gris', 'Colorino', 'Picapoll', 'Blauburger',
       'Tinta Madeira', 'Centesimino', 'Grenache Gris', 'Trajadura',
       'Merlot-Petite Verdot', 'Ramisco', 'Catalanesca',
       'Garnacha-Cabernet', 'Garnacha-Cariñena', 'Gamza',
       'Cabernet Franc-Lemberger', 'Chardonnay-Albariño',
       'Shiraz-Mourvèdre', 'Mavrokalavryta', 'Favorita', 'Babosa Negro',
       'Tintilia ', 'Dafni', 'Petit Courbu', 'Kotsifali', 'Parraleta',
       'Moscato di Noto', 'Roscetto', 'Torontel', 'Otskhanuri Sapere',
       'Viognier-Valdiguié', 'Trollinger', 'Tsapournakos', 'Francisa',
       'Kuntra', 'Pignolo', 'Caprettone', 'Ondenc', 'Athiri',
       'Bobal-Cabernet Sauvignon']

cepage = st.sidebar.selectbox(
    'Cépage', liste_cepages, index=liste_cepages.index('Pinot Noir')
)




# Création du Dataframe prenant en compte les filtres sélectionnés
df1 = df[ 
     (df['year']<=max_annee) & (df['year']>=min_annee) & (df['points']<=max_note) & (df['points']>=min_note) & (df['price']<=max_prix) & (df['price']>=min_prix) &(df.country.str.contains(pays)) & (df.variety.str.contains(cepage))
     ]

st.dataframe(df1)