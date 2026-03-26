"""
Módulo para cálculo de métricas de riesgo: VaR y CVaR
"""

import pandas as pd
import numpy as np
from scipy import stats
from arch import arch_model
from config import ANALYSIS_CONFIG


class RiskMetrics:
    """Clase para calcular métricas de riesgo"""
    
    def __init__(self, returns_df, confidence_level=None):
        self.returns = returns_df
        self.confidence_level = confidence_level or ANALYSIS_CONFIG['confidence_level']
        self.lookback_period = ANALYSIS_CONFIG['lookback_period']
    
    def calculate_var_historical(self, returns_series, confidence_level=None):
        """Calcula VaR histórico"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        # VaR histórico: percentil del nivel de confianza
        var = np.percentile(returns_series, confidence_level * 100)
        
        return var
    
    def calculate_var_parametric(self, returns_series, confidence_level=None):
        """Calcula VaR paramétrico (asumiendo distribución normal)"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        # Media y desviación estándar
        mean = returns_series.mean()
        std = returns_series.std()
        
        # VaR paramétrico
        z_score = stats.norm.ppf(confidence_level)
        var = mean + z_score * std
        
        return var
    
    def calculate_var_garch(self, returns_series, confidence_level=None, horizon=1):
        """Calcula VaR usando modelo GARCH"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        try:
            # Ajustar modelo GARCH
            model = arch_model(returns_series * 100, p=1, q=1, mean='Zero', vol='Garch', dist='normal')
            fitted_model = model.fit(disp='off')
            
            # Pronosticar volatilidad
            forecast = fitted_model.forecast(horizon=horizon)
            conditional_vol = np.sqrt(forecast.variance.iloc[-1]) / 100
            
            # VaR GARCH
            z_score = stats.norm.ppf(confidence_level)
            var = z_score * conditional_vol
            
            return var
            
        except Exception as e:
            print(f"Error calculando VaR GARCH: {str(e)}")
            return None
    
    def calculate_cvar_historical(self, returns_series, confidence_level=None):
        """Calcula CVaR (Expected Shortfall) histórico"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        # VaR histórico
        var = self.calculate_var_historical(returns_series, confidence_level)
        
        # CVaR: media de las pérdidas que exceden el VaR
        tail_losses = returns_series[returns_series <= var]
        
        if len(tail_losses) > 0:
            cvar = tail_losses.mean()
        else:
            cvar = var
        
        return cvar
    
    def calculate_cvar_parametric(self, returns_series, confidence_level=None):
        """Calcula CVaR paramétrico (distribución normal)"""
        if confidence_level is None:
            confidence_level = self.confidence_level
        
        # Media y desviación estándar
        mean = returns_series.mean()
        std = returns_series.std()
        
        # VaR paramétrico
        var = self.calculate_var_parametric(returns_series, confidence_level)
        
        # CVaR paramétrico
        z_score = stats.norm.ppf(confidence_level)
        cvar = mean - (std * stats.norm.pdf(z_score) / confidence_level)
        
        return cvar
    
    def calculate_all_risk_metrics(self, symbol):
        """Calcula todas las métricas de riesgo para un activo"""
        if symbol not in self.returns.columns:
            return None
        
        returns = self.returns[symbol].dropna()
        
        # Calcular métricas
        var_hist = self.calculate_var_historical(returns)
        var_param = self.calculate_var_parametric(returns)
        var_garch = self.calculate_var_garch(returns)
        
        cvar_hist = self.calculate_cvar_historical(returns)
        cvar_param = self.calculate_cvar_parametric(returns)
        
        # Métricas de volatilidad
        daily_vol = returns.std()
        annual_vol = daily_vol * np.sqrt(252)
        
        # Sharpe ratio
        sharpe = returns.mean() / daily_vol * np.sqrt(252)
        
        return {
            'var_historical': var_hist,
            'var_parametric': var_param,
            'var_garch': var_garch,
            'cvar_historical': cvar_hist,
            'cvar_parametric': cvar_param,
            'daily_volatility': daily_vol,
            'annual_volatility': annual_vol,
            'sharpe_ratio': sharpe,
            'confidence_level': confidence_level
        }
    
    def calculate_portfolio_var(self, weights, method='historical'):
        """Calcula VaR del portafolio"""
        # Retornos del portafolio
        portfolio_returns = (self.returns * weights).sum(axis=1)
        
        if method == 'historical':
            var = self.calculate_var_historical(portfolio_returns)
        elif method == 'parametric':
            var = self.calculate_var_parametric(portfolio_returns)
        else:
            var = None
        
        # CVaR del portafolio
        cvar = self.calculate_cvar_historical(portfolio_returns)
        
        return var, cvar
    
    def calculate_marginal_var(self, weights):
        """Calcula VaR marginal para cada activo"""
        portfolio_var, _ = self.calculate_portfolio_var(weights, 'historical')
        
        marginal_var = {}
        
        for symbol in self.returns.columns:
            # Pequeño cambio en el peso
            delta = 0.001
            new_weights = weights.copy()
            new_weights[symbol] += delta
            
            # Nuevo VaR
            new_var, _ = self.calculate_portfolio_var(new_weights, 'historical')
            
            # VaR marginal
            marginal_var[symbol] = (new_var - portfolio_var) / delta
        
        return marginal_var
    
    def calculate_component_var(self, weights):
        """Calcula VaR componente para cada activo"""
        marginal_var = self.calculate_marginal_var(weights)
        portfolio_var, _ = self.calculate_portfolio_var(weights, 'historical')
        
        component_var = {}
        
        for symbol in self.returns.columns:
            component_var[symbol] = weights[symbol] * marginal_var[symbol]
        
        return component_var
    
    def get_risk_report(self):
        """Genera reporte completo de métricas de riesgo"""
        print("📊 Métricas de Riesgo (VaR y CVaR)")
        print("=" * 50)
        
        # Métricas individuales
        individual_metrics = {}
        
        for symbol in self.returns.columns:
            metrics = self.calculate_all_risk_metrics(symbol)
            if metrics:
                individual_metrics[symbol] = metrics
        
        # Crear DataFrame
        metrics_df = pd.DataFrame(individual_metrics).T
        
        print(f"\n📈 Métricas de Riesgo Individuales (Confianza: {self.confidence_level*100:.0f}%):")
        print(metrics_df.round(4))
        
        # Resumen de riesgo
        print(f"\n🎯 Resumen de Riesgo:")
        print(f"  VaR Histórico Promedio: {metrics_df['var_historical'].mean():.4f}")
        print(f"  CVaR Histórico Promedio: {metrics_df['cvar_historical'].mean():.4f}")
        print(f"  Volatilidad Anualizada Promedio: {metrics_df['annual_volatility'].mean():.4f}")
        
        return {
            'individual_metrics': individual_metrics,
            'metrics_df': metrics_df,
            'confidence_level': self.confidence_level
        }
    
    def calculate_backtesting(self, symbol, window=252):
        """Realiza backtesting de VaR"""
        if symbol not in self.returns.columns:
            return None
        
        returns = self.returns[symbol].dropna()
        
        # Calcular VaR con ventana móvil
        var_values = []
        actual_returns = []
        
        for i in range(window, len(returns)):
            window_data = returns.iloc[i-window:i]
            
            # VaR histórico
            var = self.calculate_var_historical(window_data)
            
            # Retorno real
            actual_return = returns.iloc[i]
            
            var_values.append(var)
            actual_returns.append(actual_return)
        
        # Contar excesos
        violations = sum([1 for i in range(len(actual_returns)) 
                         if actual_returns[i] < var_values[i]])
        
        violation_rate = violations / len(actual_returns)
        
        return {
            'violations': violations,
            'violation_rate': violation_rate,
            'expected_violations': self.confidence_level,
            'var_values': var_values,
            'actual_returns': actual_returns
        }


def calculate_risk_metrics(returns_df, confidence_level=None):
    """Función principal para cálculo de métricas de riesgo"""
    rm = RiskMetrics(returns_df, confidence_level)
    return rm.get_risk_report()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass