"""
Módulo para análisis técnico de activos financieros
"""

import pandas as pd
import numpy as np
from scipy import stats
from config import TECHNICAL_CONFIG


class TechnicalAnalysis:
    """Clase para realizar análisis técnico"""
    
    def __init__(self, prices_df):
        self.prices = prices_df
    
    def calculate_sma(self, period):
        """Calcula promedio móvil simple"""
        return self.prices.rolling(window=period).mean()
    
    def calculate_ema(self, period):
        """Calcula promedio móvil exponencial"""
        return self.prices.ewm(span=period).mean()
    
    def calculate_rsi(self, period=14):
        """Calcula Relative Strength Index"""
        delta = self.prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """Calcula MACD (Moving Average Convergence Divergence)
        
        El MACD muestra la relación entre dos medias móviles exponenciales del precio:
        - MACD Line = EMA(12) - EMA(26)
        - Signal Line = EMA(9) del MACD
        - Histogram = MACD - Signal
        
        Señales:
        - Cruce alcista: MACD cruza hacia ARRIBA de Signal → COMPRA
        - Cruce bajista: MACD cruza hacia ABAJO de Signal → VENTA
        """
        ema_fast = self.prices.ewm(span=fast).mean()
        ema_slow = self.prices.ewm(span=slow).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    def calculate_stochastic(self, k_period=14, d_period=3):
        """Calcula Estocástico (Stochastic Oscillator)
        
        El estocástico compara el precio de cierre con su rango en un período:
        - %K = (Cierre - Mínimo) / (Máximo - Mínimo) × 100
        - %D = SMA(3) del %K
        
        Señales:
        - > 80: Zona de sobrecompra (posible corrección)
        - < 20: Zona de sobreventa (posible rebote)
        - %K cruza hacia ARRIBA de %D: Señal de COMPRA
        - %K cruza hacia ABAJO de %D: Señal de VENTA
        """
        # Necesitamos los precios de cierre, máximos y mínimos
        # Si solo tenemos precios de cierre, usamos ese como referencia
        close_prices = self.prices
        
        # Para un cálculo más preciso, necesitaríamos datos OHLC
        # Por ahora, usamos el precio de cierre como aproximación
        # En una implementación real, se deberían usar high, low, close
        
        # Calculamos el rango rolling
        rolling_min = close_prices.rolling(window=k_period).min()
        rolling_max = close_prices.rolling(window=k_period).max()
        rolling_range = rolling_max - rolling_min
        
        # Calculamos %K
        k_percent = ((close_prices - rolling_min) / rolling_range) * 100
        
        # Calculamos %D (SMA del %K)
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent, d_percent
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """Calcula bandas de Bollinger"""
        sma = self.calculate_sma(period)
        std = self.prices.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    def get_technical_indicators(self, symbol):
        """Obtiene todos los indicadores técnicos para un símbolo"""
        if symbol not in self.prices.columns:
            return None
        
        data = self.prices[[symbol]].copy()
        
        # Configuración de parámetros
        config = TECHNICAL_CONFIG
        
        # Calcular indicadores
        data['SMA_Short'] = self.calculate_sma(config['sma_short'])[symbol]
        data['SMA_Long'] = self.calculate_sma(config['sma_long'])[symbol]
        data['EMA_Short'] = self.calculate_ema(config['ema_short'])[symbol]
        data['EMA_Long'] = self.calculate_ema(config['ema_long'])[symbol]
        data['RSI'] = self.calculate_rsi(config['rsi_period'])[symbol]
        
        # MACD
        macd, signal, histogram = self.calculate_macd(
            config['macd_fast'], config['macd_slow'], config['macd_signal']
        )
        data['MACD'] = macd[symbol]
        data['MACD_Signal'] = signal[symbol]
        data['MACD_Histogram'] = histogram[symbol]
        
        # Bandas de Bollinger
        upper, middle, lower = self.calculate_bollinger_bands()
        data['BB_Upper'] = upper[symbol]
        data['BB_Middle'] = middle[symbol]
        data['BB_Lower'] = lower[symbol]
        
        # Señales de trading
        data['Signal_SMA'] = np.where(data['SMA_Short'] > data['SMA_Long'], 1, -1)
        data['Signal_EMA'] = np.where(data['EMA_Short'] > data['EMA_Long'], 1, -1)
        data['Signal_RSI'] = np.where(data['RSI'] < 30, 1, np.where(data['RSI'] > 70, -1, 0))
        
        return data.dropna()
    
    def get_all_technical_analysis(self):
        """Obtiene análisis técnico para todos los activos"""
        results = {}
        
        for symbol in self.prices.columns:
            indicators = self.get_technical_indicators(symbol)
            if indicators is not None:
                results[symbol] = indicators
        
        return results
    
    def generate_trading_signals(self):
        """Genera señales de trading combinadas"""
        signals = {}
        
        for symbol in self.prices.columns:
            data = self.get_technical_indicators(symbol)
            if data is None:
                continue
            
            # Combinar señales
            sma_signal = data['Signal_SMA'].iloc[-1]
            ema_signal = data['Signal_EMA'].iloc[-1]
            rsi_signal = data['Signal_RSI'].iloc[-1]
            
            # Estrategia combinada
            combined_signal = (sma_signal + ema_signal + rsi_signal) / 3
            
            signals[symbol] = {
                'sma': sma_signal,
                'ema': ema_signal,
                'rsi': rsi_signal,
                'combined': combined_signal,
                'recommendation': self._get_recommendation(combined_signal)
            }
        
        return signals
    
    def _get_recommendation(self, signal):
        """Obtiene recomendación basada en señal"""
        if signal > 0.5:
            return "COMPRAR"
        elif signal < -0.5:
            return "VENDER"
        else:
            return "MANTENER"


def analyze_technical(prices_df):
    """Función principal para análisis técnico"""
    ta = TechnicalAnalysis(prices_df)
    
    # Obtener análisis para todos los activos
    technical_data = ta.get_all_technical_analysis()
    signals = ta.generate_trading_signals()
    
    print("📊 Análisis Técnico:")
    for symbol, data in technical_data.items():
        latest = data.iloc[-1]
        print(f"\n{symbol}:")
        print(f"  RSI: {latest['RSI']:.2f}")
        print(f"  MACD: {latest['MACD']:.4f}")
        print(f"  SMA Signal: {latest['Signal_SMA']}")
        print(f"  EMA Signal: {latest['Signal_EMA']}")
    
    print("\n🎯 Señales de Trading:")
    for symbol, signal in signals.items():
        print(f"  {symbol}: {signal['recommendation']} (Score: {signal['combined']:.2f})")
    
    return {
        'technical_data': technical_data,
        'trading_signals': signals,
        'analyzer': ta
    }


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass