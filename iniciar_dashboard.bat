@echo off
echo ================================================
echo     SISTEMA DE GESTION DE PORTAFOLIO
echo ================================================
echo.
echo Iniciando el sistema...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

REM Verificar si pip está instalado
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip no está instalado
    echo Por favor instala pip
    pause
    exit /b 1
)

echo Instalando dependencias del backend...
cd backend
pip install -r requirements.txt
cd ..

echo Instalando dependencias del frontend...
cd frontend
pip install -r requirements.txt
cd ..

echo.
echo ================================================
echo     INICIANDO BACKEND (FastAPI)
echo ================================================
echo Abriendo backend en: http://localhost:8000
echo Mantén esta ventana abierta mientras uses el sistema
echo.
start "" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ================================================
echo     INICIANDO FRONTEND (Streamlit)
echo ================================================
echo Abriendo dashboard en: http://localhost:8501
echo.
cd frontend
streamlit run app.py