"""
Servicio de datos para FastAPI
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import yfinance as yf
from ..config import settings


class DataService:
    """Servicio para manejo de datos financieros"""
    
    def __init__(self):
        self.cache = {}
    
    def get_financial_data(
        self, 
        assets: List[str], 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Obtiene datos financieros de Yahoo Finance"""
        try:
            # Validar fechas
            if not start_date:
                start_date = settings.DEFAULT_START_DATE
            if not end_date:
                end_date = settings.DEFAULT_END_DATE
            
            # Crear clave de caché
            cache_key = f"{'_'.join(sorted(assets))}_{start_date}_{end_date}"
            
            # Verificar caché
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Descargar datos
            data = {}
            for symbol in assets:
                try:
                    ticker = yf.download(symbol, start=start_date, end=end_date)
                    if not ticker.empty:
                        data[symbol] = ticker
                except Exception as e:
                    print(f"Error descargando {symbol}: {e}")
            
            if not data:
                raise ValueError("No se pudieron descargar datos para los activos especificados")
            
            # Procesar datos
            prices = pd.DataFrame({symbol: data[symbol]['Close'] for symbol in data.keys()})
            returns = prices.pct_change().dropna()
            
            # Calcular estadísticas básicas
            stats = {
                'period_start': prices.index[0].strftime('%Y-%m-%d'),
                'period_end': prices.index[-1].strftime('%Y-%m-%d'),
                'total_days': len(prices),
                'assets_count': len(assets),
                'missing_assets': [symbol for symbol in assets if symbol not in data]
            }
            
            result = {
                'prices': prices,
                'returns': returns,
                'stats': stats,
                'assets': list(prices.columns)
            }
            
            # Guardar en caché
            self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            raise Exception(f"Error obteniendo datos financieros: {str(e)}")
    
    def get_price_history(self, symbol: str, days: int = 365) -> pd.DataFrame:
        """Obtiene historial de precios para un activo"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            data = yf.download(symbol, start=start_date, end=end_date)
            return data
        except Exception as e:
            raise Exception(f"Error obteniendo historial de precios para {symbol}: {str(e)}")
    
    def get_current_price(self, symbol: str) -> float:
        """Obtiene el precio actual de un activo"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('currentPrice', 0.0)
        except Exception as e:
            raise Exception(f"Error obteniendo precio actual para {symbol}: {str(e)}")