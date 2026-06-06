"""
🔌 Connecteur Odeo API
Récupère les données depuis l'API Odeo (à adapter selon leur documentation)
"""

import json
import requests
from datetime import datetime

class OdeoConnector:
    def __init__(self, api_url="", api_key=""):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        """Teste la connexion à l'API Odeo"""
        if not self.api_url or not self.api_key:
            return {"status": "error", "message": "API non configurée"}
        
        try:
            r = requests.get(f"{self.api_url}/ping", headers=self.headers, timeout=10)
            return {"status": "ok" if r.status_code == 200 else "error"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_ventes_aujourdhui(self, restaurant_id):
        """Récupère les ventes du jour"""
        try:
            r = requests.get(
                f"{self.api_url}/restaurants/{restaurant_id}/ventes/aujourdhui",
                headers=self.headers,
                timeout=10
            )
            if r.status_code == 200:
                return r.json()
            return None
        except:
            return None
    
    def get_stock(self, restaurant_id):
        """Récupère les stocks actuels"""
        try:
            r = requests.get(
                f"{self.api_url}/restaurants/{restaurant_id}/stock",
                headers=self.headers,
                timeout=10
            )
            if r.status_code == 200:
                return r.json()
            return None
        except:
            return None
    
    def get_employes(self, restaurant_id):
        """Récupère les présences employés"""
        try:
            r = requests.get(
                f"{self.api_url}/restaurants/{restaurant_id}/employes",
                headers=self.headers,
                timeout=10
            )
            if r.status_code == 200:
                return r.json()
            return None
        except:
            return None
