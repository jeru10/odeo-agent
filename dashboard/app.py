"""
🌐 Dashboard Web — Interface de gestion pour le propriétaire
Built with Flask
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory

class DashboardApp:
    def __init__(self, config, agent):
        self.config = config
        self.agent = agent
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        app = self.app
        agent = self.agent
        config = self.config
        
        @app.route('/')
        def index():
            return render_template('index.html', 
                                 agent_name=config.get("agent.name", "Agent Odeo"))
        
        @app.route('/api/chat', methods=['POST'])
        def chat():
            data = request.json
            message = data.get('message', '')
            restaurant_id = data.get('restaurant_id')
            response = agent.chat(message, restaurant_id)
            return jsonify({"response": response})
        
        @app.route('/api/status')
        def status():
            return jsonify(agent.get_status())
        
        @app.route('/api/config', methods=['GET', 'POST'])
        def config_endpoint():
            if request.method == 'POST':
                data = request.json
                for key, value in data.items():
                    config.set(key, value)
                return jsonify({"status": "ok"})
            return jsonify(config.to_dict())
        
        @app.route('/api/restaurants', methods=['GET', 'POST'])
        def restaurants():
            if request.method == 'POST':
                data = request.json
                rid = agent.db.add_restaurant(
                    data['name'],
                    data.get('phone', ''),
                    data.get('address', ''),
                    data.get('odeo_api_key', '')
                )
                return jsonify({"id": rid, "status": "ok"})
            return jsonify(agent.db.get_restaurants())
        
        @app.route('/api/report', methods=['POST'])
        def generate_report():
            data = request.json
            restaurant_id = data.get('restaurant_id')
            ventes = data.get('ventes', {})
            report = agent.generate_daily_report(restaurant_id, ventes)
            return jsonify({"report": report})
        
        @app.route('/api/ollama/check')
        def check_ollama():
            return jsonify(agent.brain.check_ollama())
    
    def run(self, host="0.0.0.0", port=5000, debug=False):
        self.app.run(host=host, port=port, debug=debug)
