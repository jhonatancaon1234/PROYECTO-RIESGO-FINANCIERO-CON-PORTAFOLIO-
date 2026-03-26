"""
Módulo para generar señales de trading automáticas
"""

import pandas as pd
import numpy as np
from scipy import stats
from config import TRADING_CONFIG, TECHNICAL_CONFIG


class TradingSignals:
    """Clase para generar señales de trading automáticas"""
    
    def __init__(self, prices_df, returns_df):
        self.prices = prices_df
        self.returns = returns_df
        self.signals = {}
    
    def generate_sma_signals(self, short_period=20, long_period=50):
        """Genera señales basadas en cruces de medias móviles"""
        signals = {}
        
        for symbol in self.prices.columns:
            prices = self.prices[symbol].dropna()
            
            # Calcular medias móviles
            sma_short = prices.rolling(window=short_period).mean()
            sma_long = prices.rolling(window=long_period).mean()
            
            # Señales de cruce
            signals[symbol] = pd.DataFrame({
                'price': prices,
                'sma_short': sma_short,
                'sma_long': sma_long
            })
            
            # Señal: 1 (compra) cuando SMA corta cruza al alza, -1 (venta) cuando cruza a la baja
            signals[symbol]['signal'] = np.where(
                signals[symbol]['sma_short'] > signals[symbol]['sma_long'], 1, -1
            )
            
            # Señal de cambio (momento de acción)
            signals[symbol]['signal_change'] = signals[symbol]['signal'].diff()
        
        return signals
    
    def generate_ema_signals(self, short_period=12, long_period=26):
        """Genera señales basadas en cruces de medias móviles exponenciales"""
        signals = {}
        
        for symbol in self.prices.columns:
            prices = self.prices[symbol].dropna()
            
            # Calcular EMAs
            ema_short = prices.ewm(span=short_period).mean()
            ema_long = prices.ewm(span=long_period).mean()
            
            # Señales
            signals[symbol] = pd.DataFrame({
                'price': prices,
                'ema_short': ema_short,
                'ema_long': ema_long
            })
            
            signals[symbol]['signal'] = np.where(
                signals[symbol]['ema_short'] > signals[symbol]['ema_long'], 1, -1
            )
            signals[symbol]['signal_change'] = signals[symbol]['signal'].diff()
        
        return signals
    
    def generate_rsi_signals(self, period=14, overbought=70, oversold=30):
        """Genera señales basadas en RSI"""
        signals = {}
        
        for symbol in self.prices.columns:
            prices = self.prices[symbol].dropna()
            
            # Calcular RSI
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Señales basadas en niveles de sobrecompra/sobreventa
            signals[symbol] = pd.DataFrame({
                'price': prices,
                'rsi': rsi
            })
            
            signals[symbol]['signal'] = np.where(
                signals[symbol]['rsi'] < oversold, 1,  # Compra en sobreventa
                np.where(signals[symbol]['rsi'] > overbought, -1, 0)  # Venta en sobrecompra
            )
        
        return signals
    
    def generate_macd_signals(self, fast=12, slow=26, signal=9):
        """Genera señales basadas en MACD"""
        signals = {}
        
        for symbol in self.prices.columns:
            prices = self.prices[symbol].dropna()
            
            # Calcular MACD
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            
            macd = ema_fast - ema_slow
            signal_line = macd.ewm(span=signal).mean()
            histogram = macd - signal_line
            
            # Señales basadas en cruces MACD/Signal
            signals[symbol] = pd.DataFrame({
                'price': prices,
                'macd': macd,
                'signal_line': signal_line,
                'histogram': histogram
            })
            
            signals[symbol]['signal'] = np.where(
                signals[symbol]['macd'] > signals[symbol]['signal_line'], 1, -1
            )
            signals[symbol]['signal_change'] = signals[symbol]['signal'].diff()
        
        return signals
    
    def generate_bollinger_signals(self, period=20, std_dev=2):
        """Genera señales basadas en bandas de Bollinger"""
        signals = {}
        
        for symbol in self.prices.columns:
            prices = self.prices[symbol].dropna()
            
            # Calcular bandas de Bollinger
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            # Señales basadas en precio respecto a bandas
            signals[symbol] = pd.DataFrame({
                'price': prices,
                'sma': sma,
                'upper_band': upper_band,
                'lower_band': lower_band
            })
            
            # Compra cuando precio toca banda inferior, venta cuando toca superior
            signals[symbol]['signal'] = np.where(
                signals[symbol]['price'] <= signals[symbol]['lower_band'], 1,
                np.where(signals[symbol]['price'] >= signals[symbol]['upper_band'], -1, 0)
            )
        
        return signals
    
    def generate_combined_signals(self):
        """Combina múltiples señales para generar una señal final"""
        # Obtener todas las señales individuales
        sma_signals = self.generate_sma_signals()
        rsi_signals = self.generate_rsi_signals()
        macd_signals = self.generate_macd_signals()
        
        combined_signals = {}
        
        for symbol in self.prices.columns:
            # Combinar señales (pesos iguales)
            sma_signal = sma_signals[symbol]['signal'].iloc[-1]
            rsi_signal = rsi_signals[symbol]['signal'].iloc[-1]
            macd_signal = macd_signals[symbol]['signal'].iloc[-1]
            
            # Señal combinada
            combined_score = (sma_signal + rsi_signal + macd_signal) / 3
            
            # Clasificación de señal
            if combined_score > 0.33:
                signal_type = "COMPRAR"
                confidence = combined_score
            elif combined_score < -0.33:
                signal_type = "VENDER"
                confidence = abs(combined_score)
            else:
                signal_type = "MANTENER"
                confidence = abs(combined_score)
            
            combined_signals[symbol] = {
                'sma_signal': sma_signal,
                'rsi_signal': rsi_signal,
                'macd_signal': macd_signal,
                'combined_score': combined_score,
                'signal_type': signal_type,
                'confidence': confidence,
                'recommendation': self._get_recommendation(combined_score)
            }
        
        return combined_signals
    
    def _get_recommendation(self, score):
        """Obtiene recomendación basada en score"""
        if score > 0.66:
            return "Fuerte Compra"
        elif score > 0.33:
            return "Compra"
        elif score > -0.33:
            return "Mantener"
        elif score > -0.66:
            return "Venta"
        else:
            return "Fuerte Venta"
    
    def backtest_signals(self, signals_dict, initial_capital=100000):
        """Backtest de señales de trading"""
        results = {}
        
        for symbol, signal_data in signals_dict.items():
            if symbol not in self.prices.columns:
                continue
            
            prices = self.prices[symbol].dropna()
            
            # Simular trading basado en señales
            capital = initial_capital
            shares = 0
            trades = []
            
            for i in range(1, len(prices)):
                current_price = prices.iloc[i]
                previous_signal = signal_data['signal'].iloc[i-1] if i > 0 else 0
                current_signal = signal_data['signal'].iloc[i]
                
                # Estrategia: entrar en largo con señal positiva, salir con señal negativa
                if previous_signal <= 0 and current_signal > 0:  # Señal de compra
                    shares = capital / current_price
                    trades.append({
                        'date': prices.index[i],
                        'action': 'BUY',
                        'price': current_price,
                        'shares': shares,
                        'capital': capital
                    })
                    capital = 0
                
                elif previous_signal > 0 and current_signal <= 0:  # Señal de venta
                    if shares > 0:
                        capital = shares * current_price
                        trades.append({
                            'date': prices.index[i],
                            'action': 'SELL',
                            'price': current_price,
                            'shares': shares,
                            'capital': capital
                        })
                        shares = 0
            
            # Valor final (si quedan acciones)
            final_value = capital if shares == 0 else shares * prices.iloc[-1]
            total_return = (final_value - initial_capital) / initial_capital
            
            results[symbol] = {
                'initial_capital': initial_capital,
                'final_value': final_value,
                'total_return': total_return,
                'num_trades': len(trades),
                'trades': trades
            }
        
        return results
    
    def calculate_signal_performance(self, signals_dict):
        """Calcula el performance de las señales"""
        performance = {}
        
        for symbol in signals_dict.keys():
            if symbol not in self.returns.columns:
                continue
            
            returns = self.returns[symbol].dropna()
            
            # Calcular retornos acumulados
            cumulative_returns = (1 + returns).cumprod()
            
            # Métricas de performance
            total_return = cumulative_returns.iloc[-1] - 1
            annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
            volatility = returns.std() * np.sqrt(252)
            sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
            
            performance[symbol] = {
                'total_return': total_return,
                'annualized_return': annualized_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': self._calculate_max_drawdown(cumulative_returns)
            }
        
        return performance
    
    def _calculate_max_drawdown(self, cumulative_returns):
        """Calcula el drawdown máximo"""
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        return drawdown.min()
    
    def generate_signal_report(self):
        """Genera reporte completo de señales"""
        print("🎯 Sistema de Señales de Trading Automáticas")
        print("=" * 60)
        
        # Señales combinadas
        combined_signals = self.generate_combined_signals()
        
        print("\n📊 Señales Combinadas:")
        for symbol, signal in combined_signals.items():
            print(f"\n{symbol}:")
            print(f"  Señal SMA: {signal['sma_signal']}")
            print(f"  Señal RSI: {signal['rsi_signal']}")
            print(f"  Señal MACD: {signal['macd_signal']}")
            print(f"  Score combinado: {signal['combined_score']:.2f}")
            print(f"  Tipo: {signal['signal_type']}")
            print(f"  Confianza: {signal['confidence']:.2f}")
            print(f"  Recomendación: {signal['recommendation']}")
        
        # Performance de señales
        print(f"\n📈 Performance de Señales:")
        performance = self.calculate_signal_performance(combined_signals)
        
        for symbol, perf in performance.items():
            print(f"\n{symbol}:")
            print(f"  Retorno total: {perf['total_return']:.4f}")
            print(f"  Retorno anualizado: {perf['annualized_return']:.4f}")
            print(f"  Volatilidad: {perf['volatility']:.4f}")
            print(f"  Sharpe ratio: {perf['sharpe_ratio']:.4f}")
            print(f"  Drawdown máximo: {perf['max_drawdown']:.4f}")
        
        return {
            'combined_signals': combined_signals,
            'performance': performance,
            'sma_signals': self.generate_sma_signals(),
            'rsi_signals': self.generate_rsi_signals(),
            'macd_signals': self.generate_macd_signals()
        }


def generate_trading_signals(prices_df, returns_df):
    """Función principal para generar señales de trading"""
    ts = TradingSignals(prices_df, returns_df)
    return ts.generate_signal_report()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass