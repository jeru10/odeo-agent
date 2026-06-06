"""
🧠 Cerveau de l'agent — Connexion au LLM (Ollama local ou API)
"""

import json
import requests
import subprocess
import os

class Brain:
    def __init__(self, config):
        self.config = config
        self.mode = config.get("llm.mode", "local")
        self.model = config.get("llm.model", "mistral")
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        return """Tu es un assistant AI pour restaurants au Maroc. 🇲🇦

RÈGLES STRICTES :
1. Parle en darija marocain mélangé au français (comme un vrai marocain)
2. Sois précis avec les chiffres
3. Donne des conseils actionnables (pas de généralités)
4. Si tu as des données, utilise-les. Sinon, dis-le honnêtement
5. Réponds en MAX 3 phrases pour les alertes, plus long pour les analyses

EXEMPLES DE RÉPONSE :
- "Safi Yassine, aujourd'hui 5 200 dh. Plat top : couscous (15 ventes). Stock poulet presque vide."
- "Moulay, comparaison vs hier : +12% de clients. Viande faut commander pour samedi."

CONTEXTE : Tu aides le propriétaire à gérer son resto. Sois utile, pas verbeux."""
    
    def ask(self, prompt, contexte=None):
        """Pose une question au LLM"""
        try:
            if self.mode == "local":
                return self._ask_ollama(prompt, contexte)
            else:
                return self._ask_api(prompt, contexte)
        except Exception as e:
            return f"❌ Erreur LLM : {e}"
    
    def _ask_ollama(self, prompt, contexte=None):
        """Appel à Ollama en local (gratuit)"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if contexte:
            messages.append({
                "role": "system",
                "content": f"Données du restaurant : {json.dumps(contexte, ensure_ascii=False)}"
            })
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": self.model, "messages": messages, "stream": False},
            timeout=60
        )
        return response.json()["message"]["content"]
    
    def _ask_api(self, prompt, contexte=None):
        """Appel à une API LLM (DeepSeek, OpenAI...)"""
        api_key = self.config.get("llm.api_key", "")
        api_url = self.config.get("llm.api_url", "")
        
        if not api_key:
            return "❌ Clé API manquante. Configure-la dans config.json ou le dashboard."
        
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if contexte:
            messages.append({
                "role": "system",
                "content": f"Données : {json.dumps(contexte, ensure_ascii=False)}"
            })
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={"model": self.model, "messages": messages},
            timeout=60
        )
        return response.json()["choices"][0]["message"]["content"]
    
    def check_ollama(self):
        """Vérifie si Ollama est accessible"""
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            if r.status_code == 200:
                models = r.json().get("models", [])
                return {
                    "status": "ok",
                    "models": [m["name"] for m in models]
                }
        except:
            pass
        return {"status": "error", "models": []}
