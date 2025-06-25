@echo off
echo Instalando dependencias...
python -m pip install streamlit numpy pandas scipy
echo.
echo Iniciando aplicacao...
python -m streamlit run app.py
pause