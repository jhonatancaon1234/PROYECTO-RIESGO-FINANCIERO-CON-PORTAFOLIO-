"""
Servicio de análisis financiero para FastAPI
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from scipy import stats
from scipy.optimize import minimize
from arch import arch_model
import warnings
warnings.filterwarnings('ignore')


class AnalysisService:
    """Servicio para análisis financiero"""
    
    def __init__(self):
        pass
    
    def calculate_technical_indicators(self, prices: pd.Series, symbol: str) -> Dict[str, Any]:
        """Calcula indicadores técnicos"""
        try:
            # Medias móviles
            sma_20 = prices.rolling(window=20).mean().iloc[-1]
            sma_50 = prices.rolling(window=50).mean().iloc[-1]
            
            # RSI
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Señal
            if sma_20 > sma_50 and rsi < 30:
                signal = "STRONG_BUY"
                recommendation = "COMPRAR"
            elif sma_20 > sma_50:
                signal = "BUY"
                recommendation = "COMPRAR"
            elif sma_20 < sma_50 and rsi > 70:
                signal = "STRONG_SELL"
                recommendation = "VENDER"
            elif sma_20 < sma_50:
                signal = "SELL"
                recommendation = "VENDER"
            else:
                signal = "HOLD"
                recommendation = "MANTENER"
            
            return {
                'symbol': symbol,
                'sma_short': float(sma_20),
                'sma_long': float(sma_50),
                'rsi': float(rsi),
                'signal': signal,
                'recommendation': recommendation
            }
            
        except Exception as e:
            raise Exception(f"Error calculando indicadores técnicos: {str(e)}")
    
    def calculate_risk_metrics(self, returns: pd.Series, confidence_level: float = 0.05) -> Dict[str, float]:
        """Calcula métricas de riesgo"""
        try:
            # VaR histórico
            var_hist = np.percentile(returns, confidence_level * 100)
            
            # CVaR histórico
            tail_losses = returns[returns <= var_hist]
            cvar_hist = tail_losses.mean() if len(tail_losses) > 0 else var_hist
            
            # Volatilidad
            volatility = returns.std() * np.sqrt(252)
            
            # Máximo drawdown
            cumulative = (1 + returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            return {
                'var': float(var_hist),
                'cvar': float(cvar_hist),
                'volatility': float(volatility),
                'max_drawdown': float(max_drawdown)
            }
            
        except Exception as e:
            raise Exception(f"Error calculando métricas de riesgo: {str(e)}")
    
    def calculate_capm(self, asset_returns: pd.Series, market_returns: pd.Series) -> Dict[str, float]:
        """Calcula análisis CAPM"""
        try:
            import statsmodels.api as sm
            
            # Regresión lineal
            X = sm.add_constant(market_returns)
            y = asset_returns
            
            model = sm.OLS(y, X).fit()
            
            alpha = model.params['const']
            beta = model.params[market_returns.name]
            r_squared = model.rsquared
            
            # Clasificación de riesgo
            if beta > 1.2:
                recommendation = "ALTO RIESGO (CÍCLICO)"
            elif beta > 1.0:
                recommendation = "RIESGO MODERADO"
            elif beta > 0.8:
                recommendation = "BAJO RIESGO"
            else:
                recommendation = "DEFENSIVO"
            
            return {
                'alpha': float(alpha),
                'beta': float(beta),
                'r_squared': float(r_squared),
                'recommendation': recommendation
            }
            
        except Exception as e:
            raise Exception(f"Error calculando CAPM: {str(e)}")
    
    def optimize_portfolio(self, returns: pd.DataFrame, target_return: Optional[float] = None) -> Dict[str, Any]:
        """Optimiza portafolio usando Markowitz"""
        try:
            expected_returns = returns.mean() * 252
            cov_matrix = returns.cov() * 252
            
            n_assets = len(returns.columns)
            
            # Restricciones
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = tuple((0.0, 0.4) for _ in range(n_assets))
            initial_weights = np.array([1/n_assets] * n_assets)
            
            # Portafolio de mínima varianza
            min_var_result = minimize(
                lambda w: np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))),
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            # Portafolio de máximo Sharpe
            risk_free_rate = 0.02
            max_sharpe_result = minimize(
                lambda w: -(np.sum(w * expected_returns) - risk_free_rate) / np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))),
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            # Métricas de portafolios
            min_var_return = np.sum(min_var_result.x * expected_returns)
            min_var_vol = np.sqrt(np.dot(min_var_result.x.T, np.dot(cov_matrix, min_var_result.x)))
            min_var_sharpe = (min_var_return - risk_free_rate) / min_var_vol
            
            max_sharpe_return = np.sum(max_sharpe_result.x * expected_returns)
            max_sharpe_vol = np.sqrt(np.dot(max_sharpe_result.x.T, np.dot(cov_matrix, max_sharpe_result.x)))
            max_sharpe_sharpe = (max_sharpe_return - risk_free_rate) / max_sharpe_vol
            
            weights_min_var = dict(zip(returns.columns, min_var_result.x))
            weights_max_sharpe = dict(zip(returns.columns, max_sharpe_result.x))
            
            return {
                'min_variance': {
                    'weights': weights_min_var,
                    'expected_return': float(min_var_return),
                    'volatility': float(min_var_vol),
                    'sharpe_ratio': float(min_var_sharpe)
                },
                'max_sharpe': {
                    'weights': weights_max_sharpe,
                    'expected_return': float(max_sharpe_return),
                    'volatility': float(max_sharpe_vol),
                    'sharpe_ratio': float(max_sharpe_sharpe)
                }
            }
            
        except Exception as e:
            raise Exception(f"Error optimizando portafolio: {str(e)}")
    
    def calculate_volatility(self, returns: pd.Series) -> Dict[str, Any]:
        """Calcula volatilidad histórica y GARCH"""
        try:
            # Volatilidad histórica
            hist_vol = returns.std() * np.sqrt(252)
            
            # Modelo GARCH
            try:
                am = arch_model(returns * 100, p=1, q=1, mean='Zero', vol='Garch', dist='normal')
                res = am.fit(disp='off')
                garch_vol = res.conditional_volatility.iloc[-1] / 100
                
                # Forecast
                forecasts = res.forecast(horizon=30)
                vol_forecast = forecasts.variance.iloc[-1].values / 10000
                vol_forecast = vol_forecast.tolist()
                
            except:
                garch_vol = hist_vol
                vol_forecast = [hist_vol] * 30
            
            return {
                'historical_volatility': float(hist_vol),
                'garch_volatility': float(garch_vol),
                'volatility_forecast': vol_forecast
            }
            
        except Exception as e:
            raise Exception(f"Error calculando volatilidad: {str(e)}")
    
    def generate_trading_signals(self, prices: pd.Series, symbol: str) -> Dict[str, Any]:
        """Genera señales de trading"""
        try:
            # Señales SMA
            sma_20 = prices.rolling(20).mean()
            sma_50 = prices.rolling(50).mean()
            
            # Señales RSI
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Señal combinada
            sma_signal = 1 if sma_20.iloc[-1] > sma_50.iloc[-1] else -1
            rsi_signal = 1 if rsi.iloc[-1] < 30 else (-1 if rsi.iloc[-1] > 70 else 0)
            combined_signal = (sma_signal + rsi_signal) / 2
            
            if combined_signal > 0.3:
                signal_type = "BUY"
                confidence = combined_signal
            elif combined_signal < -0.3:
                signal_type = "SELL"
                confidence = abs(combined_signal)
            else:
                signal_type = "HOLD"
                confidence = 0.0
            
            return {
                'symbol': symbol,
                'signal_type': signal_type,
                'confidence': float(confidence),
                'price': float(prices.iloc[-1]),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Error generando señales de trading: {str(e)}")
    
    def compare_with_benchmark(self, returns: pd.Series, benchmark_returns: pd.Series) -> Dict[str, Any]:
        """Compara activo con benchmark"""
        try:
            import statsmodels.api as sm
            
            # Asegurar que ambos series tengan el mismo índice
            common_index = returns.index.intersection(benchmark_returns.index)
            if len(common_index) == 0:
                return {
                    'alpha': 0.0,
                    'beta': 0.0,
                    'tracking_error': 0.0,
                    'information_ratio': 0.0,
                    'outperformance': False
                }
            
            returns_aligned = returns.loc[common_index]
            benchmark_aligned = benchmark_returns.loc[common_index]
            
            # Regresión para alpha y beta
            X = sm.add_constant(benchmark_aligned)
            y = returns_aligned
            
            model = sm.OLS(y, X).fit()
            alpha = model.params['const']
            beta = model.params[benchmark_aligned.name]
            
            # Tracking error
            tracking_error = (returns_aligned - benchmark_aligned).std() * np.sqrt(252)
            
            # Information ratio
            info_ratio = alpha / tracking_error if tracking_error != 0 else 0
            
            # Outperformance
            outperformance = alpha > 0
            
            return {
                'alpha': float(alpha),
                'beta': float(beta),
                'tracking_error': float(tracking_error),
                'information_ratio': float(info_ratio),
                'outperformance': outperformance
            }
            
        except Exception as e:
            # Retornar valores por defecto en caso de error
            return {
                'alpha': 0.0,
                'beta': 0.0,
                'tracking_error': 0.0,
                'information_ratio': 0.0,
                'outperformance': False
            }
