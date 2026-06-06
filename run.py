"""
🎯 Agent Odeo — Point d'entrée principal
Lance l'agent complet : LLM + Dashboard + API
"""

import os
import sys
import json
import threading
import webbrowser

# Forcer UTF-8 dans la console Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Imports de notre projet
from core.config import Config
from core.database import Database
from agent.agent import Agent
from dashboard.app import DashboardApp


def main():
    print("""
╔══════════════════════════════════════════╗
║         🤖 AGENT ODEO v1.0              ║
║   Assistant IA pour Restaurants 🇲🇦      ║
║   Maroc — Darija / Français             ║
╚══════════════════════════════════════════╝
    """)
    
    # 1. Charger la configuration
    config = Config()
    print("✅ Configuration chargée")
    
    # 2. Initialiser la base de données
    db = Database(config.get("database.path", "data/agent.db"))
    print("✅ Base de données prête")
    
    # 3. Créer l'agent
    agent = Agent(config, db)
    print("✅ Agent initialisé")
    
    # 4. Lancer le dashboard web
    dashboard = DashboardApp(config, agent)
    
    # 5. Ouvrir le navigateur
    port = config.get("dashboard.port", 5000)
    print(f"\n🌐 Dashboard : http://localhost:{port}")
    print("📱 WhatsApp : à configurer dans le dashboard")
    print("\nAppuie sur Ctrl+C pour arrêter.\n")
    
    # 6. Lancer le serveur
    try:
        dashboard.run(
            host=config.get("dashboard.host", "0.0.0.0"),
            port=port,
            debug=False
        )
    except KeyboardInterrupt:
        print("\n👋 Arrêt de l'Agent Odeo. À bientôt !")


if __name__ == "__main__":
    main()
