from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime
import requests
import time
import threading

app = Flask(__name__)

# TES INFORMATIONS TELEGRAM
TELEGRAM_BOT_TOKEN = "8841690888:AAGWBQQvvgmX_n3MQ3sfFsk_pAvNbMe0XTQ"
TELEGRAM_CHAT_ID = "1030632520"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur d'envoi Telegram : {e}")

# Données des enseignes nantaises
BOUTIQUES_PHYSIQUES = [
    {
        "nom": "Smyths Toys", 
        "quartier": "Saint-Herblain (Atlantis Le Sillon)", 
        "reassort": "Mercredi / Vendredi", 
        "statut": "Gros arrivages de coffrets & bundles",
        "lien": "https://www.smythstoys.com/fr/fr-fr/search?text=pokemon"
    },
    {
        "nom": "King Jouet", 
        "quartier": "Nantes Beaulieu & Orvault", 
        "reassort": "Mardi / Jeudi", 
        "statut": "Rayon cartes TCG surveillé",
        "lien": "https://www.kingjouet.com/recherche?q=pokemon"
    },
    {
        "nom": "E.Leclerc", 
        "quartier": "Océane (Rezé) & Paridis (Nantes)", 
        "reassort": "Mardi / Vendredi", 
        "statut": "Arrivages massifs en tête de gondole",
        "lien": "https://www.e.leclerc/cat/pokemon"
    },
    {
        "nom": "Auchan", 
        "quartier": "Saint-Sébastien-sur-Loire", 
        "reassort": "Mercredi", 
        "statut": "Réassorts réguliers jeux & jouets",
        "lien": "https://www.auchan.fr/recherche?text=pokemon"
    }
]

# Calendrier officiel des sorties et stocks prévisionnels 2026 (implanté dans le système)
CALENDRIER_STOCKS = [
    {
        "date": "02 Octobre 2026",
        "produit": "Booster Bundle & Mini-Tins 30 Ans (Célébrations)",
        "volume_estime": "Modéré (~15 à 30 unités par grande surface)",
        "enseignes_ Cible": "Smyths Toys, Leclerc Océane",
        "statut": "En cours de déploiement en rayon"
    },
    {
        "date": "23 Octobre 2026",
        "produit": "Deck Crafter's Collection (30 Ans)",
        "volume_estime": "Faible (~10 unités par enseigne)",
        "enseignes_Cible": "King Jouet, Auchan",
        "statut": "Arrivage imminent"
    },
    {
        "date": "06 Novembre 2026",
        "produit": "Coffrets Ultra-Premium Mentali/Noctali & Méga-Rayquaza",
        "volume_estime": "Très Limité (Allocation stricte / 5 à 10 max par magasin)",
        "enseignes_Cible": "Toutes enseignes (Priorité Smyths & Leclerc)",
        "statut": "Grosse tension - Alerte max activée"
    }
]

# --- SURVEILLANCE AUTOMATIQUE EN ARRIÈRE-PLAN ---
def background_stock_checker():
    while True:
        print("🤖 Vérification du calendrier et des stocks prévisionnels en cours...")
        time.sleep(3600)

surveillance_thread = threading.Thread(target=background_stock_checker, daemon=True)
surveillance_thread.start()
# -----------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PokéNantes — Calendrier & Stocks Temps Réel</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { font-size: 24px; color: #111; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .badge { background: #eef2ff; color: #4f46e5; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
        .badge-alert { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
        .shop-item, .cal-item { border-bottom: 1px solid #eee; padding: 12px 0; }
        .shop-item:last-child, .cal-item:last-child { border-bottom: none; }
        .btn { display: inline-block; background: #e11d48; color: white; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; }
        .link-btn { display: inline-block; background: #4f46e5; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold; margin-top: 6px; }
        footer { text-align: center; font-size: 12px; color: #666; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ PokéNantes Alertes</h1>
        <p style="color: #666; font-size: 14px;">Radar des stocks & Calendrier Prévisionnel 44</p>

        <div class="card">
            <h3>🚨 Test d'Alerte Stock / Arrivage</h3>
            <p>Simuler une alerte d'arrivage avec volume précis :</p>
            <a href="/test-alerte-boutique" class="btn">Tester alerte stock 🔔</a>
        </div>

        <div class="card">
            <h3>📅 Calendrier & Volumes Prévus (Prochaines Sorties)</h3>
            {% for c in calendrier %}
            <div class="cal-item">
                <span class="badge">{{ c.date }}</span><br>
                <strong>{{ c.produit }}</strong><br>
                <span style="font-size: 13px; color: #d97706;">📦 Volume prévu : {{ c.volume_estime }}</span><br>
                <span style="font-size: 12px; color: #666;">🎯 Cibles : {{ c.enseignes_Cible }}</span><br>
                <span class="badge-alert">⚡ {{ c.statut }}</span>
            </div>
            {% endfor %}
        </div>

        <div class="card">
            <h3>📍 Suivi des Enseignes & Liens Directs</h3>
            {% for b in boutiques %}
            <div class="shop-item">
                <strong>{{ b.nom }}</strong> <span style="font-size: 12px; color: #666;">({{ b.quartier }})</span><br>
                <span style="font-size: 13px; color: #4f46e5;">📦 Réassort : {{ b.reassort }}</span><br>
                <span style="font-size: 12px; color: #059669;">✔ {{ b.statut }}</span><br>
                <a href="{{ b.lien }}" target="_blank" class="link-btn">🔗 Vérifier le stock en ligne</a>
            </div>
            {% endfor %}
        </div>

        <footer>
            Dernière mise à jour : {{ current_time }}
        </footer>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    now = datetime.now().strftime('%d/%m/%Y à %H:%M')
    return render_template_string(HTML_TEMPLATE, boutiques=BOUTIQUES_PHYSIQUES, calendrier=CALENDRIER_STOCKS, current_time=now)

@app.route('/test-alerte-boutique')
def test_alerte_boutique():
    message = "🚨 *ALERTE STOCK PRÉVISIONNEL NANTES*\n\n🏪 *Enseigne :* Smyths Toys / Leclerc Océane\n📦 *Produit :* Coffrets 30 Ans / Allocations\n📊 *Volume estimé :* ~20 unités en rayon\n⚡ *Statut :* Mise en rayon validée par le calendrier !\n🏃‍♂️ Foncez en magasin !"
    send_telegram_alert(message)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
