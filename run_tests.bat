@echo off
echo ========================================================
echo Ejecutando Suite de Pruebas Unitarias e Integracion
echo ========================================================
python -m unittest discover -s tests -v
pause
