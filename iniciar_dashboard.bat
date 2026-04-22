@echo off
chcp 65001 >nul
echo ============================================
echo   INICIANDO DASHBOARD DE RIESGO FINANCIERO
echo ============================================
echo.

REM Establecer la ruta del script actual
set "SCRIPT_DIR=%~dp0"

echo [1/3] Iniciando Backend FastAPI...
start "Backend - FastAPI" cmd /k "cd /d "%SCRIPT_DIR%backend" && echo Backend iniciado en http://localhost:8000 && uvicorn main:app --reload --port 8000"

echo Esperando 3 segundos para que el backend inicie...
timeout /t 3 /nobreak >nul

echo.
echo [2/3] Iniciando Frontend Streamlit...
start "Frontend - Streamlit" cmd /k "cd /d "%SCRIPT_DIR%frontend" && echo Frontend iniciado en http://localhost:8501 && streamlit run app.py --server.port 8501"

echo.
echo [3/3] Abriendo navegador...
timeout /t 5 /nobreak >nul
start http://localhost:8501

echo.
echo ============================================
echo   DASHBOARD INICIADO CORRECTAMENTE
echo ============================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
echo.
echo Para detener el dashboard, cierra las ventanas de CMD.
echo.
pause