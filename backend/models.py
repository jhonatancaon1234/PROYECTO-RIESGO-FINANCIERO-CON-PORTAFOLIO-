"""
Modelos Pydantic para FastAPI
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import date
from decimal import Decimal


class AssetRequest(BaseModel):
    """Solicitud para análisis de activos"""
    assets: List[str] = Field(
        default=["AAPL", "MSFT", "XOM", "KO", "SPY"],
        description="Lista de símbolos de activos a analizar",
        min_length=1,
        max_length=10
    )
    start_date: Optional[date] = Field(
        default=None,
        description="Fecha de inicio del análisis"
    )
    end_date: Optional[date] = Field(
        default=None,
        description="Fecha de fin del análisis"
    )
    confidence_level: float = Field(
        default=0.05,
        ge=0.01,
        le=0.10,
        description="Nivel de confianza para cálculo de VaR (1% a 10%)"
    )
    
    @field_validator('assets')
    @classmethod
    def validate_assets(cls, v):
        """Validador personalizado para símbolos de activos"""
        valid_symbols = ['AAPL', 'MSFT', 'XOM', 'KO', 'SPY', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA']
        for symbol in v:
            if symbol not in valid_symbols:
                raise ValueError(f"Símbolo {symbol} no es válido. Símbolos permitidos: {valid_symbols}")
        return v
    
    @field_validator('confidence_level')
    @classmethod
    def validate_confidence_level(cls, v):
        """Validador personalizado para nivel de confianza"""
        if v <= 0 or v > 0.10:
            raise ValueError("El nivel de confianza debe estar entre 0.01 y 0.10")
        return v


class TechnicalAnalysisRequest(BaseModel):
    """Solicitud para análisis técnico"""
    symbol: str = Field(..., description="Símbolo del activo")
    window_sma_short: int = Field(default=20, ge=5, le=100, description="Ventana SMA corta")
    window_sma_long: int = Field(default=50, ge=20, le=200, description="Ventana SMA larga")
    window_rsi: int = Field(default=14, ge=5, le=50, description="Ventana RSI")


class RiskMetricsRequest(BaseModel):
    """Solicitud para métricas de riesgo"""
    symbol: str = Field(..., description="Símbolo del activo")
    confidence_level: float = Field(default=0.05, ge=0.01, le=0.10, description="Nivel de confianza")


class PortfolioOptimizationRequest(BaseModel):
    """Solicitud para optimización de portafolio"""
    assets: List[str] = Field(..., min_length=2, max_length=10, description="Activos del portafolio")
    target_return: Optional[float] = Field(None, description="Retorno objetivo")
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0, description="Tolerancia al riesgo")


class CAPMRequest(BaseModel):
    """Solicitud para análisis CAPM"""
    assets: List[str] = Field(..., min_length=1, max_length=10, description="Activos a analizar")
    market_symbol: str = Field(default="SPY", description="Símbolo del mercado")


class VolatilityRequest(BaseModel):
    """Solicitud para análisis de volatilidad"""
    symbol: str = Field(..., description="Símbolo del activo")
    window: int = Field(default=30, ge=10, le=100, description="Ventana de volatilidad")


class TradingSignalsRequest(BaseModel):
    """Solicitud para señales de trading"""
    symbol: str = Field(..., description="Símbolo del activo")
    strategy: str = Field(default="combined", description="Estrategia de señales")


class BenchmarkRequest(BaseModel):
    """Solicitud para comparación con benchmark"""
    assets: List[str] = Field(..., min_length=1, max_length=10, description="Activos a comparar")
    benchmark_symbol: str = Field(default="SPY", description="Símbolo del benchmark")


# Modelos de respuesta
class PriceData(BaseModel):
    """Datos de precios"""
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class TechnicalIndicators(BaseModel):
    """Indicadores técnicos"""
    symbol: str
    sma_short: float
    sma_long: float
    rsi: float
    signal: str
    recommendation: str


class RiskMetrics(BaseModel):
    """Métricas de riesgo"""
    symbol: str
    var: float
    cvar: float
    volatility: float
    max_drawdown: float


class PortfolioResult(BaseModel):
    """Resultado de optimización de portafolio"""
    weights: Dict[str, float]
    expected_return: float
    volatility: float
    sharpe_ratio: float
    efficient_frontier: List[Dict[str, float]]


class CAPMResult(BaseModel):
    """Resultado de análisis CAPM"""
    symbol: str
    alpha: float
    beta: float
    r_squared: float
    recommendation: str


class VolatilityResult(BaseModel):
    """Resultado de análisis de volatilidad"""
    symbol: str
    historical_volatility: float
    garch_volatility: float
    volatility_forecast: List[float]


class TradingSignal(BaseModel):
    """Señal de trading"""
    symbol: str
    signal_type: str
    confidence: float
    price: float
    timestamp: str


class BenchmarkComparison(BaseModel):
    """Comparación con benchmark"""
    asset: str
    alpha: float
    beta: float
    tracking_error: float
    information_ratio: float
    outperformance: bool


class ApiResponse(BaseModel):
    """Respuesta API genérica"""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None