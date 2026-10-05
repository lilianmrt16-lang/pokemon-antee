import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="PokéNantes Alertes",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ PokéNantes Alertes")
st.markdown("### Alertes Pokémon TCG — Nantes & Loire-Atlantique")

# Section Dernières alertes
st.markdown("---")
st.subheader("Dernières alertes")

# Pour l'instant, aucune alerte détectée
st.info("Aucune alerte pour le moment.")

# Section Surveillance
st.markdown("---")
st.subheader("Surveillance")
st.write("Amazon, Fnac, Cultura, Carrefour, Leclerc, Auchan, Micromania et boutiques locales.")

# Petit pied de page
st.markdown("---")
st.markdown(f"<small>Dernière vérification : {datetime.now().strftime('%d/%m/%Y à %H:%M')}</small>", unsafe_allow_html=True)
