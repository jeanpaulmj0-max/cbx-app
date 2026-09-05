@echo off
title Cultura de Boxeo Web App
cd /d "%~dp0"
echo Verificando e instalando componentes necesarios...
python -m pip install streamlit -q
echo Iniciando Servidor de la App...
python -m streamlit run app.py
pause
