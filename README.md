# 📈 Sistema de Gestión de Portafolio

Sistema profesional para análisis de riesgo financiero y gestión de portafolios con modelos avanzados (CAPM, GARCH, VaR, Markowitz).

## 🚀 **Instrucciones de Uso**

### **1. Iniciar el Backend (FastAPI)**

Abre una terminal y ejecuta:

```bash
cd backend
uvicorn main:app --reload
```

El servidor se iniciará en `http://localhost:8000`

### **2. Iniciar el Frontend (Streamlit)**

Abre **otra terminal** y ejecuta:

```bash
cd frontend
streamlit run app.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`

### **3. Usar el Dashboard**

1. En el sidebar, selecciona los activos que deseas analizar
2. Elige el período de análisis (6 meses, 1 año, 2 años, 5 años)
3. Ajusta el nivel de confianza para VaR si lo deseas
4. Haz clic en **"🔄 Cargar Datos"**
5. Explora las 8 pestañas del dashboard

## 📋 **Endpoints Disponibles**

- `POST /data` - Obtener datos financieros
- `POST /technical-analysis` - Análisis técnico (SMA, RSI)
- `POST /risk-metrics` - Métricas de riesgo (VaR, CVaR)
- `POST /portfolio-optimize` - Optimización de portafolio (Markowitz)
- `POST /capm` - Análisis CAPM
- `POST /volatility` - Análisis de volatilidad (GARCH)
- `POST /trading-signals` - Señales de trading
- `POST /benchmark` - Comparación con benchmark

## 🎯 **Características Principales**

- ✅ **Fechas dinámicas** - Se actualizan automáticamente
- ✅ **Manejo robusto de errores** - Sistema tolerante a fallos
- ✅ **Soporte MultiIndex** - Compatible con yfinance moderno
- ✅ **Interfaz profesional** - Diseño claro y moderno
- ✅ **8 paneles de análisis** - Cobertura completa de métricas

## 🛠️ **Tecnologías Utilizadas**

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Datos**: Yahoo Finance (yfinance)
- **Análisis**: pandas, numpy, scipy, statsmodels, arch
- **Visualización**: Plotly

## 📊 **Activos Soportados**

- AAPL (Apple)
- MSFT (Microsoft)
- XOM (Exxon Mobil)
- KO (Coca-Cola)
- SPY (S&P 500 ETF)

## 🔧 **Requisitos**

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

## 📝 **Notas Importantes**

1. Asegúrate de tener conexión a internet para descargar datos de Yahoo Finance
2. El backend debe estar corriendo antes de iniciar el frontend
3. Los datos se almacenan en caché para mejorar el rendimiento

## 🎓 **Propósito Académico**

Este proyecto fue desarrollado para la Universidad Santo Tomas como parte del curso de análisis de riesgo financiero con portafolio.

## 📧 **Soporte**

Para problemas o preguntas, por favor revisa los logs del backend para ver errores detallados.