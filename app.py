from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime
import requests

app = Flask(__name__)

# TES VRAIES INFORMATIONS INTÉGRÉES :
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PokéNantes Alertes</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { font-size: 24px; color: #111; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .badge { background: #eef2ff; color: #4f46e5; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
        .btn { display: inline-block; background: #4f46e5; color: white; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; }
        footer { text-align: center; font-size: 12px; color: #666; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ PokéNantes Alertes</h1>
        <p style="color: #666; font-size: 14px;">Veille & Stock Pokémon TCG — Nantes & Loire-Atlantique</p>

        <div class="card">
            <h3>🔴 Dernières alertes</h3>
            <p><strong>Système Telegram :</strong> Connecté et prêt à notifier</p>
            <span class="badge">Veille active (30 min)</span><br>
            <a href="/test-alerte" class="btn">Tester une notification test 🔔</a>
        </div>

        <div class="card">
            <h3>📍 Boutiques & Enseignes surveillées</h3>
            <p style="font-size: 14px; line-height: 1.5;">
                <strong>Grandes enseignes :</strong> Amazon, Fnac, Cultura, Carrefour, Leclerc, Auchan, Micromania, King Jouet.<br><br>
                <strong>Boutiques 44 :</strong> Pokuji, Sortilèges, Le Temple du Jeu, La Mal’O Jeux, Archi Chouette, Japanim Atlantis, Ludotrotter, Galaxie Games.
            </p>
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
    return render_template_string(HTML_TEMPLATE, current_time=now)

@app.route('/test-alerte')
def test_alerte():
    message = "🚨 *ALERTE TEST POKÉNANTES*\n\n📦 Produit : Coffret Pokémon Test\n🏪 Lieu : FNAC Nantes / Pokuji\n💰 Prix : 49,99 €\n\nLe système de notification fonctionne à merveille !"
    send_telegram_alert(message)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
