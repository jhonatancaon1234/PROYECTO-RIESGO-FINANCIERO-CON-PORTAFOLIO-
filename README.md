# 📊 Dashboard de Análisis de Riesgo Financiero con Portafolio

## 🎯 Descripción del Proyecto

Este proyecto implementa un dashboard interactivo para el análisis de riesgo financiero de un portafolio diversificado compuesto por 5 activos:

- **Apple Inc. (AAPL)** - Tecnología
- **Microsoft Corporation (MSFT)** - Tecnología  
- **Exxon Mobil Corporation (XOM)** - Energía
- **The Coca-Cola Company (KO)** - Consumo
- **SPDR S&P 500 ETF Trust (SPY)** - Benchmark del mercado

## 🧠 Justificación de la Selección de Activos

La selección de estos activos responde a una estrategia de **diversificación sectorial**:

- **Tecnología**: Apple y Microsoft representan el sector tecnológico, caracterizado por alto crecimiento pero mayor volatilidad
- **Energía**: Exxon Mobil proporciona exposición al sector energético, sensible a ciclos económicos y precios de commodities
- **Consumo**: Coca-Cola ofrece estabilidad a través del consumo básico, considerado defensivo
- **Benchmark**: SPY (S&P 500 ETF) sirve como referencia de mercado para comparar el performance del portafolio

Esta combinación permite analizar diferentes perfiles de riesgo y correlaciones entre sectores.

## 🏗️ Arquitectura del Proyecto

```
PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-/
├── README.md                    # Documentación del proyecto
├── requirements.txt             # Dependencias Python
├── main.py                      # Aplicación Streamlit principal
├── config.py                    # Configuración y constantes
├── data/                        # Módulos de datos
│   ├── __init__.py
│   ├── data_loader.py          # Carga de datos de Yahoo Finance
│   └── data_processor.py       # Procesamiento de datos
├── analysis/                    # Módulos de análisis financiero
│   ├── __init__.py
│   ├── technical_analysis.py   # Análisis técnico (RSI, MACD, medias)
│   ├── returns_analysis.py     # Análisis de rendimientos
│   ├── volatility_models.py    # Modelos ARCH/GARCH
│   ├── capm_analysis.py        # Modelo CAPM
│   ├── risk_metrics.py         # VaR y CVaR
│   └── portfolio_optimization.py # Optimización Markowitz
├── signals/                     # Sistema de señales de trading
│   ├── __init__.py
│   └── trading_signals.py      # Señales automáticas
└── utils/                       # Utilidades
    ├── __init__.py
    └── plotting.py             # Funciones de visualización
```

## 🔧 Tecnologías Utilizadas

### Principal
- **Streamlit** - Dashboard interactivo web
- **yfinance** - API de Yahoo Finance para datos en tiempo real

### Análisis de Datos
- **pandas** - Manipulación y análisis de datos
- **numpy** - Cálculos numéricos
- **scipy** - Estadísticas avanzadas

### Visualización
- **plotly** - Gráficos interactivos
- **matplotlib/seaborn** - Gráficos estáticos

### Modelos Financieros
- **arch** - Modelos ARCH/GARCH para volatilidad
- **statsmodels** - Regresiones y análisis estadístico
- **scikit-learn** - Optimización y machine learning

## 📈 Módulos de Análisis

### 🔹 1. Análisis Técnico
**Objetivo**: Entender tendencias y señales de compra/venta

**Indicadores implementados**:
- **Promedios Móviles**: SMA 20 y 50 para identificar tendencias
- **RSI (Relative Strength Index)**: Identificar sobrecompra (>70) y sobreventa (<30)
- **MACD**: Momentum y cruces de tendencia
- **Bandas de Bollinger**: Volatilidad y niveles de soporte/resistencia

**Interpretación**:
- Cruces de medias: Señales de cambio de tendencia
- RSI: Condiciones extremas de precio
- MACD: Momentum del precio

### 🔹 2. Análisis de Rendimientos
**Objetivo**: Comprender el comportamiento estadístico de los retornos

**Métricas calculadas**:
- Media, desviación estándar, varianza
- Asimetría (skewness) y curtosis (kurtosis)
- Pruebas de normalidad (Jarque-Bera, Shapiro-Wilk)
- Drawdown máximo y tiempo de recuperación

**Hallazgos clave**:
- Los rendimientos no siguen distribución normal (colas pesadas)
- Presencia de asimetría y curtosis alta
- Patrones de volatilidad clustering

### 🔹 3. Modelos ARCH/GARCH
**Objetivo**: Modelar la volatilidad condicional y heterocedástica

**Modelos implementados**:
- **ARCH(1)**: Modela efectos de choques pasados en volatilidad
- **GARCH(1,1)**: Combina efectos de choques y volatilidad pasada
- Comparación de modelos mediante AIC/BIC

**Aplicaciones**:
- Pronóstico de volatilidad futura
- Mejor comprensión de patrones de riesgo
- Input para cálculo de VaR avanzado

### 🔹 4. CAPM (Capital Asset Pricing Model)
**Objetivo**: Medir el riesgo sistemático y retorno esperado

**Cálculos realizados**:
- **Beta**: Sensibilidad de cada activo al mercado (SPY)
- **Alpha**: Exceso de retorno no explicado por el mercado
- **R²**: Proporción de varianza explicada por el mercado
- **Ratio de Treynor**: Retorno ajustado por riesgo sistemático

**Clasificación de riesgo**:
- **Beta > 1.2**: Alto riesgo (cíclico)
- **Beta 1.0-1.2**: Riesgo moderado
- **Beta 0.8-1.0**: Riesgo bajo
- **Beta < 0.8**: Defensivo

### 🔹 5. VaR y CVaR
**Objetivo**: Cuantificar la pérdida máxima esperada en escenarios extremos

**Métodos implementados**:
- **VaR Histórico**: Percentil del nivel de confianza
- **VaR Paramétrico**: Asumiendo distribución normal
- **VaR GARCH**: Incorporando volatilidad condicional
- **CVaR (Expected Shortfall)**: Pérdida promedio en colas extremas

**Interpretación**:
- "Con 95% de confianza, la pérdida diaria no superará X%"
- CVaR proporciona visión más conservadora del riesgo extremo

### 🔹 6. Optimización Markowitz
**Objetivo**: Encontrar portafolios óptimos según relación riesgo-retorno

**Portafolios calculados**:
- **Mínima Varianza**: Menor riesgo posible
- **Máximo Sharpe**: Mejor retorno ajustado por riesgo
- **Pesos Iguales**: Benchmark simple
- **Paridad de Riesgo**: Igual contribución al riesgo

**Métricas de diversificación**:
- Índice de Herfindahl-Hirschman (HHI)
- Número efectivo de activos
- Concentración máxima

### 🔹 7. Señales Automáticas ⭐
**Objetivo**: Sistema de trading basado en indicadores técnicos

**Señales generadas**:
- **SMA**: Cruce de medias móviles (20/50)
- **RSI**: Condiciones de sobrecompra/sobreventa
- **MACD**: Cruce de línea MACD y señal
- **Señal Combinada**: Integración de múltiples indicadores

**Clasificación**:
- **Fuerte Compra/Venta**: Score > 0.66
- **Compra/Venta**: Score 0.33-0.66
- **Mantener**: Score -0.33 a 0.33

### 🔹 8. Contexto Macro y Benchmark ⭐
**Objetivo**: Comparar performance del portafolio vs mercado

**Métricas de comparación**:
- **Retorno Total**: Performance absoluta
- **Sharpe Ratio**: Retorno ajustado por riesgo total
- **Sortino Ratio**: Retorno ajustado por riesgo a la baja
- **Alpha**: Exceso de retorno vs benchmark
- **Information Ratio**: Consistencia del alpha

**Análisis de correlación**:
- Relación con el mercado (beta)
- Diversificación entre sectores
- Ciclos económicos y sensibilidad sectorial

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Conexión a internet para descargar datos de Yahoo Finance

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Ejecución del Dashboard
```bash
streamlit run main.py
```

### Acceso al Dashboard
El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Interfaz del Dashboard

### Configuración (Sidebar)
- Selección de activos para análisis
- Período de análisis (6 meses a 5 años)
- Nivel de confianza para VaR (1%-10%)

### Pestañas de Análisis
1. **🔍 Análisis Técnico**: Gráficos de precios e indicadores
2. **📊 Rendimientos**: Distribuciones y correlaciones
3. **📈 Volatilidad**: Modelos GARCH y volatilidad histórica
4. **🎯 CAPM**: Betas y análisis de riesgo sistemático
5. **⚠️ VaR & CVaR**: Métricas de riesgo extremo
6. **⚖️ Markowitz**: Optimización de portafolios
7. **🎯 Señales**: Sistema de trading automático
8. **🏆 Benchmark**: Comparación con mercado

## 🎓 Interpretación Económica

### Diversificación
La combinación de sectores diferentes reduce el riesgo no sistemático:
- **Tecnología**: Alto crecimiento, alta volatilidad
- **Energía**: Cíclico, correlación con commodities
- **Consumo**: Defensivo, menor volatilidad
- **Benchmark**: Referencia de mercado

### Riesgo Sistemico vs Específico
- **Sistemico**: No diversificable, medido por beta
- **Específico**: Diversificable mediante portafolio
- **Optimización**: Busca equilibrio entre ambos

### Gestión de Riesgo
- **VaR**: Límite de pérdida esperada
- **CVaR**: Gestión de colas extremas
- **Diversificación**: Reducción de riesgo no sistemático

## 📈 Aplicaciones Prácticas

### Para Inversionistas
- **Selección de activos**: Basado en perfil de riesgo
- **Timing de mercado**: Señales técnicas de entrada/salida
- **Gestión de riesgo**: Límites de VaR y diversificación

### Para Gestores de Portafolios
- **Optimización**: Portafolios eficientes según Markowitz
- **Benchmarking**: Comparación vs mercado
- **Reportes de riesgo**: Métricas regulatorias y de gestión

### Para Analistas Financieros
- **Modelos de volatilidad**: Pronósticos GARCH
- **Valuación**: CAPM para costos de capital
- **Backtesting**: Validación de estrategias

## 🔬 Metodología

### Fuentes de Datos
- **Yahoo Finance**: Precios diarios de cierre ajustado
- **Frecuencia**: Diaria (días hábiles)
- **Horizonte**: Configurable por el usuario

### Supuestos del Modelo
- **Mercados eficientes**: Precios reflejan toda información disponible
- **Normalidad condicional**: Para algunos cálculos paramétricos
- **Estacionariedad**: Series temporales estacionarias en media y varianza

### Limitaciones
- **Datos históricos**: No garantizan performance futura
- **Supuestos de normalidad**: Rendimientos financieros suelen tener colas pesadas
- **Costos de transacción**: No incluidos en el análisis
- **Impuestos**: No considerados en cálculos de retorno

## 📚 Referencias y Bibliografía

### Modelos Financieros
- Markowitz, H. (1952). "Portfolio Selection"
- Sharpe, W. (1964). "Capital Asset Prices"
- Engle, R. (1982). "Autoregressive Conditional Heteroscedasticity"
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity"

### Risk Management
- Jorion, P. (2006). "Value at Risk"
- McNeil, A.J., Frey, R., Embrechts, P. (2015). "Quantitative Risk Management"

### Technical Analysis
- Murphy, J.J. (1999). "Technical Analysis of the Financial Markets"
- Pring, M.J. (2002). "Technical Analysis Explained"

## 🤝 Contribución

Este proyecto está diseñado para ser educativo y de código abierto. Se agradecen contribuciones que mejoren:

- Nuevos indicadores técnicos
- Modelos de riesgo avanzados
- Mejoras en la interfaz de usuario
- Documentación y ejemplos

## 📄 Licencia

Este proyecto es de uso educativo y académico. Se permite su uso, modificación y distribución con fines de aprendizaje.

## 🙏 Agradecimientos

- **Yahoo Finance**: Por proporcionar datos financieros gratuitos
- **Comunidad Python**: Por desarrollar las excelentes librerías utilizadas
- **Academia financiera**: Por el desarrollo de las teorías y modelos implementados

---

**Nota**: Este proyecto tiene como objetivo principal la educación y comprensión de conceptos de análisis de riesgo financiero. No constituye asesoría de inversión y las decisiones financieras deben basarse en análisis más completos y profesionales.