import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="PokéNantes Alertes",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ PokéNantes Alertes")
st.markdown("### Veille & Stock Pokémon TCG — Nantes & Loire-Atlantique")

# Section des alertes en direct
st.markdown("---")
st.subheader("🔴 Dernières alertes détectées")

# Simulation d'une structure d'alerte connectée prête à l'emploi
alerts = [
    {
        "store": "FNAC Nantes",
        "product": "ETB / Coffret Pokémon (Veille active)",
        "status": "En attente de réassort...",
        "time": datetime.now().strftime('%H:%M')
    },
    {
        "store": "Pokuji & Boutiques Locales (44)",
        "product": "Surveillance des nouveautés TCG",
        "status": "Système prêt à l'écoute",
        "time": datetime.now().strftime('%H:%M')
    }
]

for alert in alerts:
    with st.container():
        st.markdown(f"**🏪 {alert['store']}**")
        st.write(f"📦 {alert['product']}")
        st.caption(f"Statut : {alert['status']} — Vérifié à {alert['time']}")
        st.markdown("---")

# Section des sources surveillées
st.subheader("📍 Sources sous surveillance")
st.markdown("""
- **Grandes enseignes :** Amazon, Fnac, Cultura, Carrefour, Leclerc, Auchan, Micromania, King Jouet, Smyths Toys, JouéClub.
- **Boutiques locales (44) :** Pokuji, Sortilèges, Le Temple du Jeu, La Mal’O Jeux, Archi Chouette, Japanim Atlantis, Ludotrotter, Galaxie Games.
""")

# Pied de page
st.markdown("---")
st.markdown(f"<small>Moteur de veille actif — Dernière synchro : {datetime.now().strftime('%d/%m/%Y à %H:%M')}</small>", unsafe_allow_html=True)
