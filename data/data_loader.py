"""
Módulo para cargar datos financieros de Yahoo Finance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from config import ASSETS, ANALYSIS_CONFIG


class DataLoader:
    """Clase para cargar y procesar datos financieros"""
    
    def __init__(self):
        self.assets = ASSETS
        self.lookback_days = ANALYSIS_CONFIG['lookback_period']
    
    def download_data(self, start_date=None, end_date=None):
        """
        Descarga datos históricos de precios de cierre ajustado
        
        Args:
            start_date: Fecha de inicio (YYYY-MM-DD)
            end_date: Fecha de fin (YYYY-MM-DD)
            
        Returns:
            DataFrame con precios de cierre ajustado
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=self.lookback_days * 2)
        
        # Convertir a strings
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        print(f"Descargando datos desde {start_str} hasta {end_str}")
        
        # Descargar datos para todos los activos
        data = {}
        for symbol, name in self.assets.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_str, end=end_str)
                
                if not hist.empty:
                    data[symbol] = hist['Close']
                    print(f"✓ {symbol} ({name}): {len(hist)} días descargados")
                else:
                    print(f"⚠ {symbol}: No se encontraron datos")
                    
            except Exception as e:
                print(f"✗ Error descargando {symbol}: {str(e)}")
        
        # Crear DataFrame
        if data:
            prices_df = pd.DataFrame(data)
            prices_df = prices_df.dropna()  # Eliminar días sin datos
            
            if not prices_df.empty:
                print(f"\n✓ Datos descargados exitosamente:")
                print(f"  - Período: {prices_df.index[0].strftime('%Y-%m-%d')} a {prices_df.index[-1].strftime('%Y-%m-%d')}")
                print(f"  - Días: {len(prices_df)}")
                print(f"  - Activos: {list(prices_df.columns)}")
            else:
                print("⚠ No se pudieron descargar datos válidos")
                
            return prices_df
        else:
            return pd.DataFrame()
    
    def get_latest_prices(self):
        """Obtiene los precios más recientes de todos los activos"""
        latest_prices = {}
        
        for symbol in self.assets.keys():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                if 'currentPrice' in info:
                    latest_prices[symbol] = info['currentPrice']
                else:
                    # Fallback: obtener el último precio del historial
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        latest_prices[symbol] = hist['Close'].iloc[-1]
                        
            except Exception as e:
                print(f"Error obteniendo precio actual de {symbol}: {str(e)}")
                latest_prices[symbol] = None
        
        return latest_prices
    
    def get_asset_info(self, symbol):
        """Obtiene información detallada de un activo"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            asset_info = {
                'symbol': symbol,
                'name': self.assets.get(symbol, symbol),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'beta': info.get('beta', 'N/A')
            }
            
            return asset_info
            
        except Exception as e:
            print(f"Error obteniendo información de {symbol}: {str(e)}")
            return None


def load_financial_data():
    """Función principal para cargar datos financieros"""
    loader = DataLoader()
    prices = loader.download_data()
    
    if not prices.empty:
        # Calcular retornos diarios
        returns = prices.pct_change().dropna()
        
        # Información resumen
        print(f"\n📊 Resumen de datos:")
        print(f"   Precios: {prices.shape}")
        print(f"   Retornos: {returns.shape}")
        print(f"   Período: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
        
        return prices, returns
    else:
        return None, None


if __name__ == "__main__":
    # Ejemplo de uso
    prices, returns = load_financial_data()
    
    if prices is not None:
        print("\n📈 Precios (últimos 5 días):")
        print(prices.tail())
        
        print("\n📉 Retornos (últimos 5 días):")
        print(returns.tail())