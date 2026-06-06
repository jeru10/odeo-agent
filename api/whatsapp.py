"""
📱 Connecteur WhatsApp (Meta Cloud API)
Envoie des messages aux propriétaires
"""

import requests
import json

class WhatsAppSender:
    def __init__(self, phone_number_id="", token=""):
        self.phone_number_id = phone_number_id
        self.token = token
        self.base_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    
    def test_connection(self):
        if not self.phone_number_id or not self.token:
            return {"status": "error", "message": "WhatsApp non configuré"}
        return {"status": "ok", "message": "WhatsApp configuré"}
    
    def send_message(self, to_number, message):
        """
        Envoie un message WhatsApp
        to_number : +212XXXXXXXXX
        """
        if not self.token:
            return {"status": "error", "message": "Token non configuré"}
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": to_number,
                    "type": "text",
                    "text": {"body": message}
                },
                timeout=15
            )
            
            if response.status_code == 200:
                return {"status": "ok", "message_id": response.json().get("messages", [{}])[0].get("id")}
            else:
                return {"status": "error", "message": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def send_template(self, to_number, template_name, parameters=[]):
        """Envoie un template WhatsApp (pour messages approuvés)"""
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": to_number,
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "language": {"code": "fr"},
                        "components": [{
                            "type": "body",
                            "parameters": [{"type": "text", "text": p} for p in parameters]
                        }]
                    }
                },
                timeout=15
            )
            return {"status": "ok" if response.status_code == 200 else "error"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
