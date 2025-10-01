@echo off
echo ========================================
echo   Sonhos Lusíadas - Sistema de Análise
echo ========================================
echo.

echo Iniciando backend...
cd ..\sonhos-lusiadas-backend
start cmd /k "python src\main.py"
timeout /t 3 /nobreak > nul

echo.
echo Iniciando frontend...
cd ..\sonhos-lusiadas-app
start cmd /k "npm run dev"
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo   Sistema iniciado com sucesso!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Pressione qualquer tecla para fechar...
pause > nul
