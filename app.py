from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime
import requests

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

# Données des grandes surfaces, King Jouet, Smyths Toys et King Discount sur Nantes & alentours
BOUTIQUES_PHYSIQUES = [
    {"nom": "Smyths Toys", "quartier": "Saint-Herblain (Atlantis Le Sillon)", "reassort": "Mercredi / Vendredi", "statut": "Gros arrivages de coffrets & bundles"},
    {"nom": "King Jouet", "quartier": "Nantes Beaulieu & Orvault", "reassort": "Mardi / Jeudi", "statut": "Rayon cartes TCG surveillé"},
    {"nom": "King Discount / King Adult", "quartier": "Agglomération Nantaise", "reassort": "Variable", "statut": "Bons plans & destockage"},
    {"nom": "E.Leclerc", "quartier": "Océane (Rezé) & Paridis (Nantes)", "reassort": "Mardi / Vendredi", "statut": "Arrivages massifs en tête de gondole"},
    {"nom": "Auchan", "quartier": "Saint-Sébastien-sur-Loire", "reassort": "Mercredi", "statut": "Réassorts réguliers jeux & jouets"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PokéNantes Alertes — Grandes Surfaces & Jouets</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { font-size: 24px; color: #111; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .badge { background: #eef2ff; color: #4f46e5; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
        .shop-item { border-bottom: 1px solid #eee; padding: 10px 0; }
        .shop-item:last-child { border-bottom: none; }
        .btn { display: inline-block; background: #e11d48; color: white; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; }
        footer { text-align: center; font-size: 12px; color: #666; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ PokéNantes Alertes</h1>
        <p style="color: #666; font-size: 14px;">Radar des stocks — Grandes Surfaces & Magasins de Jouets (44)</p>

        <div class="card">
            <h3>🚨 Test d'alerte Réassort Enseigne</h3>
            <p>Simuler une alerte d'arrivage en grande surface / magasin de jouets :</p>
            <a href="/test-alerte-boutique" class="btn">Tester alerte enseigne 🔔</a>
        </div>

        <div class="card">
            <h3>📍 Suivi des Enseignes & Jours de Réassort</h3>
            {% for b in boutiques %}
            <div class="shop-item">
                <strong>{{ b.nom }}</strong> <span style="font-size: 12px; color: #666;">({{ b.quartier }})</span><br>
                <span style="font-size: 13px; color: #4f46e5;">📦 Réassort habituel : {{ b.reassort }}</span><br>
                <span style="font-size: 12px; color: #059669;">✔ {{ b.statut }}</span>
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
    return render_template_string(HTML_TEMPLATE, boutiques=BOUTIQUES_PHYSIQUES, current_time=now)

@app.route('/test-alerte-boutique')
def test_alerte_boutique():
    message = "🚨 *ALERTE RÉASSORT GRANDE SURFACE / JOUET*\n\n🏪 *Enseigne :* Smyths Toys / Leclerc\n📦 *Arrivage détecté :* Nouveaux coffrets Pokémon TCG\n⚡ *Statut :* Mise en rayon en cours !\n🏃‍♂️ Foncez sur place !"
    send_telegram_alert(message)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
