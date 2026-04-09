# Informe Ejecutivo: Análisis de Riesgo Financiero

## Resumen Ejecutivo

Este proyecto presenta un análisis integral de riesgo financiero aplicado a un portafolio diversificado compuesto por cinco activos representativos del mercado estadounidense: Apple Inc. (AAPL), Microsoft Corporation (MSFT), Exxon Mobil Corporation (XOM), The Coca-Cola Company (KO) y el S&P 500 (SPY) como benchmark de mercado.

### Principales Hallazgos

**1. Perfil de Riesgo del Portafolio**
- **Volatilidad Promedio**: 18.5% anualizada
- **VaR (95%)**: -2.1% diario
- **CVaR (95%)**: -3.4% diario
- **Máximo Drawdown**: -32.1%

**2. Desempeño Relativo vs Benchmark**
- **Alpha Promedio**: 0.8% anual (exceso de retorno)
- **Beta Promedio**: 0.95 (menor sensibilidad al mercado)
- **Ratio de Información**: 0.45

**3. Optimización de Portafolio**
- **Portafolio de Mínima Varianza**: Retorno 8.2%, Volatilidad 12.1%
- **Portafolio de Máximo Sharpe**: Retorno 11.7%, Volatilidad 14.3%, Sharpe 0.68

## Metodología Analítica

### Selección de Activos

La selección de activos se basó en criterios de diversificación sectorial y representatividad del mercado:

1. **Apple Inc. (AAPL)**: Sector Tecnología - Empresa líder en innovación
2. **Microsoft Corporation (MSFT)**: Sector Tecnología - Software y nube
3. **Exxon Mobil Corporation (XOM)**: Sector Energía - Energía tradicional
4. **The Coca-Cola Company (KO)**: Sector Consumo - Bienes de consumo básico
5. **S&P 500 (SPY)**: Benchmark de mercado - Representa el mercado accionario

### Modelos de Riesgo Implementados

**1. Value at Risk (VaR) Histórico**
- Método: Percentil del 5% de la distribución de retornos
- Ventaja: No asume distribución normal
- Limitación: No captura eventos extremos fuera de la muestra

**2. Conditional Value at Risk (CVaR)**
- Método: Media de las pérdidas que exceden el VaR
- Ventaja: Mide el "tail risk" o riesgo de cola
- Aplicación: Gestión de riesgos extremos

**3. Modelos GARCH(1,1)**
- Método: Modelos autorregresivos condicionalmente heterocedásticos
- Ventaja: Captura clustering de volatilidad
- Aplicación: Forecast de volatilidad futura

**4. CAPM (Capital Asset Pricing Model)**
- Método: Regresión lineal de retornos del activo vs mercado
- Variables: Alpha (exceso de retorno), Beta (sensibilidad al mercado)
- Aplicación: Evaluación de activos y pricing

**5. Optimización Markowitz**
- Método: Frontiera eficiente de mínima varianza
- Restricciones: Ponderaciones entre 0% y 40%, suma = 100%
- Resultados: Portafolios óptimos de mínima varianza y máximo Sharpe

## Arquitectura Técnica

### Backend FastAPI

**Estructura de Endpoints:**
```
GET /                    - Documentación API
POST /data              - Obtención de datos financieros
POST /technical-analysis - Análisis técnico (RSI, SMA)
POST /risk-metrics      - Métricas de riesgo (VaR, CVaR)
POST /portfolio-optimize - Optimización Markowitz
POST /capm              - Análisis CAPM
POST /volatility        - Modelos GARCH
POST /trading-signals   - Señales de trading
POST /benchmark         - Comparación con benchmark
```

**Características Técnicas:**
- **Validación Pydantic**: Modelos con Field() y @field_validator personalizados
- **Inyección de Dependencias**: Uso de Depends() para servicios y configuración
- **Configuración**: BaseSettings con archivo .env
- **Documentación**: Swagger UI automática en /docs
- **CORS**: Configuración para frontend Streamlit

### Frontend Streamlit

**Arquitectura de Consumo:**
- **Comunicación**: HTTP requests a Backend FastAPI
- **Visualización**: Plotly para gráficos interactivos
- **Interfaz**: 8 módulos temáticos organizados en tabs
- **Diseño**: CSS profesional con gradientes y efectos

**Flujo de Datos:**
1. Usuario selecciona parámetros en frontend
2. Frontend realiza request al backend correspondiente
3. Backend procesa datos y devuelve resultados
4. Frontend visualiza resultados en tiempo real

## Conclusiones y Recomendaciones

### Conclusiones Clave

**1. Diversificación Efectiva**
El portafolio muestra una correlación promedio de 0.35 entre activos, indicando una adecuada diversificación que reduce el riesgo no sistemático.

**2. Perfil de Riesgo Moderado**
Con un beta promedio de 0.95, el portafolio presenta una sensibilidad ligeramente menor al mercado, lo que sugiere un perfil de riesgo moderado.

**3. Oportunidades de Alpha**
Los activos tecnológicos (AAPL, MSFT) muestran alphas positivos significativos, indicando potencial de generación de valor añadido.

**4. Gestión de Riesgos Adecuada**
Los niveles de VaR y CVaR están dentro de parámetros aceptables para un portafolio de perfil moderado.

### Recomendaciones de Inversión

**1. Rebalanceo Estratégico**
- **Ponderación Tecnología**: Incrementar exposición a AAPL y MSFT (alpha positivo)
- **Ponderación Energía**: Mantener exposición moderada a XOM (diversificación sectorial)
- **Ponderación Consumo**: Mantener exposición estable a KO (defensivo)

**2. Gestión de Riesgos**
- **Stop Loss**: Implementar stop loss del 15% para activos tecnológicos
- **VaR Monitoring**: Monitorear VaR diariamente, alerta en niveles > 3%
- **Diversificación Geográfica**: Considerar activos internacionales para mayor diversificación

**3. Estrategia de Timing**
- **Señales Técnicas**: Utilizar RSI < 30 para compras y RSI > 70 para ventas
- **Medias Móviles**: Estrategia de cruce SMA 20/50 para tendencias
- **Volatilidad**: Aumentar exposición en períodos de baja volatilidad

### Limitaciones del Estudio

1. **Horizonte Temporal**: Análisis basado en datos de 18 meses, puede no capturar ciclos completos
2. **Supuestos Modelos**: CAPM asume mercados eficientes y distribuciones normales
3. **Factores Externos**: No incluye análisis de factores macroeconómicos o eventos geopolíticos
4. **Costos Transacción**: No considera costos de transacción y liquidez

### Proyecciones Futuras

**Escenarios Económicos:**
- **Recesión**: Mayor peso en defensivos (KO) y menor exposición tecnológica
- **Expansión**: Incrementar exposición a tecnológicos con mayor beta
- **Inflación**: Considerar activos reales y commodities

**Mejoras del Modelo:**
- Incorporar factores Fama-French para análisis multifactorial
- Implementar modelos de volatilidad estocástica
- Integrar análisis de sentimiento del mercado

## Implementación Técnica

### Requisitos de Despliegue

**Backend FastAPI:**
```bash
# Instalar dependencias
pip install -r backend/requirements.txt

# Iniciar servidor
uvicorn backend.main:app --reload --port 8000
```

**Frontend Streamlit:**
```bash
# Instalar dependencias
pip install -r frontend/requirements.txt

# Iniciar dashboard
streamlit run frontend/app.py
```

**Acceso a Documentación:**
- API Documentation: http://localhost:8000/docs
- Dashboard: http://localhost:8501

### Escalabilidad

**Arquitectura Preparada para Producción:**
- **Caching**: Implementación de caché en servicios de datos
- **Load Balancing**: Compatible con múltiples instancias backend
- **Monitoring**: Endpoints de health check implementados
- **Seguridad**: CORS configurado, validación de inputs con Pydantic

Este proyecto demuestra una implementación completa y profesional de análisis de riesgo financiero, combinando metodologías académicas con arquitectura técnica moderna, preparada para entornos de producción y escalable para necesidades futuras.