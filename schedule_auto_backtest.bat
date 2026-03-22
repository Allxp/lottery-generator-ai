@echo off
REM Script de scheduling para Auto-Backtesting en Windows
REM Programar con Task Scheduler: diario a las 6:00 AM

echo [%DATE% %TIME%] Iniciando Auto-Backtesting...
cd /d "c:\Users\allxp\Downloads\CURSO DESARROLLO CON IA BRAIS SCHOOL\generador de combinaciones loteria"
python auto_backtest.py
if %ERRORLEVEL% EQU 0 (
    echo [%DATE% %TIME%] Auto-Backtesting completado exitosamente
) else (
    echo [%DATE% %TIME%] ERROR en Auto-Backtesting - Codigo: %ERRORLEVEL%
)
echo.