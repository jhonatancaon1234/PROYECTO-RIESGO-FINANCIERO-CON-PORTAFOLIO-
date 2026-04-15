"""
Backend FastAPI - API de Riesgo Financiero
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime

from config import settings
from models import (
    AssetRequest, 
    TechnicalAnalysisRequest, 
    RiskMetricsRequest,
    PortfolioOptimizationRequest,
    CAPMRequest,
    VolatilityRequest,
    TradingSignalsRequest,
    BenchmarkRequest,
    ApiResponse,
    TechnicalIndicators,
    RiskMetrics,
    PortfolioResult,
    CAPMResult,
    VolatilityResult,
    TradingSignal,
    BenchmarkComparison
)
from services.data_service import DataService
from services.analysis_service import AnalysisService

# Inicializar FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para análisis de riesgo financiero con modelos avanzados (CAPM, GARCH, VaR, Markowitz)"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
data_service = DataService()
analysis_service = AnalysisService()


# Dependencias
def get_data_service():
    """Inyección de dependencia para DataService"""
    return data_service


def get_analysis_service():
    """Inyección de dependencia para AnalysisService"""
    return analysis_service


# Endpoints
@app.get("/", response_model=ApiResponse)
async def root():
    """Endpoint raíz"""
    return ApiResponse(
        success=True,
        message="API de Riesgo Financiero - Documentación disponible en /docs",
        data={
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "endpoints": [
                "/data",
                "/technical-analysis",
                "/risk-metrics",
                "/portfolio-optimize",
                "/capm",
                "/volatility",
                "/trading-signals",
                "/benchmark"
            ]
        }
    )


@app.post("/data", response_model=ApiResponse)
async def get_financial_data(
    request: AssetRequest,
    data_service: DataService = Depends(get_data_service)
):
    """
    Endpoint 1: Obtener datos financieros
    
    - **assets**: Lista de símbolos de activos
    - **start_date**: Fecha de inicio (opcional)
    - **end_date**: Fecha de fin (opcional)
    - **confidence_level**: Nivel de confianza para VaR
    """
    try:
        result = data_service.get_financial_data(
            assets=request.assets,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        # Convertir DataFrames a diccionarios para JSON
        prices_dict = result['prices'].to_dict()
        returns_dict = result['returns'].to_dict()
        
        return ApiResponse(
            success=True,
            message="Datos financieros obtenidos exitosamente",
            data={
                "prices": prices_dict,
                "returns": returns_dict,
                "stats": result['stats'],
                "assets": result['assets']
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/technical-analysis", response_model=ApiResponse)
async def technical_analysis(
    request: TechnicalAnalysisRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 2: Análisis Técnico
    
    - **symbol**: Símbolo del activo
    - **window_sma_short**: Ventana SMA corta
    - **window_sma_long**: Ventana SMA larga
    - **window_rsi**: Ventana RSI
    
    Retorna indicadores técnicos y señales de trading.
    """
    try:
        # Obtener datos
        data = data_service.get_financial_data(assets=[request.symbol])
        prices = data['prices'][request.symbol]
        
        # Calcular indicadores
        indicators = analysis_service.calculate_technical_indicators(
            prices=prices,
            symbol=request.symbol
        )
        
        return ApiResponse(
            success=True,
            message="Análisis técnico completado",
            data=indicators
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/risk-metrics", response_model=ApiResponse)
async def risk_metrics(
    request: RiskMetricsRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 3: Métricas de Riesgo
    
    - **symbol**: Símbolo del activo
    - **confidence_level**: Nivel de confianza para VaR (1% a 10%)
    
    Retorna VaR, CVaR, volatilidad y máximo drawdown.
    """
    try:
        # Obtener datos
        data = data_service.get_financial_data(assets=[request.symbol])
        returns = data['returns'][request.symbol]
        
        # Calcular métricas
        metrics = analysis_service.calculate_risk_metrics(
            returns=returns,
            confidence_level=request.confidence_level
        )
        
        return ApiResponse(
            success=True,
            message="Métricas de riesgo calculadas",
            data=metrics
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/portfolio-optimize", response_model=ApiResponse)
async def portfolio_optimize(
    request: PortfolioOptimizationRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 4: Optimización de Portafolio (Markowitz)
    
    - **assets**: Lista de activos del portafolio
    - **target_return**: Retorno objetivo (opcional)
    - **risk_tolerance**: Tolerancia al riesgo (0 a 1)
    
    Retorna portafolios óptimos de mínima varianza y máximo Sharpe.
    """
    try:
        # Obtener datos
        data = data_service.get_financial_data(assets=request.assets)
        returns = data['returns']
        
        # Optimizar portafolio
        optimization_result = analysis_service.optimize_portfolio(
            returns=returns,
            target_return=request.target_return
        )
        
        return ApiResponse(
            success=True,
            message="Portafolio optimizado exitosamente",
            data=optimization_result
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/capm", response_model=ApiResponse)
async def capm_analysis(
    request: CAPMRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 5: Análisis CAPM
    
    - **assets**: Lista de activos a analizar
    - **market_symbol**: Símbolo del mercado (benchmark)
    
    Retorna alpha, beta, R-cuadrado y clasificación de riesgo.
    """
    try:
        # Obtener datos
        all_assets = request.assets + [request.market_symbol]
        data = data_service.get_financial_data(assets=all_assets)
        returns = data['returns']
        
        # Calcular CAPM para cada activo
        capm_results = {}
        market_returns = returns[request.market_symbol]
        
        for symbol in request.assets:
            if symbol != request.market_symbol:
                asset_returns = returns[symbol]
                capm_result = analysis_service.calculate_capm(
                    asset_returns=asset_returns,
                    market_returns=market_returns
                )
                capm_results[symbol] = capm_result
        
        return ApiResponse(
            success=True,
            message="Análisis CAPM completado",
            data=capm_results
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/volatility", response_model=ApiResponse)
async def volatility_analysis(
    request: VolatilityRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 6: Análisis de Volatilidad (GARCH)
    
    - **symbol**: Símbolo del activo
    - **window**: Ventana de volatilidad
    
    Retorna volatilidad histórica, volatilidad GARCH y forecast.
    """
    try:
        # Obtener datos
        data = data_service.get_financial_data(assets=[request.symbol])
        returns = data['returns'][request.symbol]
        
        # Calcular volatilidad
        volatility_result = analysis_service.calculate_volatility(
            returns=returns
        )
        
        return ApiResponse(
            success=True,
            message="Análisis de volatilidad completado",
            data=volatility_result
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/trading-signals", response_model=ApiResponse)
async def trading_signals(
    request: TradingSignalsRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 7: Señales de Trading
    
    - **symbol**: Símbolo del activo
    - **strategy**: Estrategia de señales (combined, sma, rsi)
    
    Retorna señales de compra/venta con nivel de confianza.
    """
    try:
        # Obtener datos
        data = data_service.get_financial_data(assets=[request.symbol])
        prices = data['prices'][request.symbol]
        
        # Generar señales
        signal = analysis_service.generate_trading_signals(
            prices=prices,
            symbol=request.symbol
        )
        
        return ApiResponse(
            success=True,
            message="Señales de trading generadas",
            data=signal
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/benchmark", response_model=ApiResponse)
async def benchmark_comparison(
    request: BenchmarkRequest,
    data_service: DataService = Depends(get_data_service),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Endpoint 8: Comparación con Benchmark
    
    - **assets**: Lista de activos a comparar
    - **benchmark_symbol**: Símbolo del benchmark
    
    Retorna alpha, beta, tracking error e information ratio.
    """
    try:
        # Obtener datos
        all_assets = request.assets + [request.benchmark_symbol]
        data = data_service.get_financial_data(assets=all_assets)
        returns = data['returns']
        
        # Comparar con benchmark
        benchmark_returns = returns[request.benchmark_symbol]
        comparison_results = {}
        
        for symbol in request.assets:
            if symbol != request.benchmark_symbol:
                asset_returns = returns[symbol]
                comparison = analysis_service.compare_with_benchmark(
                    returns=asset_returns,
                    benchmark_returns=benchmark_returns
                )
                comparison_results[symbol] = comparison
        
        return ApiResponse(
            success=True,
            message="Comparación con benchmark completada",
            data=comparison_results
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION
    }


# Manejo de excepciones global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    return ApiResponse(
        success=False,
        message="Error interno del servidor",
        error=str(exc)
    )