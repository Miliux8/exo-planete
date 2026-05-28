import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page (en mode "Large" pour bien voir la 3D)
st.set_page_config(page_title="Explorateur 3D", page_icon="🌌", layout="wide")

st.title("🌌 Explorateur 3D de l'Univers")
st.markdown("Tournez le graphique avec votre doigt ou votre souris. Zoomez pour explorer le nuage de points et cliquez sur une planète pour voir ses caractéristiques !")

# 2. Chargement et nettoyage des données
@st.cache_data
def load_data():
    # Remplace sep=';' ou sep=',' selon ton fichier
    df = pd.read_csv('data_set.csv', encoding='latin-1', sep=',') 
    
    # On enlève les planètes où il manque des infos cruciales
    df = df.dropna(subset=['P_MASS', 'P_RADIUS', 'P_TEMP_SURF', 'P_NAME', 'P_ESI'])
    
    # On filtre les immenses géantes gazeuses (Masse > 30) pour que le graphique 
    # reste "zoomé" sur les planètes de type terrestre ou super-terres.
    df = df[df['P_MASS'] < 30]
    return df

df = load_data()

# 3. Astuce : Ajouter "La Terre" manuellement pour avoir un point de repère !
terre = pd.DataFrame([{
    'P_NAME': '🌍 LA TERRE (Notre repère)', 
    'P_MASS': 1.0, 
    'P_RADIUS': 1.0, 
    'P_TEMP_SURF': 288.0, 
    'P_ESI': 1.0, 
    'P_HABITABLE': 1
}])
# On fusionne la Terre avec le reste des données
df = pd.concat([terre, df], ignore_index=True)

# 4. Création du graphique 3D avec Plotly
fig = px.scatter_3d(
    df,
    x='P_MASS',
    y='P_RADIUS',
    z='P_TEMP_SURF',
    color='P_ESI',          # La couleur dépend du score de ressemblance avec la Terre
    hover_name='P_NAME',    # Le nom s'affiche quand on passe la souris
    hover_data={
        'P_MASS': True, 
        'P_RADIUS': True, 
        'P_TEMP_SURF': True, 
        'P_ESI': True
    },
    color_continuous_scale='Turbo', # Une magnifique palette de couleurs (du bleu au rouge vif)
    opacity=0.8,
    size_max=10
)

# 5. Personnalisation pour un look "Espace"
fig.update_layout(
    template='plotly_dark', # Fond noir de l'espace !
    scene=dict(
        xaxis_title="Masse (Terres)",
        yaxis_title="Rayon (Terres)",
        zaxis_title="Température (K)"
    ),
    margin=dict(l=0, r=0, b=0, t=40) # Enlève les marges blanches autour
)

# 6. Affichage sur le site Web
st.plotly_chart(fig, use_container_width=True)
