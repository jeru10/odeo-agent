"""
💾 Base de données — Stockage local avec SQLite
"""

import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data/agent.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Crée les tables nécessaires"""
        self.cursor.executescript("""
            -- Restaurants
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                odeo_api_key TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Ventes quotidiennes
            CREATE TABLE IF NOT EXISTS ventes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER,
                date DATE,
                total REAL,
                plat_plus_vendu TEXT,
                nb_clients INTEGER,
                data_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            );
            
            -- Alertes / Rapports envoyés
            CREATE TABLE IF NOT EXISTS rapports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER,
                type TEXT,
                message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            );
            
            -- Configuration agent par restaurant
            CREATE TABLE IF NOT EXISTS agent_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER UNIQUE,
                lang TEXT DEFAULT 'darija',
                auto_report BOOLEAN DEFAULT 1,
                report_hour INTEGER DEFAULT 22,
                whatsapp_enabled BOOLEAN DEFAULT 0,
                whatsapp_number TEXT,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            );
        """)
        self.conn.commit()
    
    def add_restaurant(self, name, phone="", address="", odeo_api_key=""):
        """Ajoute un restaurant"""
        self.cursor.execute(
            "INSERT INTO restaurants (name, phone, address, odeo_api_key) VALUES (?, ?, ?, ?)",
            (name, phone, address, odeo_api_key)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_restaurants(self):
        """Liste tous les restaurants"""
        self.cursor.execute("SELECT * FROM restaurants ORDER BY name")
        return self.cursor.fetchall()
    
    def save_vente(self, restaurant_id, date, total, plat_plus_vendu="", nb_clients=0, data_json=""):
        """Enregistre les ventes du jour"""
        self.cursor.execute(
            """INSERT INTO ventes (restaurant_id, date, total, plat_plus_vendu, nb_clients, data_json)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (restaurant_id, date, total, plat_plus_vendu, nb_clients, data_json)
        )
        self.conn.commit()
    
    def get_ventes(self, restaurant_id, jours=7):
        """Récupère les ventes des N derniers jours"""
        self.cursor.execute(
            """SELECT date, total, plat_plus_vendu, nb_clients 
               FROM ventes 
               WHERE restaurant_id = ? 
               ORDER BY date DESC LIMIT ?""",
            (restaurant_id, jours)
        )
        return self.cursor.fetchall()
    
    def save_rapport(self, restaurant_id, type_rapport, message):
        """Enregistre un rapport envoyé"""
        self.cursor.execute(
            "INSERT INTO rapports (restaurant_id, type, message) VALUES (?, ?, ?)",
            (restaurant_id, type_rapport, message)
        )
        self.conn.commit()
    
    def close(self):
        self.conn.close()
