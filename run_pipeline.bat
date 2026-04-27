@echo off

:: Entrando na pasta principal
cd /d %~dp0\desafio-etl-main

echo.
echo Executando ETL...
python run_etl.py

echo.
echo  Iniciando API...
start cmd /k "cd /d %cd% && python run_api.py"

:: Um pequeno aguardo para a API subir
timeout /t 2 >nul

echo.
echo Iniciando servidor web...
start cmd /k "cd /d %cd%\web && python -m http.server 5500"

echo.
echo Pipeline rodando!
echo.
echo API: http://127.0.0.1:8000
echo.
echo Frontend: http://127.0.0.1:5500
echo.
echo Para acessar o site, digite: http://127.0.0.1:5500 no navegador
echo.
echo Para acessar os dados coletados digite: http://127.0.0.1:8000/dados no navegador
echo.


pause