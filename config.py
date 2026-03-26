"""
Configuración del proyecto de análisis de riesgo financiero
"""

# Configuración de activos
ASSETS = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation', 
    'XOM': 'Exxon Mobil Corporation',
    'KO': 'The Coca-Cola Company',
    'SPY': 'SPDR S&P 500 ETF Trust'
}

# Configuración de análisis
ANALYSIS_CONFIG = {
    'risk_free_rate': 0.02,  # Tasa libre de riesgo (2%)
    'confidence_level': 0.05,  # Nivel de confianza para VaR (95%)
    'lookback_period': 252,   # Período de análisis (días hábiles)
    'train_test_split': 0.8,  # División entrenamiento/prueba
    'optimization_periods': 63  # Períodos para optimización (3 meses)
}

# Configuración de indicadores técnicos
TECHNICAL_CONFIG = {
    'sma_short': 20,
    'sma_long': 50,
    'ema_short': 12,
    'ema_long': 26,
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9
}

# Configuración de modelos ARCH/GARCH
GARCH_CONFIG = {
    'p': 1,  # Orden ARCH
    'q': 1,  # Orden GARCH
    'mean': 'Zero',  # Modelo de media
    'vol': 'Garch',  # Modelo de volatilidad
    'dist': 'normal'  # Distribución de errores
}

# Configuración de señales de trading
TRADING_CONFIG = {
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'signal_threshold': 0.02  # Umbral para señales (2%)
}

# Configuración de optimización
OPTIMIZATION_CONFIG = {
    'min_weight': 0.0,
    'max_weight': 0.4,
    'target_return': 0.10  # Retorno objetivo anual (10%)
}