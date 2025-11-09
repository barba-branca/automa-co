@echo off
echo ==========================================================
echo    Script para Gerar o Executavel do RPA Assistente
echo ==========================================================
echo.
echo Verificando se o PyInstaller esta instalado...
pip show pyinstaller > NUL 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
) else (
    echo PyInstaller ja esta instalado.
)

echo.
echo Limpando builds anteriores (pastas build/ e dist/)...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo.
echo Gerando o executavel...
pyinstaller --onefile --noconsole --name RPA_Assistente_Dominio rpa.py

echo.
echo ==========================================================
echo    Processo Concluido!
echo ==========================================================
echo.
echo O arquivo "RPA_Assistente_Dominio.exe" foi criado dentro da pasta "dist".
echo.
pause
