from flask import Flask, jsonify, request
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib
import re
from datetime import datetime, timezone

app = Flask(__name__)

DB_FILE = "pokenantes.db"
SOURCES_FILE = "sources.json"

KEYWORDS = re.compile(
    r"\b(pokemon|pokémon|tcg|trading card|etb|display|booster|"
    r"coffret|collection|précommande|precommande|preorder|"
    r"restock|réassort|stock|disponible)\b",
    re.IGNORECASE
)


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            detected_at TEXT NOT NULL,
            fingerprint TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def load_sources():
    if not os.path.exists(SOURCES_FILE):
        return []

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_alert(source, title, url):
    fingerprint = hashlib.sha256(
        f"{source}|{title}|{url}".encode("utf-8")
    ).hexdigest()

    conn = get_db()

    try:
        conn.execute(
            """
            INSERT INTO alerts
            (source, title, url, detected_at, fingerprint)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                source,
                title,
                url,
                datetime.now(timezone.utc).isoformat(),
                fingerprint,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()


def check_source(source):
    name = source.get("name", "Source")
    url = source.get("url")

    if not url:
        return {
            "source": name,
            "status": "error",
            "message": "URL manquante"
        }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 Safari/604.1"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:
            return {
                "source": name,
                "status": "error",
                "message": f"HTTP {response.status_code}"
            }

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style", "noscript"]):
            element.decompose()

        text = soup.get_text(" ", strip=True)

        if KEYWORDS.search(text):
            add_alert(
                name,
                f"Activité Pokémon détectée sur {name}",
                url
            )

            return {
                "source": name,
                "status": "signal",
                "message": "Mots-clés Pokémon détectés"
            }

        return {
            "source": name,
            "status": "ok",
            "message": "Aucun nouveau signal détecté"
        }

    except Exception as e:
        return {
            "source": name,
            "status": "error",
            "message": str(e)
        }


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>PokéNantes Alertes</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                margin: 0;
                padding: 20px;
            }

            .container {
                max-width: 700px;
                margin: auto;
            }

            h1 {
                margin-bottom: 5px;
            }

            .subtitle {
                color: #666;
            }

            .card {
                background: white;
                padding: 16px;
                border-radius: 14px;
                margin-top: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,.08);
            }

            button {
                background: #111;
                color: white;
                border: 0;
                padding: 12px 16px;
                border-radius: 10px;
                font-weight: bold;
            }

            a {
                color: #0066cc;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>⚡ PokéNantes Alertes</h1>

            <div class="subtitle">
                Alertes Pokémon TCG — Nantes & Loire-Atlantique
            </div>

            <div class="card">

                <h2>Dernières alertes</h2>

                <div id="alerts">
                    Chargement...
                </div>

            </div>

            <div class="card">

                <h2>Surveillance</h2>

                <p>
                    Amazon, Fnac, Cultura, Carrefour, Leclerc,
                    Auchan, Micromania et boutiques locales.
                </p>

            </div>

        </div>

        <script>

            async function loadAlerts() {

                const response =
                    await fetch("/api/alerts");

                const alerts =
                    await response.json();

                const container =
                    document.getElementById("alerts");

                if (!alerts.length) {

                    container.innerHTML =
                        "<p>Aucune alerte pour le moment.</p>";

                    return;
                }

                container.innerHTML =
                    alerts.map(alert => `

                        <div class="card">

                            <strong>
                                ${alert.title}
                            </strong>

                            <p>
                                ${alert.source}
                            </p>

                            <a href="${alert.url}"
                               target="_blank">

                                Voir la source

                            </a>

                        </div>

                    `).join("");

            }

            loadAlerts();

        </script>

    </body>

    </html>
    """


@app.route("/api/alerts")
def api_alerts():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT id, source, title, url, detected_at
        FROM alerts
        ORDER BY id DESC
        LIMIT 100
        """
    ).fetchall()

    conn.close()

    return jsonify([
        dict(row)
        for row in rows
    ])


@app.route("/api/sources")
def api_sources():
    return jsonify(load_sources())


@app.route("/admin/check", methods=["POST"])
def admin_check():

    token = request.args.get("token")

    expected = os.environ.get(
        "POKENANTES_ADMIN_TOKEN",
        "dev-token"
    )

    if token != expected:

        return jsonify({
            "error": "Unauthorized"
        }), 401

    sources = load_sources()

    results = []

    for source in sources:

        if source.get("enabled", True):

            results.append(
                check_source(source)
            )

    return jsonify({
        "checked_at":
            datetime.now(timezone.utc).isoformat(),

        "results": results
    })


init_db()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )
