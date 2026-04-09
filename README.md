# 📊 Dashboard de Riesgo Financiero - Backend FastAPI + Frontend Streamlit

## 🎯 Descripción del Proyecto

Sistema integral de análisis de riesgo financiero con arquitectura Backend-Frontend, implementando modelos avanzados como CAPM, GARCH, Value at Risk (VaR), optimización de portafolio Markowitz, y señales de trading automatizadas. El proyecto combina rigor académico con arquitectura profesional lista para producción.

## 👥 Autores

- **Jhonatan Cañón** - [jhonatancaon1234](https://github.com/jhonatancaon1234)
- **Nombre del Segundo Integrante** - [usuario](https://github.com/usuario)

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │  HTTP   │   Backend       │
│   Streamlit     │◄───────►│   FastAPI       │
│   (Puerto 8501) │         │   (Puerto 8000) │
└─────────────────┘         └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │   Yahoo Finance │
                            │   API           │
                            └─────────────────┘
```

### Estructura del Proyecto

```
PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-/
├── backend/                    # Backend FastAPI
│   ├── __init__.py
│   ├── main.py                # API principal (8 endpoints)
│   ├── models.py              # Modelos Pydantic
│   ├── config.py              # Configuración con BaseSettings
│   ├── requirements.txt       # Dependencias backend
│   └── services/              # Servicios de negocio
│       ├── __init__.py
│       ├── data_service.py    # Servicio de datos
│       └── analysis_service.py # Servicio de análisis
├── frontend/                   # Frontend Streamlit
│   ├── __init__.py
│   ├── app.py                 # Dashboard principal
│   └── requirements.txt       # Dependencias frontend
├── analysis/                   # Módulos de análisis (reutilizados)
│   ├── __init__.py
│   ├── technical_analysis.py
│   ├── returns_analysis.py
│   ├── volatility_models.py
│   ├── capm_analysis.py
│   ├── risk_metrics.py
│   └── portfolio_optimization.py
├── data/                       # Módulos de datos
│   ├── __init__.py
│   ├── data_loader.py
│   └── data_processor.py
├── signals/                    # Sistema de señales
│   ├── __init__.py
│   └── trading_signals.py
├── utils/                      # Utilidades
│   ├── __init__.py
│   └── plotting.py
├── docs/                       # Documentación
│   └── informe_ejecutivo.md   # Informe ejecutivo
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Configuración Git
├── config.py                  # Configuración global
├── requirements.txt           # Dependencias generales
└── README.md                  # Este archivo
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/jhonatancaon1234/PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-.git
cd PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Mac/Linux)
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Instalar dependencias generales
pip install -r requirements.txt

# Instalar dependencias del backend
pip install -r backend/requirements.txt

# Instalar dependencias del frontend
pip install -r frontend/requirements.txt
```

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores (opcional)
# Las configuraciones por defecto funcionan correctamente
```

## 🔧 Configuración de Variables de Entorno

### Variables Requeridas (.env)

```env
# Configuración de la aplicación
APP_NAME="API de Riesgo Financiero"
APP_VERSION="1.0.0"
DEBUG=false

# Configuración de datos financieros
DEFAULT_START_DATE="2024-01-01"
DEFAULT_END_DATE="2026-04-08"
DEFAULT_CONFIDENCE_LEVEL=0.05
RISK_FREE_RATE=0.02

# Parámetros técnicos
SMA_SHORT_WINDOW=20
SMA_LONG_WINDOW=50
RSI_WINDOW=14
GARCH_P=1
GARCH_Q=1

# CORS (permitir frontend)
ALLOWED_ORIGINS=http://localhost:8501,http://localhost:8502
```

### API Keys (Opcional)

El proyecto utiliza Yahoo Finance de forma gratuita. Si deseas usar servicios premium:

```env
# Alpha Vantage (opcional)
ALPHA_VANTAGE_API_KEY=tu_api_key

# Yahoo Finance Premium (opcional)
YAHOO_FINANCE_API_KEY=tu_api_key
```

## 🎮 Ejecución del Proyecto

### 1. Iniciar el Backend FastAPI

```bash
# Desde la raíz del proyecto
uvicorn backend.main:app --reload --port 8000
```

**Verificación:**
- API disponible en: `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 2. Iniciar el Frontend Streamlit (en otra terminal)

```bash
# Asegúrate de que el backend esté corriendo
streamlit run frontend/app.py --server.port 8501
```

**Verificación:**
- Dashboard disponible en: `http://localhost:8501`

### 3. Acceder al Dashboard

1. Abre tu navegador en `http://localhost:8501`
2. Haz clic en "🔄 Cargar Datos" en el sidebar
3. Explora las 8 pestañas del dashboard

## 📡 Documentación de Endpoints (API)

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `POST` | `/data` | Obtener datos financieros |
| `POST` | `/technical-analysis` | Análisis técnico (RSI, SMA) |
| `POST` | `/risk-metrics` | Métricas de riesgo (VaR, CVaR) |
| `POST` | `/portfolio-optimize` | Optimización Markowitz |
| `POST` | `/capm` | Análisis CAPM |
| `POST` | `/volatility` | Modelos GARCH |
| `POST` | `/trading-signals` | Señales de trading |
| `POST` | `/benchmark` | Comparación con benchmark |

### Ejemplo de Uso de API

```bash
# Obtener datos financieros
curl -X POST "http://localhost:8000/data" \
  -H "Content-Type: application/json" \
  -d '{"assets": ["AAPL", "MSFT", "SPY"]}'

# Análisis técnico
curl -X POST "http://localhost:8000/technical-analysis" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "window_sma_short": 20, "window_sma_long": 50}'
```

### Documentación Automática

La API incluye documentación interactiva Swagger UI:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 📊 Activos Seleccionados

### Portafolio Base

| Símbolo | Empresa | Sector | Justificación |
|---------|---------|--------|---------------|
| **AAPL** | Apple Inc. | Tecnología | Líder en innovación, alta capitalización |
| **MSFT** | Microsoft Corporation | Tecnología | Software y cloud computing, estabilidad |
| **XOM** | Exxon Mobil Corporation | Energía | Diversificación sectorial, energía tradicional |
| **KO** | The Coca-Cola Company | Consumo | Bienes de consumo básico, defensivo |
| **SPY** | SPDR S&P 500 ETF Trust | Índice | Benchmark de mercado, referencia |

### Criterios de Selección

1. **Diversificación Sectorial**: Tecnología, Energía, Consumo
2. **Liquidez**: Todos los activos tienen alto volumen diario
3. **Representatividad**: Empresas líderes en sus sectores
4. **Disponibilidad de Datos**: Información histórica completa

## 🛠️ Características Técnicas

### Backend FastAPI

- ✅ **Pydantic Models**: Validación de datos con Field() y @field_validator
- ✅ **Dependency Injection**: Uso de Depends() para servicios
- ✅ **BaseSettings**: Configuración con variables de entorno
- ✅ **CORS**: Configuración para frontend Streamlit
- ✅ **Documentación Automática**: Swagger UI y ReDoc
- ✅ **Manejo de Errores**: Excepciones globales y validación
- ✅ **Caching**: Sistema de caché para optimización

### Frontend Streamlit

- ✅ **Arquitectura Cliente-Servidor**: Consume API REST
- ✅ **8 Módulos Temáticos**: Análisis técnico, rendimientos, volatilidad, CAPM, VaR, Markowitz, señales, benchmark
- ✅ **Visualización Interactiva**: Plotly con gráficos dinámicos
- ✅ **Diseño Profesional**: CSS personalizado con gradientes
- ✅ **Responsive**: Adaptable a diferentes tamaños de pantalla
- ✅ **Navegación Intuitiva**: Tabs y sidebar organizados

### Modelos Financieros Implementados

1. **Análisis Técnico**: RSI, SMA, Bandas de Bollinger
2. **Rendimientos**: Estadísticas descriptivas, distribuciones
3. **Volatilidad**: Modelos GARCH(1,1), volatilidad histórica
4. **CAPM**: Alpha, Beta, R-cuadrado
5. **VaR/CVaR**: Value at Risk histórico y condicional
6. **Markowitz**: Optimización de portafolio, frontera eficiente
7. **Señales**: Sistema combinado SMA-RSI
8. **Benchmark**: Alpha, tracking error, information ratio

## 📋 Uso de Herramientas de IA

Este proyecto fue desarrollado con asistencia de herramientas de IA para:

- **Generación de código**: Estructura base y funciones auxiliares
- **Documentación**: Redacción de comentarios y documentación
- **Optimización**: Sugerencias de mejora de rendimiento
- **Testing**: Generación de casos de prueba

**Nota**: Todo el código fue revisado, validado y adaptado manualmente para cumplir con los requisitos académicos y profesionales del proyecto.

## 🧪 Pruebas y Validación

### Verificación de Instalación

```bash
# Verificar versiones de Python
python --version  # Debe ser 3.8+

# Verificar paquetes instalados
pip list | grep -E "(fastapi|streamlit|pandas|numpy)"

# Verificar conexión a Yahoo Finance
python -c "import yfinance as yf; print(yf.download('AAPL', period='1d'))"
```

### Pruebas del Backend

```bash
# Prueba de health check
curl http://localhost:8000/health

# Prueba de endpoint de datos
curl -X POST "http://localhost:8000/data" \
  -H "Content-Type: application/json" \
  -d '{"assets": ["AAPL"]}'
```

### Pruebas del Frontend

1. Verificar que el backend esté corriendo
2. Acceder a `http://localhost:8501`
3. Hacer clic en "Cargar Datos"
4. Verificar que se muestren gráficos y métricas

## 🐛 Solución de Problemas

### Error: "No module named 'backend'"

```bash
# Asegúrate de estar en la raíz del proyecto
pwd  # Debe mostrar: .../PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-

# Reinstalar paquetes
pip install -r backend/requirements.txt
```

### Error: "Connection refused" en frontend

```bash
# Verificar que el backend esté corriendo
curl http://localhost:8000/health

# Si no responde, iniciar backend
uvicorn backend.main:app --reload --port 8000
```

### Error: "Port already in use"

```bash
# Cambiar puerto del backend
uvicorn backend.main:app --reload --port 8001

# Actualizar frontend/app.py
API_BASE_URL = "http://localhost:8001"
```

### Error: "Yahoo Finance API rate limit"

- Esperar 1-2 minutos entre solicitudes
- Reducir número de activos en análisis
- Usar datos cacheados (ya implementado)

## 📄 Licencia

Este proyecto es de uso académico y personal. Los datos financieros son proporcionados por Yahoo Finance bajo sus términos de servicio.

## 🤝 Contribuciones

Este es un proyecto universitario. Para contribuciones o preguntas:

1. Crear un issue en GitHub
2. Contactar a los autores por email

## 📚 Referencias

### Bibliografía

1. **Hull, J. C. (2018)**: "Risk Management and Financial Institutions"
2. **Tsay, R. S. (2005)**: "Analysis of Financial Time Series"
3. **Markowitz, H. (1952)**: "Portfolio Selection" - Journal of Finance
4. **Sharpe, W. F. (1964)**: "Capital Asset Prices: A Theory of Market Equilibrium"

### Recursos en Línea

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)
- [Plotly Documentation](https://plotly.com/python/)

## 🎓 Notas Académicas

Este proyecto fue desarrollado para la materia de **Análisis de Riesgo Financiero** de la Universidad Santo Tomás, demostrando la aplicación práctica de modelos financieros avanzados con arquitectura de software profesional.

---

**Fecha de última actualización**: Abril 2026
**Versión del proyecto**: 2.0.0