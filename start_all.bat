@echo off
cd /d %~dp0
title 🚀 FRAUD DETECTOR CM
color 0A

echo ========================================
echo    🚀 FRAUD DETECTOR - BANQUE CAMEROUN
echo ========================================
echo.

REM Active venv
call venv\Scripts\activate

REM Installe dépendances
echo [1/5] 📦 Installation...
pip install -r requirements.txt --quiet

REM Télécharge données si besoin
if not exist data\creditcard.csv (
    echo [2/5] 📊 Téléchargement données...
    mkdir data
    powershell -Command "Invoke-WebRequest -Uri 'https://files.catbox.moe/2l4p0j.csv' -OutFile 'data\creditcard.csv'"
)

REM Entraîne modèle
echo [3/5] 🧠 Entraînement IA...
if not exist fraud_app\ml\model.xgb (
    python fraud_app/ml/train.py
) else (
    echo    ✅ Modèle déjà prêt
)

REM Migrations DB
echo [4/5] 🗄️ Base de données...
python manage.py migrate

REM Lance serveur
echo [5/5] 🌐 Démarrage serveur...
start "" "Interface" http://127.0.0.1:8000
python manage.py runserver

echo.
echo ✅ ✅ ✅ FRAUD DETECTOR ACTIF ✅ ✅ ✅
echo 👉 Interface: http://127.0.0.1:8000
echo 👉 Admin:    http://127.0.0.1:8000/admin
echo.
pause