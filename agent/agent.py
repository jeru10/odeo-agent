"""
🤖 Agent Odeo — Orchestrateur principal
Coordonne le LLM, le RAG, les données et les actions
"""

from datetime import datetime
import json
import random

from agent.brain import Brain
from agent.rag import RAG

class Agent:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.brain = Brain(config)
        self.rag = RAG()
        self.name = config.get("agent.name", "Agent Odeo")
    
    def ask(self, question, restaurant_id=None):
        """Pose une question à l'agent"""
        # 1. Récupérer le contexte (RAG)
        contexte_rag = self.rag.get_context(question)
        
        # 2. Récupérer les données du restaurant
        donnees = {}
        if restaurant_id:
            ventes = self.db.get_ventes(restaurant_id, jours=7)
            if ventes:
                donnees["ventes"] = [
                    {"date": v[0], "total": v[1], "top_plat": v[2], "clients": v[3]}
                    for v in ventes
                ]
        
        # 3. Contexte complet
        contexte = {}
        if donnees:
            contexte["donnees_restaurant"] = donnees
        if contexte_rag:
            contexte["documents"] = contexte_rag
        
        # 4. Poser la question au LLM
        reponse = self.brain.ask(question, contexte)
        return reponse
    
    def generate_daily_report(self, restaurant_id, ventes_aujourdhui):
        """Génère le rapport quotidien pour le propriétaire"""
        prompt = f"""Fais le rapport du jour pour le propriétaire.
        
Données du jour :
- Total ventes : {ventes_aujourdhui.get('total', 0)} DH
- Nombre clients : {ventes_aujourdhui.get('nb_clients', 0)}
- Plat le plus vendu : {ventes_aujourdhui.get('top_plat', 'N/A')}
- Stocks critiques : {ventes_aujourdhui.get('stocks', 'aucune alerte')}

Donne un message court (2-3 phrases) en darija/français."""
        
        rapport = self.brain.ask(prompt)
        
        # Sauvegarder
        self.db.save_rapport(restaurant_id, "quotidien", rapport)
        
        return rapport
    
    def analyze_stock(self, stock_data):
        """Analyse les stocks et donne des recommandations"""
        prompt = f"""Analyse ces données de stock et donne des recommandations :
{json.dumps(stock_data, ensure_ascii=False, indent=2)}

Dis ce qui est critique et quoi commander."""
        
        return self.brain.ask(prompt)
    
    def chat(self, message, restaurant_id=None):
        """Interface de chat simple"""
        if not message:
            return "Salam ! Comment je peux t'aider aujourd'hui ?"
        
        return self.ask(message, restaurant_id)
    
    def get_status(self):
        """Retourne le statut de l'agent"""
        ollama_status = self.brain.check_ollama()
        
        return {
            "name": self.name,
            "mode": self.config.get("llm.mode", "local"),
            "model": self.config.get("llm.model", "mistral"),
            "ollama": ollama_status,
            "documents_rag": len(self.rag.documents),
            "odeo_connected": self.config.get("odeo.enabled", False),
            "whatsapp_connected": self.config.get("whatsapp.enabled", False)
        }
