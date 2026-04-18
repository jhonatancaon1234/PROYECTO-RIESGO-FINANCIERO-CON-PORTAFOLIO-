# DOCUMENTACIÓN COMPLETA - SISTEMA PROFESIONAL DE GESTIÓN DE PORTAFOLIO

## 📋 RESUMEN EJECUTIVO DEL TRABAJO REALIZADO

### 🎯 **Objetivo del Proyecto**
Desarrollar un sistema profesional de análisis de riesgo financiero y optimización de portafolios que integre:
- Backend robusto con FastAPI
- Frontend interactivo con Streamlit
- Análisis técnico, fundamental y de riesgo
- Optimización moderna de portafolios (Markowitz)
- Sistema de señales de trading automatizadas

---

## 🏗️ **ARQUITECTURA DEL SISTEMA**

### **Estructura de Carpetas**
```
PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-/
├── backend/              # API REST con FastAPI
│   ├── services/        # Lógica de negocio
│   ├── main.py          # Punto de entrada
│   ├── models.py        # Modelos de datos
│   └── config.py        # Configuración
├── frontend/            # Dashboard Streamlit
│   └── app.py          # Interfaz de usuario
├── analysis/           # Módulos de análisis financiero
│   ├── technical_analysis.py    # Indicadores técnicos
│   ├── risk_metrics.py          # VaR, CVaR
│   ├── capm_analysis.py         # Modelo CAPM
│   ├── portfolio_optimization.py # Markowitz
│   ├── volatility_models.py     # GARCH, volatilidad
│   └── returns_analysis.py      # Estadísticas de retornos
├── data/               # Gestión de datos
│   ├── data_loader.py  # Carga desde Yahoo Finance
│   └── data_processor.py # Limpieza y transformación
├── signals/            # Sistema de señales
│   └── trading_signals.py # Generación de señales
├── utils/              # Utilidades
│   └── plotting.py     # Funciones de visualización
└── docs/               # Documentación
    └── informe_ejecutivo.md
```

---

## 🔧 **FUNCIONES PRINCIPALES Y SU UTILIDAD**

### **1. MÓDULO DE ANÁLISIS TÉCNICO** (`analysis/technical_analysis.py`)

#### **Funciones Implementadas:**
```python
def calculate_sma(prices, window)
def calculate_rsi(prices, window)
def get_technical_indicators(symbol, prices)
```

#### **¿Para qué sirvieron?**
- **SMA (Simple Moving Average)**: Identificar tendencias del mercado
  - SMA 20: Tendencia a corto plazo (1 mes)
  - SMA 50: Tendencia a mediano plazo (2 meses)
  - Cruces: Señales de compra/venta

- **RSI (Relative Strength Index)**: Medir sobrecompra/sobreventa
  - RSI > 70: Activo sobrecomprado (posible venta)
  - RSI < 30: Activo sobrevendido (posible compra)
  - RSI 30-70: Zona neutral

#### **Código Explicado:**
```python
# Cálculo del RSI paso a paso
delta = prices.diff()  # Cambio diario
gain = delta.where(delta > 0, 0)  # Solo ganancias
loss = -delta.where(delta < 0, 0)  # Solo pérdidas
rs = gain.rolling(window).mean() / loss.rolling(window).mean()
rsi = 100 - (100 / (1 + rs))
```

---

### **2. MÓDULO DE MÉTRICAS DE RIESGO** (`analysis/risk_metrics.py`)

#### **Funciones Implementadas:**
```python
def calculate_var(returns, confidence_level)
def calculate_cvar(returns, confidence_level)
def historical_var(returns, confidence_level)
def parametric_var(returns, confidence_level)
```

#### **¿Para qué sirvieron?**
- **VaR (Value at Risk)**: Máxima pérdida esperada en un día "normal"
  - Ejemplo: VaR = 0.03 (3%) con 95% confianza
  - Interpretación: Hay 95% de probabilidad de NO perder más del 3% en un día
  - Si inviertes $10,000 → Pérdida máxima esperada: $300

- **CVaR (Conditional VaR)**: Pérdida esperada en los PEORES días
  - Ejemplo: CVaR = 0.05 (5%)
  - Interpretación: En el 5% de los peores días, la pérdida promedio es 5%
  - Más conservador que el VaR

#### **Código Explicado:**
```python
# VaR Histórico (método no paramétrico)
def historical_var(returns, confidence_level):
    # Ordena los retornos de menor a mayor
    sorted_returns = np.sort(returns)
    # Toma el percentil correspondiente
    var_index = int((1 - confidence_level) * len(sorted_returns))
    return -sorted_returns[var_index]

# CVaR: Promedio de las peores pérdidas
def calculate_cvar(returns, confidence_level):
    var = calculate_var(returns, confidence_level)
    # Promedio de todos los retornos peores que el VaR
    cvar = -returns[returns <= -var].mean()
    return cvar
```

---

### **3. MÓDULO CAPM** (`analysis/capm_analysis.py`)

#### **Funciones Implementadas:**
```python
def calculate_beta(asset_returns, market_returns)
def calculate_alpha(asset_returns, market_returns, beta)
def capm_analysis(assets, market_symbol)
```

#### **¿Para qué sirvieron?**
- **Beta (β)**: Mide el riesgo sistemático (del mercado)
  - β = 1: Se mueve igual que el mercado
  - β > 1: Más volátil que el mercado (amplifica movimientos)
  - β < 1: Menos volátil que el mercado (amortigua movimientos)

- **Alpha (α)**: Valor agregado del activo
  - α > 0: El activo supera al mercado (¡Excelente!)
  - α < 0: El activo bajo desempeño vs el mercado

- **R-cuadrado (R²)**: Confiabilidad de la beta
  - R² > 0.7: Beta confiable
  - R² < 0.5: Beta poco confiable

#### **Código Explicado:**
```python
# Regresión lineal para calcular Beta
from scipy import stats

def calculate_beta(asset_returns, market_returns):
    # Alinea los datos por fecha
    aligned = pd.DataFrame({
        'asset': asset_returns,
        'market': market_returns
    }).dropna()
    
    # Regresión: asset = alpha + beta * market + error
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        aligned['market'], 
        aligned['asset']
    )
    
    return {
        'beta': slope,           # Pendiente = Beta
        'alpha': intercept,      # Intercepto = Alpha
        'r_squared': r_value**2  # R-cuadrado
    }
```

---

### **4. MÓDULO DE OPTIMIZACIÓN DE PORTAFOLIO** (`analysis/portfolio_optimization.py`)

#### **Funciones Implementadas:**
```python
def portfolio_return(weights, mean_returns)
def portfolio_volatility(weights, cov_matrix)
def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate)
def optimize_min_variance(mean_returns, cov_matrix)
def optimize_max_sharpe(mean_returns, cov_matrix, risk_free_rate)
```

#### **¿Para qué sirvieron?**
- **Portafolio de Mínima Varianza**: El más SEGURO posible
  - Minimiza el riesgo mediante diversificación inteligente
  - Combina activos que no se mueven juntos
  - Ideal para inversores conservadores

- **Portafolio de Máximo Sharpe**: El más EFICIENTE posible
  - Máximo retorno por cada unidad de riesgo
  - Es el portafolio "óptimo" en la frontera eficiente
  - Sharpe Ratio > 2: Excelente | 1-2: Bueno | < 1: Regular

#### **Código Explicado:**
```python
from scipy.optimize import minimize

def optimize_max_sharpe(mean_returns, cov_matrix, risk_free_rate):
    n_assets = len(mean_returns)
    
    # Función objetivo: minimizar -Sharpe Ratio (negativo para minimizar)
    def neg_sharpe(weights):
        port_return = np.sum(mean_returns * weights) * 252
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)) * 252)
        return -(port_return - risk_free_rate) / port_vol
    
    # Restricciones: suma de pesos = 1, pesos >= 0
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))
    
    # Optimización
    result = minimize(neg_sharpe, 
                     x0=np.array([1/n_assets]*n_assets),
                     method='SLSQP',
                     bounds=bounds,
                     constraints=constraints)
    
    return result.x  # Pesos óptimos
```

---

### **5. MÓDULO DE VOLATILIDAD** (`analysis/volatility_models.py`)

#### **Funciones Implementadas:**
```python
def historical_volatility(returns, window)
def garch_volatility(returns)
def volatility_forecast(returns, horizon)
```

#### **¿Para qué sirvieron?**
- **Volatilidad Histórica**: Variabilidad pasada del precio
  - Volatilidad anualizada = std(retornos) × √252
  - 20% volatilidad = precio puede variar ±20% en un año

- **Modelo GARCH**: Predice volatilidad futura
  - Considera clusters de volatilidad (períodos tranquilos/inestables)
  - Mejor que solo usar promedio histórico

#### **Código Explicado:**
```python
import arch  # Package para modelos GARCH

def garch_volatility(returns):
    # Modelo GARCH(1,1): 
    # σ²(t) = ω + α × ε²(t-1) + β × σ²(t-1)
    model = arch.arch_model(returns, 
                           mean='Constant', 
                           vol='GARCH', 
                           p=1, q=1)
    
    fitted = model.fit(disp='off')
    
    # Volatilidad actual predicha
    current_vol = fitted.conditional_volatility.iloc[-1]
    
    return current_vol
```

---

### **6. MÓDULO DE SEÑALES DE TRADING** (`signals/trading_signals.py`)

#### **Funciones Implementadas:**
```python
def generate_buy_signal(prices, sma_short, sma_long, rsi)
def generate_sell_signal(prices, sma_short, sma_long, rsi)
def combined_strategy(prices, strategy='combined')
```

#### **¿Para qué sirvieron?**
- **Estrategia Combinada**: Señales más confiables
  - COMPRA: SMA 20 > SMA 50 Y RSI < 30
  - VENTA: SMA 20 < SMA 50 Y RSI > 70
  - Ambas condiciones deben cumplirse simultáneamente

- **Ventaja**: Filtra señales falsas
  - Solo SMA: Muchas señales falsas
  - Solo RSI: Muchas señales en tendencia fuerte
  - Combinado: Señales más selectivas y confiables

#### **Código Explicado:**
```python
def combined_strategy(prices, window_sma_short=20, window_sma_long=50, window_rsi=14):
    # Calcular indicadores
    sma_short = prices.rolling(window_sma_short).mean()
    sma_long = prices.rolling(window_sma_long).mean()
    rsi = calculate_rsi(prices, window_rsi)
    
    signals = []
    for i in range(len(prices)):
        # Señal de COMPRA
        if (sma_short.iloc[i] > sma_long.iloc[i] and 
            rsi.iloc[i] < 30):
            signals.append('BUY')
        # Señal de VENTA
        elif (sma_short.iloc[i] < sma_long.iloc[i] and 
              rsi.iloc[i] > 70):
            signals.append('SELL')
        else:
            signals.append('HOLD')
    
    return signals
```

---

## 📊 **TEORÍA DE RIESGO FINANCIERO**

### **1. CONCEPTOS FUNDAMENTALES**

#### **¿Qué es el Riesgo Financiero?**
- **Definición**: Posibilidad de perder dinero en una inversión
- **Fuentes**: Mercado, crédito, liquidez, operacional
- **Medición**: Volatilidad, VaR, CVaR, Beta

#### **Tipos de Riesgo:**
1. **Riesgo Sistemático (Mercado)**: No diversificable
   - Guerras, crisis económicas, pandemias
   - Medido por Beta (β)

2. **Riesgo No Sistemático (Específico)**: Diversificable
   - Problemas de una empresa específica
   - Se reduce con diversificación

---

### **2. VALUE AT RISK (VaR)**

#### **Definición Formal:**
"El VaR es la pérdida máxima esperada en un horizonte de tiempo dado, con un nivel de confianza específico, bajo condiciones normales de mercado."

#### **Fórmula:**
```
VaR(α) = -inf{ x : P(Loss ≤ x) ≥ α }
```
Donde α es el nivel de confianza (ej: 95%)

#### **Métodos de Cálculo:**

**1. Método Histórico:**
```python
# Ordena retornos históricos
# Toma el percentil (1-α)
VaR = -percentil(retornos, 5%)  # Para 95% confianza
```
- **Ventaja**: No asume distribución
- **Desventaja**: Asume que el pasado se repite

**2. Método Paramétrico (Normal):**
```python
VaR = μ - z_α × σ
```
Donde:
- μ = retorno promedio
- z_α = valor crítico (1.645 para 95%, 2.326 para 99%)
- σ = volatilidad

- **Ventaja**: Simple y rápido
- **Desventaja**: Asume normalidad (los mercados tienen "fat tails")

**3. Simulación Monte Carlo:**
```python
# Genera miles de escenarios aleatorios
# Calcula pérdidas en cada escenario
# Toma el percentil
```
- **Ventaja**: Flexible, captura no-linealidades
- **Desventaja**: Computacionalmente intensivo

#### **Limitaciones del VaR:**
1. **No dice qué pasa en los peores casos**: Solo da un límite
2. **No es coherente**: No cumple subaditividad
3. **Puede subestimar riesgo en crisis**: Las colas son más gruesas

---

### **3. CONDITIONAL VaR (CVaR)**

#### **Definición:**
"El CVaR es la pérdida esperada, dado que la pérdida excede el VaR."

#### **Fórmula:**
```
CVaR(α) = E[Loss | Loss > VaR(α)]
```

#### **Interpretación:**
- **VaR**: "¿Cuánto puedo perder en un día NORMAL?"
- **CVaR**: "¿Cuánto pierdo en los DÍAS PEORES?"

#### **Ejemplo Práctico:**
```
Portafolio de $1,000,000
VaR (95%) = $30,000 (3%)
CVaR (95%) = $50,000 (5%)

Interpretación:
- 95% de los días: pérdida ≤ $30,000
- 5% de los peores días: pérdida promedio = $50,000
```

#### **Ventajas sobre VaR:**
1. **Coherente**: Cumple todas las propiedades de una medida de riesgo
2. **Considera colas**: Captura el riesgo extremo
3. **Más conservador**: Mejor para gestión de riesgo

---

### **4. MODELO CAPM (Capital Asset Pricing Model)**

#### **Fórmula:**
```
E(R_i) = R_f + β_i × [E(R_m) - R_f]
```

Donde:
- E(R_i) = Retorno esperado del activo i
- R_f = Tasa libre de riesgo
- β_i = Beta del activo i
- E(R_m) = Retorno esperado del mercado
- [E(R_m) - R_f] = Prima de riesgo de mercado

#### **Interpretación:**
- **Beta (β)**: Sensibilidad del activo al mercado
  - β = 1.2 → Si mercado sube 10%, activo sube 12%
  - β = 0.8 → Si mercado sube 10%, activo sube 8%

- **Alpha (α)**: Retorno "extra" no explicado por el mercado
  - α > 0 → El activo supera al mercado (¡buen gestor!)
  - α < 0 → El activo bajo desempeño

#### **Supuestos del CAPM:**
1. Mercados eficientes
2. Inversionistas racionales
3. No hay impuestos ni costos de transacción
4. Todos tienen las mismas expectativas
5. Se puede prestar/prestar a tasa libre de riesgo

#### **Críticas:**
- Los mercados no son perfectamente eficientes
- Las betas cambian con el tiempo
- No captura todos los factores de riesgo

---

### **5. TEORÍA MODERNA DE PORTAFOLIO (Markowitz)**

#### **Idea Central:**
"No pongas todos los huevos en la misma canasta" - La diversificación reduce el riesgo sin sacrificar retorno.

#### **Fórmula de Retorno de Portafolio:**
```
E(R_p) = Σ w_i × E(R_i)
```

#### **Fórmula de Riesgo (Varianza):**
```
σ²_p = Σ Σ w_i × w_j × σ_i × σ_j × ρ_ij
```

Donde:
- w_i = peso del activo i
- σ_i = volatilidad del activo i
- ρ_ij = correlación entre activos i y j

#### **Punto Clave:**
- Si ρ_ij < 1 → Hay beneficio de diversificación
- Si ρ_ij = -1 → Máximo beneficio (se anulan riesgos)

#### **Frontera Eficiente:**
- Conjunto de portafolios que maximizan retorno para cada nivel de riesgo
- **Portafolio de Mínima Varianza**: El menos riesgoso
- **Portafolio de Máximo Sharpe**: El más eficiente

#### **Sharpe Ratio:**
```
Sharpe = [E(R_p) - R_f] / σ_p
```
- Mide retorno excedente por unidad de riesgo
- > 2: Excelente | 1-2: Bueno | < 1: Regular

---

### **6. VOLATILIDAD Y MODELOS GARCH**

#### **Volatilidad:**
- **Definición**: Desviación estándar de los retornos
- **Anualizada**: σ_anual = σ_diario × √252
- **Interpretación**: 20% volatilidad = precio puede variar ±20% en un año

#### **Estilizados de Volatilidad:**
1. **Clustering**: Períodos de alta/baja volatilidad se agrupan
2. **Mean Reversion**: Tiende a regresar a un promedio
3. **Leverage Effect**: Malas noticias aumentan más la volatilidad

#### **Modelo GARCH(1,1):**
```
σ²_t = ω + α × ε²_(t-1) + β × σ²_(t-1)
```

Donde:
- ω = término constante
- α = impacto de shocks recientes (noticias)
- β = persistencia de volatilidad
- ε_(t-1) = shock del período anterior

#### **Interpretación:**
- **α alto**: La volatilidad reacciona fuertemente a noticias
- **β alto**: La volatilidad es persistente (dura mucho)
- **α + β ≈ 1**: Volatilidad muy persistente

---

## 🎨 **MEJORAS DE DISEÑO IMPLEMENTADAS**

### **1. Frontend (Streamlit)**
- **Tema oscuro profesional** con colores corporativos
- **Títulos en blanco** para mejor legibilidad
- **Colores consistentes por activo** en todos los gráficos
- **Tarjetas de interpretación** humanizadas
- **Métricas destacadas** con diseño moderno

### **2. Visualizaciones**
- **Gráficos Plotly** interactivos
- **Leyendas mejoradas** con nombres completos
- **Señales de trading** con posición ajustada
- **Heatmaps** de correlación intuitivos
- **Gráficos de torta** con colores específicos por activo

---

## 🚀 **CÓMO EJECUTAR EL PROYECTO**

### **1. Instalación**
```bash
# Clonar repositorio
git clone https://github.com/jhonatancaon1234/PROYECTO-RIESGO-FINANCIERO-CON-PORTAFOLIO-.git

# Instalar dependencias backend
cd backend
pip install -r requirements.txt

# Instalar dependencias frontend
cd ../frontend
pip install -r requirements.txt
```

### **2. Ejecución**
```bash
# Método 1: Usar script batch
./iniciar_dashboard.bat

# Método 2: Manual
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
streamlit run app.py
```

### **3. Acceder**
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 📈 **EJEMPLO DE USO COMPLETO**

### **Paso 1: Selección de Activos**
```python
# En el sidebar, seleccionar:
- AAPL (Apple)
- MSFT (Microsoft)
- XOM (Exxon)
- KO (Coca-Cola)
- SPY (S&P 500)
```

### **Paso 2: Configuración**
```python
# Parámetros:
- Período: 2 años
- Nivel de confianza VaR: 95%
```

### **Paso 3: Análisis**
```python
# El sistema calcula automáticamente:
1. Precios y retornos históricos
2. Indicadores técnicos (SMA, RSI)
3. Métricas de riesgo (VaR, CVaR)
4. Betas y Alpha (CAPM)
5. Portafolios óptimos (Markowitz)
6. Señales de trading
```

### **Paso 4: Interpretación**
```python
# Ejemplo de resultados:
- AAPL: Beta = 1.2 (20% más volátil que mercado)
- VaR (95%) = 2.5% → Máxima pérdida diaria esperada: 2.5%
- Portafolio Máx Sharpe: 40% AAPL, 30% MSFT, 20% XOM, 10% KO
- Señal actual: HOLD (esperar mejor oportunidad)
```

---

## 🔍 **CONCLUSIONES Y APRENDIZAJES**

### **Lo que aprendimos:**
1. **Gestión de Riesgo**: El VaR es útil pero tiene limitaciones
2. **Diversificación**: La correlación es clave para reducir riesgo
3. **Análisis Técnico**: Útil pero no infalible, mejor combinar con fundamental
4. **Optimización**: Markowitz es poderoso pero sensible a estimaciones
5. **Volatilidad**: No es constante, modelos GARCH la capturan mejor

### **Aplicaciones Prácticas:**
1. **Gestión de Portafolios**: Asignación óptima de activos
2. **Risk Management**: Límites de pérdida diaria
3. **Trading**: Señales sistemáticas basadas en datos
4. **Análisis de Inversiones**: Evaluación riesgo-retorno

### **Limitaciones:**
1. **Datos históricos**: No garantizan resultados futuros
2. **Supuestos de normalidad**: Los mercados tienen colas gruesas
3. **Costos de transacción**: No considerados en optimización
4. **Liquidez**: Asumimos que podemos comprar/vender siempre

---

## 📚 **REFERENCIAS BIBLIOGRÁFICAS**

1. **Markowitz, H. (1952)**: "Portfolio Selection" - Journal of Finance
2. **Sharpe, W. (1964)**: "Capital Asset Prices" - Journal of Finance
3. **Jorion, P. (2007)**: "Value at Risk" - McGraw-Hill
4. **Tsay, R. (2005)**: "Analysis of Financial Time Series" - Wiley
5. **Hull, J. (2018)**: "Options, Futures and Other Derivatives" - Pearson

---

## 👨‍💻 **SOBRE EL AUTOR**

Proyecto universitario desarrollado para la asignatura de **Gestión de Riesgo Financiero** en la Universidad Santo Tomás.

**Tecnologías utilizadas:**
- Python 3.9+
- FastAPI (Backend)
- Streamlit (Frontend)
- Pandas, NumPy (Análisis de datos)
- Plotly (Visualizaciones)
- SciPy (Optimización)
- ARCH (Modelos de volatilidad)

**Contacto:** jhonatancaon1234@ustadigital.edu.co

---

**Fecha de última actualización:** 18 de abril de 2026
**Versión:** 2.0 - Sistema Profesional Completo