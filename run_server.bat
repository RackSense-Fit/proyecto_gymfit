@echo off
echo ========================================================
echo Iniciando Servidor GymFit Agent con Recarga Automatica
echo ========================================================
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
pause
