@echo off
echo Instalando dependencias...
python -m pip install streamlit numpy pandas scipy
echo.
echo Iniciando aplicacao...
python -m streamlit run app.py --server.port 8501 --server.address 127.0.0.1
pause