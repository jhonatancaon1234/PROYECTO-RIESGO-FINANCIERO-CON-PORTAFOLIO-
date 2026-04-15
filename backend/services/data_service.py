"""
Servicio de datos para FastAPI
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import yfinance as yf
from config import settings


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
            
            # Validar que las fechas sean válidas
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                if start_dt >= end_dt:
                    raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
            except ValueError as e:
                raise ValueError(f"Formato de fecha inválido: {e}")
            
            # Crear clave de caché
            cache_key = f"{'_'.join(sorted(assets))}_{start_date}_{end_date}"
            
            # Verificar caché
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Descargar datos con manejo robusto de errores
            data = {}
            valid_assets = []
            
            for symbol in assets:
                try:
                    # Intentar descargar datos
                    ticker = yf.download(symbol, start=start_date, end=end_date)
                    
                    if not ticker.empty and not ticker['Close'].isna().all():
                        data[symbol] = ticker
                        valid_assets.append(symbol)
                        print(f"✅ Datos descargados exitosamente para {symbol}")
                    else:
                        print(f"⚠️  No se encontraron datos válidos para {symbol}")
                        
                except Exception as e:
                    print(f"❌ Error descargando {symbol}: {str(e)}")
                    continue
            
            if not data:
                raise ValueError("No se pudieron descargar datos válidos para ninguno de los activos especificados")
            
            # Procesar datos con validaciones adicionales
            prices_dict = {}
            dates = None
            
            for symbol in valid_assets:
                try:
                    if not data[symbol].empty:
                        # Extraer precios de cierre correctamente
                        close_prices = data[symbol]['Close']
                        
                        # Validar que los precios no estén todos vacíos
                        if close_prices.isna().all():
                            print(f"⚠️  Precios vacíos para {symbol}, omitiendo...")
                            continue
                            
                        # Si es un DataFrame con múltiples columnas, tomar la primera
                        if hasattr(close_prices, 'iloc'):
                            # Si es DataFrame, convertir a Series
                            if isinstance(close_prices, pd.DataFrame):
                                close_prices = close_prices.iloc[:, 0]
                            prices_dict[symbol] = close_prices.values.flatten()
                        else:
                            prices_dict[symbol] = close_prices.values.flatten()
                        
                        # Obtener fechas del primer símbolo válido
                        if dates is None:
                            if hasattr(data[symbol].index, 'to_pydatetime'):
                                dates = data[symbol].index.to_pydatetime()
                            else:
                                dates = data[symbol].index.values
                                
                except Exception as e:
                    print(f"❌ Error procesando datos para {symbol}: {str(e)}")
                    continue
            
            if not prices_dict:
                raise ValueError("No se pudieron procesar datos válidos para ningún activo")
            
            # Crear DataFrame con índice de fechas
            try:
                if dates is not None:
                    prices = pd.DataFrame(prices_dict, index=pd.to_datetime(dates))
                else:
                    prices = pd.DataFrame(prices_dict)
                
                # Validar que el DataFrame no esté vacío
                if prices.empty or prices.isna().all().all():
                    raise ValueError("DataFrame de precios vacío después del procesamiento")
                    
            except Exception as e:
                raise ValueError(f"Error creando DataFrame de precios: {str(e)}")
            
            # Calcular retornos
            try:
                returns = prices.pct_change().dropna()
                
                # Validar que haya suficientes datos
                if len(returns) < 10:  # Mínimo 10 días de datos
                    raise ValueError(f"Pocos datos disponibles: {len(returns)} días. Se necesitan al menos 10 días.")
                    
            except Exception as e:
                raise ValueError(f"Error calculando retornos: {str(e)}")
            
            # Calcular estadísticas básicas
            try:
                stats = {
                    'period_start': prices.index[0].strftime('%Y-%m-%d'),
                    'period_end': prices.index[-1].strftime('%Y-%m-%d'),
                    'total_days': len(prices),
                    'assets_count': len(valid_assets),
                    'missing_assets': [symbol for symbol in assets if symbol not in valid_assets],
                    'downloaded_assets': valid_assets
                }
                
            except Exception as e:
                raise ValueError(f"Error calculando estadísticas: {str(e)}")
            
            result = {
                'prices': prices,
                'returns': returns,
                'stats': stats,
                'assets': valid_assets
            }
            
            # Guardar en caché
            self.cache[cache_key] = result
            
            print(f"✅ Datos financieros procesados exitosamente para {len(valid_assets)} activos")
            return result
            
        except ValueError as e:
            # Errores de validación
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            # Errores generales
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