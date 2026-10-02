@echo off
echo ========================================================
echo Iniciando Servidor GymFit Agent con Recarga Automatica
echo ========================================================
python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
pause
