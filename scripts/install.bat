@echo off
REM ╔══════════════════════════════════════════╗
REM ║   🤖 AGENT ODEO — Installation Windows  ║
REM ╚══════════════════════════════════════════╝

echo.
echo ╔══════════════════════════════════════════╗
echo ║   🤖 INSTALLATION AGENT ODEO            ║
echo ║   Assistant IA pour Restaurants 🇲🇦     ║
echo ╚══════════════════════════════════════════╝
echo.

:: Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [01/04] ❌ Python n'est pas installe.
    echo.
    echo Telecharge Python ici : https://www.python.org/downloads/
    echo IMPORTANT : coche "Add Python to PATH" pendant l'installation.
    pause
    exit /b
)
echo [01/04] ✅ Python detecte

:: Installer les dépendances
echo [02/04] 📦 Installation des dependances...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erreur installation dependances
    pause
    exit /b
)
echo [02/04] ✅ Dependances installees

:: Installer Ollama
echo [03/04] 🦙 Installation d'Ollama...
echo.
echo Telecharge Ollama depuis : https://ollama.ai/download
echo Execute l'installateur Windows.
echo.
echo Apres installation, ouvre un terminal et tape :
echo   ollama pull mistral
echo.
echo Puis lance : ollama serve
echo.
pause
echo [03/04] ✅ Ollama installe (si tu l'as fait)

:: Config
echo [04/04] ⚙️ Configuration initiale...
if not exist config.local.json (
    copy config.json config.local.json >nul
)
echo [04/04] ✅ Configuration prete

echo.
echo ╔══════════════════════════════════════════╗
echo ║   ✅ INSTALLATION TERMINEE !             ║
echo ║                                          ║
echo ║   Pour lancer l'agent :                  ║
echo ║     python run.py                       ║
echo ║                                          ║
echo ║   Dashboard : http://localhost:5000     ║
echo ╚══════════════════════════════════════════╝
echo.
pause
