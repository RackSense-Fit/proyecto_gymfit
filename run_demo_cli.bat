@echo off
echo ========================================================
echo Ejecutando Demostracion en Consola (Paradigma Funcional)
echo ========================================================
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python src/main.py
pause
