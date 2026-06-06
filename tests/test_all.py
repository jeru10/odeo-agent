"""
Tests de base — Vérifie que tout fonctionne
"""

import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Vérifie que tous les modules s'importent correctement"""
    try:
        from core.config import Config
        print("✅ core.config importé")
        
        from core.database import Database
        print("✅ core.database importé")
        
        from agent.brain import Brain
        print("✅ agent.brain importé")
        
        from agent.rag import RAG
        print("✅ agent.rag importé")
        
        from agent.agent import Agent
        print("✅ agent.agent importé")
        
        from api.odeo import OdeoConnector
        print("✅ api.odeo importé")
        
        from api.whatsapp import WhatsAppSender
        print("✅ api.whatsapp importé")
        
        from dashboard.app import DashboardApp
        print("✅ dashboard.app importé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur d'import : {e}")
        return False

def test_config():
    """Test de la configuration"""
    from core.config import Config
    config = Config("config.json")
    
    assert config.get("agent.name") == "Agent Odeo"
    assert config.get("llm.mode") == "local"
    assert config.get("llm.model") == "mistral"
    assert config.get("dashboard.port") == 5000
    
    print("✅ Configuration OK")
    return True

def test_database():
    """Test de la base de données"""
    from core.database import Database
    
    db = Database(":memory:")  # Base temporaire en mémoire
    
    # Ajouter un restaurant
    rid = db.add_restaurant("Resto Test", "+212600000000", "Marrakech")
    assert rid is not None
    print(f"✅ Restaurant ajouté (id={rid})")
    
    # Ajouter des ventes
    db.save_vente(rid, "2026-06-06", 5200, "couscous", 30, '{"detail": "test"}')
    db.save_vente(rid, "2026-06-05", 4800, "tajine", 25, '{}')
    print("✅ Ventes ajoutées")
    
    # Récupérer les ventes
    ventes = db.get_ventes(rid, jours=7)
    assert len(ventes) == 2
    print(f"✅ {len(ventes)} ventes récupérées")
    
    db.close()
    return True

def test_rag():
    """Test du système RAG"""
    from agent.rag import RAG
    
    rag = RAG()
    
    # Ajouter des documents
    rag.add_document("Le couscous est le plat le plus populaire, prix 65 dh", "menu")
    rag.add_document("Ouvert de 12h à 23h, fermé le lundi", "horaires")
    rag.add_document("Spécialité : tajine de poulet aux olives, 75 dh", "menu")
    
    context = rag.get_context("couscous")
    assert "couscous" in context
    print(f"✅ RAG fonctionne : contexte trouvé")
    
    context_all = rag.get_all_context()
    assert "Ouvert" in context_all
    print(f"✅ RAG : tous les documents accessibles")
    
    return True

def test_brain():
    """Test du cerveau (sans Ollama — vérifie juste la structure)"""
    from core.config import Config
    from agent.brain import Brain
    
    config = Config("config.json")
    brain = Brain(config)
    
    # Vérifie que le système prompt est bien construit
    assert "darija" in brain.system_prompt
    assert "Maroc" in brain.system_prompt
    print("✅ Cerveau initialisé correctement")
    
    # Test check_ollama (ne doit pas planter si Ollama pas lancé)
    result = brain.check_ollama()
    assert "status" in result
    print(f"✅ Check Ollama : {result['status']}")
    
    return True

if __name__ == "__main__":
    print("🧪 TESTS AGENT ODEO\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Base de données", test_database),
        ("RAG", test_rag),
        ("Cerveau", test_brain),
    ]
    
    success = 0
    for name, func in tests:
        print(f"\n--- {name} ---")
        try:
            if func():
                success += 1
        except Exception as e:
            print(f"❌ {e}")
    
    print(f"\n{'='*40}")
    print(f"📊 Résultat : {success}/{len(tests)} tests réussis")
    
    if success == len(tests):
        print("🌟 Tout est prêt !")
    else:
        print("⚠️ Certains tests ont échoué")
