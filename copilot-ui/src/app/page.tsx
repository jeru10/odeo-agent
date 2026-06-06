"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function AgentOdeoPage() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
        {/* Header */}
        <header className="border-b border-gray-700/50 bg-gray-900/80 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-3xl">🇲🇦</span>
              <div>
                <h1 className="text-xl font-bold text-white">Agent Odeo</h1>
                <p className="text-sm text-gray-400">Assistant IA pour Restaurants — Maroc</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              <span className="text-sm text-green-400">Ollama · Local</span>
            </div>
          </div>
        </header>

        {/* Main Chat */}
        <main className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-gray-800/50 rounded-2xl border border-gray-700/50 overflow-hidden shadow-2xl">
            <div className="h-[650px]">
              <CopilotChat
                instructions={`
                  Tu es Agent Odeo, assistant IA pour restaurants au Maroc. 🇲🇦

                  REGLES:
                  - Parle en darija marocain melange au francais
                  - Sois chaleureux et professionnel
                  - Reponds en MAX 3-4 phrases
                  - Donne des conseils actionnables

                  EXEMPLES:
                  - "Safi Yassine, aujourd'hui 5 200 dh. Plat top: couscous (15 ventes). Stock poulet presque vide."
                  - "Moulay, comparaison vs hier: +12% clients. Faut preparer plus de viande pour samedi."
                `}
                labels={{
                  title: "Agent Odeo",
                  initial: "Salam! 🇲🇦\n\nJe suis Agent Odeo, ton assistant IA pour le restaurant.\n\nPose-moi des questions sur:\n📊 Les ventes et analyse\n📦 La gestion du stock\n💰 Les conseils financiers\n👨‍🍳 Le personnel\n\nComment je peux t'aider aujourd'hui?",
                }}
              />
            </div>
          </div>
        </main>
      </div>
    </CopilotKit>
  );
}
