"""
⚙️ Configuration — Lecture et gestion du config.json
"""

import json
import os

class Config:
    def __init__(self, path="config.json"):
        self.path = path
        self.data = self._load()
    
    def _load(self):
        """Charge la configuration depuis le fichier JSON"""
        default_config = {
            "agent": {
                "name": "Agent Odeo",
                "version": "1.0.0",
                "language": "darija"
            },
            "llm": {
                "mode": "local",
                "model": "mistral",
                "api_key": "",
                "api_url": "https://api.deepseek.com/v1/chat/completions"
            },
            "odeo": {
                "enabled": False,
                "api_url": "",
                "api_key": ""
            },
            "whatsapp": {
                "enabled": False,
                "phone_number_id": "",
                "token": ""
            },
            "dashboard": {
                "port": 5000,
                "host": "0.0.0.0"
            },
            "database": {
                "path": "data/agent.db"
            }
        }
        
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    for key, value in loaded.items():
                        if key in default_config:
                            if isinstance(value, dict):
                                default_config[key].update(value)
                            else:
                                default_config[key] = value
        except Exception as e:
            print(f"⚠️ Erreur config : {e}. Utilisation des valeurs par défaut.")
        
        return default_config
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key, value):
        keys = key.split('.')
        target = self.data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self.save()
    
    def save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde config : {e}")
    
    def to_dict(self):
        return self.data
