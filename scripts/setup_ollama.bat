@echo off
REM 🦙 Setup Ollama — Télécharge et lance le modèle

echo.
echo ╔══════════════════════════════════════════╗
echo ║   🦙 OLLAMA SETUP                        ║
echo ║   Installation du modele local           ║
echo ╚══════════════════════════════════════════╝
echo.

:: Vérifier si Ollama est installé
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama n'est pas installe.
    echo.
    echo Va sur https://ollama.ai/download
    echo Telecharge et installe Ollama pour Windows.
    echo.
    pause
    exit /b
)
echo ✅ Ollama detecte

:: Vérifier si le modèle est déjà téléchargé
ollama list | findstr "mistral" >nul
if %errorlevel% equ 0 (
    echo ✅ Modele mistral deja telecharge
) else (
    echo 📥 Telechargement du modele mistral (4 Go environ)...
    echo Cela peut prendre quelques minutes...
    ollama pull mistral
    echo ✅ Modele mistral telecharge
)

:: Lancer le serveur
echo.
echo 🚀 Demarrage du serveur Ollama...
echo Le serveur tourne maintenant en arriere-plan.
echo Tu peux fermer cette fenetre.
echo.
start /B ollama serve

echo.
echo ✅ Ollama est pret !
echo Teste avec : ollama run mistral
echo.
pause
