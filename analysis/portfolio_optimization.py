"""
Módulo para optimización de portafolios según Markowitz
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from config import OPTIMIZATION_CONFIG, ANALYSIS_CONFIG


class PortfolioOptimization:
    """Clase para optimizar portafolios según Markowitz"""
    
    def __init__(self, returns_df, risk_free_rate=None):
        self.returns = returns_df
        self.risk_free_rate = risk_free_rate or ANALYSIS_CONFIG['risk_free_rate']
        self.n_assets = len(self.returns.columns)
        self.expected_returns = self.returns.mean() * 252  # Anualizado
        self.cov_matrix = self.returns.cov() * 252  # Anualizado
        self.correlation_matrix = self.returns.corr()
    
    def portfolio_performance(self, weights):
        """Calcula retorno y volatilidad de un portafolio"""
        weights = np.array(weights)
        
        # Retorno esperado
        portfolio_return = np.sum(weights * self.expected_returns)
        
        # Volatilidad (riesgo)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        
        # Sharpe ratio
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def negative_sharpe_ratio(self, weights):
        """Función objetivo para maximizar Sharpe ratio"""
        return -self.portfolio_performance(weights)[2]
    
    def portfolio_volatility(self, weights):
        """Función objetivo para minimizar volatilidad"""
        return self.portfolio_performance(weights)[1]
    
    def minimize_variance(self):
        """Optimiza para mínima varianza"""
        # Restricciones
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds
        bounds = tuple((OPTIMIZATION_CONFIG['min_weight'], OPTIMIZATION_CONFIG['max_weight']) 
                      for _ in range(self.n_assets))
        
        # Peso inicial
        initial_weights = np.array([1/self.n_assets] * self.n_assets)
        
        # Optimización
        result = minimize(
            self.portfolio_volatility,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def maximize_sharpe_ratio(self):
        """Optimiza para máximo Sharpe ratio"""
        # Restricciones
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds
        bounds = tuple((OPTIMIZATION_CONFIG['min_weight'], OPTIMIZATION_CONFIG['max_weight']) 
                      for _ in range(self.n_assets))
        
        # Peso inicial
        initial_weights = np.array([1/self.n_assets] * self.n_assets)
        
        # Optimización
        result = minimize(
            self.negative_sharpe_ratio,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def optimize_for_target_return(self, target_return):
        """Optimiza para un retorno objetivo"""
        # Restricciones
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.sum(x * self.expected_returns) - target_return}
        )
        
        # Bounds
        bounds = tuple((OPTIMIZATION_CONFIG['min_weight'], OPTIMIZATION_CONFIG['max_weight']) 
                      for _ in range(self.n_assets))
        
        # Peso inicial
        initial_weights = np.array([1/self.n_assets] * self.n_assets)
        
        # Optimización
        result = minimize(
            self.portfolio_volatility,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def generate_efficient_frontier(self, n_points=50):
        """Genera la frontera eficiente"""
        target_returns = np.linspace(
            self.expected_returns.min(), 
            self.expected_returns.max(), 
            n_points
        )
        
        efficient_portfolios = []
        
        for target in target_returns:
            try:
                weights = self.optimize_for_target_return(target)
                ret, vol, sharpe = self.portfolio_performance(weights)
                
                efficient_portfolios.append({
                    'weights': weights,
                    'return': ret,
                    'volatility': vol,
                    'sharpe': sharpe
                })
            except:
                continue
        
        return pd.DataFrame(efficient_portfolios)
    
    def calculate_equal_weights(self):
        """Portafolio con pesos iguales"""
        weights = np.array([1/self.n_assets] * self.n_assets)
        return weights
    
    def calculate_market_cap_weights(self):
        """Portafolio ponderado por capitalización de mercado"""
        # Para este ejemplo, asumimos pesos iguales
        # En una implementación real, usaríamos datos de market cap
        return self.calculate_equal_weights()
    
    def calculate_risk_parity(self):
        """Portafolio de paridad de riesgo"""
        def risk_parity_objective(weights):
            weights = np.array(weights)
            portfolio_vol = self.portfolio_volatility(weights)
            
            # Contribuciones al riesgo
            marginal_contrib = np.dot(self.cov_matrix, weights)
            risk_contrib = weights * marginal_contrib / portfolio_vol
            
            # Igualar contribuciones al riesgo
            target_contrib = np.ones(self.n_assets) / self.n_assets
            return np.sum((risk_contrib - target_contrib)**2)
        
        # Restricciones
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds
        bounds = tuple((0.01, 0.5) for _ in range(self.n_assets))
        
        # Peso inicial
        initial_weights = np.array([1/self.n_assets] * self.n_assets)
        
        # Optimización
        result = minimize(
            risk_parity_objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def get_optimal_portfolios(self):
        """Calcula diferentes portafolios óptimos"""
        portfolios = {}
        
        # Mínima varianza
        min_var_weights = self.minimize_variance()
        portfolios['min_variance'] = {
            'weights': min_var_weights,
            'return': self.portfolio_performance(min_var_weights)[0],
            'volatility': self.portfolio_performance(min_var_weights)[1],
            'sharpe': self.portfolio_performance(min_var_weights)[2]
        }
        
        # Máximo Sharpe
        max_sharpe_weights = self.maximize_sharpe_ratio()
        portfolios['max_sharpe'] = {
            'weights': max_sharpe_weights,
            'return': self.portfolio_performance(max_sharpe_weights)[0],
            'volatility': self.portfolio_performance(max_sharpe_weights)[1],
            'sharpe': self.portfolio_performance(max_sharpe_weights)[2]
        }
        
        # Pesos iguales
        equal_weights = self.calculate_equal_weights()
        portfolios['equal_weights'] = {
            'weights': equal_weights,
            'return': self.portfolio_performance(equal_weights)[0],
            'volatility': self.portfolio_performance(equal_weights)[1],
            'sharpe': self.portfolio_performance(equal_weights)[2]
        }
        
        # Paridad de riesgo
        risk_parity_weights = self.calculate_risk_parity()
        portfolios['risk_parity'] = {
            'weights': risk_parity_weights,
            'return': self.portfolio_performance(risk_parity_weights)[0],
            'volatility': self.portfolio_performance(risk_parity_weights)[1],
            'sharpe': self.portfolio_performance(risk_parity_weights)[2]
        }
        
        return portfolios
    
    def calculate_diversification_metrics(self, weights):
        """Calcula métricas de diversificación"""
        weights = np.array(weights)
        
        # Índice de Herfindahl-Hirschman (HHI)
        hhi = np.sum(weights**2)
        
        # Número efectivo de activos
        effective_assets = 1 / hhi
        
        # Concentración máxima
        max_weight = np.max(weights)
        
        return {
            'hhi': hhi,
            'effective_assets': effective_assets,
            'max_weight': max_weight,
            'diversification_ratio': effective_assets / self.n_assets
        }
    
    def generate_report(self):
        """Genera reporte completo de optimización"""
        print("📊 Optimización de Portafolio (Markowitz)")
        print("=" * 50)
        
        # Portafolios óptimos
        optimal_portfolios = self.get_optimal_portfolios()
        
        print("\n🎯 Portafolios Óptimos:")
        for name, portfolio in optimal_portfolios.items():
            print(f"\n{name.replace('_', ' ').title()}:")
            print(f"  Retorno: {portfolio['return']:.4f}")
            print(f"  Volatilidad: {portfolio['volatility']:.4f}")
            print(f"  Sharpe Ratio: {portfolio['sharpe']:.4f}")
            
            # Pesos
            weights_df = pd.DataFrame({
                'Activo': self.returns.columns,
                'Peso': portfolio['weights']
            })
            print(f"  Pesos:")
            for _, row in weights_df.iterrows():
                print(f"    {row['Activo']}: {row['Peso']:.4f}")
            
            # Métricas de diversificación
            diversification = self.calculate_diversification_metrics(portfolio['weights'])
            print(f"  Diversificación:")
            print(f"    HHI: {diversification['hhi']:.4f}")
            print(f"    Activos efectivos: {diversification['effective_assets']:.2f}")
        
        # Frontera eficiente
        print(f"\n📈 Frontera Eficiente:")
        efficient_frontier = self.generate_efficient_frontier()
        
        if not efficient_frontier.empty:
            print(f"  Puntos en frontera: {len(efficient_frontier)}")
            print(f"  Retorno máximo: {efficient_frontier['return'].max():.4f}")
            print(f"  Volatilidad mínima: {efficient_frontier['volatility'].min():.4f}")
        
        return {
            'optimal_portfolios': optimal_portfolios,
            'efficient_frontier': efficient_frontier,
            'expected_returns': self.expected_returns,
            'cov_matrix': self.cov_matrix,
            'correlation_matrix': self.correlation_matrix
        }


def optimize_portfolio(returns_df, risk_free_rate=None):
    """Función principal para optimización de portafolios"""
    po = PortfolioOptimization(returns_df, risk_free_rate)
    return po.generate_report()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass