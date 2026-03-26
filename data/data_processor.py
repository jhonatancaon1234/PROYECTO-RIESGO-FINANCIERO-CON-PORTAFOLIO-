"""
Módulo para procesar y transformar datos financieros
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta


class DataProcessor:
    """Clase para procesar datos financieros"""
    
    def __init__(self, prices_df, returns_df):
        self.prices = prices_df
        self.returns = returns_df
    
    def calculate_basic_stats(self):
        """Calcula estadísticas básicas de los retornos"""
        stats_dict = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            stats_dict[column] = {
                'media': series.mean(),
                'desviacion': series.std(),
                'varianza': series.var(),
                'skewness': stats.skew(series),
                'kurtosis': stats.kurtosis(series),
                'jarque_bera': stats.jarque_bera(series),
                'min': series.min(),
                'max': series.max(),
                'q_05': series.quantile(0.05),
                'q_95': series.quantile(0.95)
            }
        
        return pd.DataFrame(stats_dict).T
    
    def calculate_cumulative_returns(self):
        """Calcula retornos acumulados"""
        return (1 + self.returns).cumprod() - 1
    
    def calculate_annualized_stats(self):
        """Calcula estadísticas anualizadas"""
        trading_days = 252  # Días hábiles al año
        
        annual_stats = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            # Estadísticas anualizadas
            annual_mean = series.mean() * trading_days
            annual_std = series.std() * np.sqrt(trading_days)
            annual_var = annual_std ** 2
            sharpe_ratio = annual_mean / annual_std if annual_std != 0 else 0
            
            annual_stats[column] = {
                'retorno_anual': annual_mean,
                'volatilidad_anual': annual_std,
                'varianza_anual': annual_var,
                'sharpe_ratio': sharpe_ratio
            }
        
        return pd.DataFrame(annual_stats).T
    
    def calculate_correlation_matrix(self):
        """Calcula matriz de correlación de retornos"""
        return self.returns.corr()
    
    def calculate_covariance_matrix(self):
        """Calcula matriz de covarianza de retornos"""
        return self.returns.cov()
    
    def get_summary_report(self):
        """Genera un reporte resumen de los datos"""
        basic_stats = self.calculate_basic_stats()
        annual_stats = self.calculate_annualized_stats()
        correlation = self.calculate_correlation_matrix()
        
        report = {
            'basic_stats': basic_stats,
            'annual_stats': annual_stats,
            'correlation_matrix': correlation,
            'data_shape': self.returns.shape,
            'date_range': {
                'inicio': self.returns.index[0],
                'fin': self.returns.index[-1]
            }
        }
        
        return report


def process_financial_data(prices_df, returns_df):
    """Función principal para procesar datos financieros"""
    processor = DataProcessor(prices_df, returns_df)
    
    # Calcular estadísticas
    basic_stats = processor.calculate_basic_stats()
    annual_stats = processor.calculate_annualized_stats()
    correlation = processor.calculate_correlation_matrix()
    covariance = processor.calculate_covariance_matrix()
    
    print("📊 Estadísticas básicas de retornos:")
    print(basic_stats.round(4))
    
    print("\n📈 Estadísticas anualizadas:")
    print(annual_stats.round(4))
    
    print("\n🔗 Matriz de correlación:")
    print(correlation.round(3))
    
    return {
        'basic_stats': basic_stats,
        'annual_stats': annual_stats,
        'correlation': correlation,
        'covariance': covariance,
        'processor': processor
    }


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass