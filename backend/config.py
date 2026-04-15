"""
Configuración del Backend FastAPI
"""

from pydantic_settings import BaseSettings
from typing import List
from datetime import datetime, timedelta


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    APP_NAME: str = "API de Riesgo Financiero"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configuración de activos
    DEFAULT_ASSETS: List[str] = ["AAPL", "MSFT", "XOM", "KO", "SPY"]
    
    # Configuración de fechas (5 años atrás hasta hoy) - Dinámico
    DEFAULT_START_DATE: str = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    DEFAULT_END_DATE: str = datetime.now().strftime('%Y-%m-%d')
    
    # Configuración de riesgo
    DEFAULT_CONFIDENCE_LEVEL: float = 0.05
    RISK_FREE_RATE: float = 0.02
    
    # Configuración de ventanas
    SMA_SHORT_WINDOW: int = 20
    SMA_LONG_WINDOW: int = 50
    RSI_WINDOW: int = 14
    GARCH_P: int = 1
    GARCH_Q: int = 1
    
    # Configuración de CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:8502"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia de configuración
settings = Settings()