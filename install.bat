@echo off
echo ==========================================================
echo    Instalador de Dependencias para o RPA Assistente
echo ==========================================================
echo.
echo Este script ira instalar todas as bibliotecas Python necessarias.
echo Certifique-se de que voce tem Python instalado e adicionado ao PATH.
echo.
pause

echo Instalando dependencias a partir de requirements.txt...
pip install -r requirements.txt

echo.
echo ==========================================================
echo    Instalacao Concluida!
echo ==========================================================
echo.
echo Voce ja pode configurar o arquivo 'config.json' e depois
echo executar o 'build.bat' para criar o programa.
echo.
pause
