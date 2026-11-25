@echo off
echo ========================================================
echo Ejecutando Suite de Pruebas Unitarias e Integracion
echo ========================================================
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python -m pytest -v
pause
