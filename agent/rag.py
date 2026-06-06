"""
📚 RAG — Recherche dans les documents du restaurant
Menu, tarifs, infos... sans base vectorielle (simple pour commencer)
"""

import os
import json

class RAG:
    def __init__(self):
        self.documents = []
    
    def add_document(self, texte, source="manuel"):
        """Ajoute un document texte"""
        self.documents.append({
            "texte": texte,
            "source": source
        })
    
    def add_file(self, filepath):
        """Ajoute un fichier texte"""
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.add_document(content, source=os.path.basename(filepath))
            return True
        except:
            return False
    
    def add_menu(self, items):
        """Ajoute un menu (liste de plats avec prix)"""
        texte = "MENU DU RESTAURANT :\n"
        for item in items:
            texte += f"- {item.get('nom')} : {item.get('prix', '?')} dh\n"
            if 'ingredients' in item:
                texte += f"  Ingrédients : {item['ingredients']}\n"
        self.add_document(texte, source="menu")
    
    def search(self, query, max_results=3):
        """Recherche simple par mots-clés"""
        if not self.documents:
            return []
        query_lower = query.lower()
        results = []
        for doc in self.documents:
            if query_lower in doc["texte"].lower():
                results.append(doc)
        return results[:max_results]
    
    def get_context(self, query=""):
        """Retourne le contexte formaté pour le LLM"""
        if not query or not self.documents:
            return ""
        results = self.search(query)
        if not results:
            return ""
        context = "📄 INFORMATIONS DU RESTAURANT :\n"
        for r in results:
            context += f"\n--- {r['source']} ---\n{r['texte'][:500]}..."
        return context
    
    def get_all_context(self):
        """Retourne TOUS les documents pour le contexte"""
        if not self.documents:
            return ""
        context = "📄 INFORMATIONS COMPLÈTES DU RESTAURANT :\n"
        for r in self.documents:
            context += f"\n--- {r['source']} ---\n{r['texte'][:1000]}...\n"
        return context
