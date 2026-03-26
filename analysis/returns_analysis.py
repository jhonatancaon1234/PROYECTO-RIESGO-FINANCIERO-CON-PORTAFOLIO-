"""
Módulo para análisis de rendimientos financieros
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from config import ANALYSIS_CONFIG


class ReturnsAnalysis:
    """Clase para analizar rendimientos financieros"""
    
    def __init__(self, returns_df):
        self.returns = returns_df
    
    def calculate_basic_statistics(self):
        """Calcula estadísticas básicas de rendimientos"""
        stats_dict = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            stats_dict[column] = {
                'media': series.mean(),
                'mediana': series.median(),
                'desviacion': series.std(),
                'varianza': series.var(),
                'asimetria': stats.skew(series),
                'kurtosis': stats.kurtosis(series),
                'min': series.min(),
                'max': series.max(),
                'q_05': series.quantile(0.05),
                'q_95': series.quantile(0.95),
                'jarque_bera': stats.jarque_bera(series),
                'shapiro': stats.shapiro(series)
            }
        
        return pd.DataFrame(stats_dict).T
    
    def calculate_annualized_metrics(self):
        """Calcula métricas anualizadas"""
        trading_days = 252
        
        metrics = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            # Métricas diarias
            daily_mean = series.mean()
            daily_std = series.std()
            
            # Métricas anualizadas
            annual_mean = daily_mean * trading_days
            annual_std = daily_std * np.sqrt(trading_days)
            annual_var = annual_std ** 2
            sharpe_ratio = annual_mean / annual_std if annual_std != 0 else 0
            
            # Sortino ratio (solo volatilidad a la baja)
            downside_returns = series[series < 0]
            downside_dev = downside_returns.std() if len(downside_returns) > 0 else 0
            sortino_ratio = annual_mean / (downside_dev * np.sqrt(trading_days)) if downside_dev > 0 else 0
            
            metrics[column] = {
                'retorno_diario': daily_mean,
                'volatilidad_diaria': daily_std,
                'retorno_anual': annual_mean,
                'volatilidad_anual': annual_std,
                'varianza_anual': annual_var,
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio
            }
        
        return pd.DataFrame(metrics).T
    
    def test_normality(self):
        """Prueba de normalidad de los rendimientos"""
        normality_tests = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            # Prueba de Jarque-Bera
            jb_stat, jb_p_value = stats.jarque_bera(series)
            
            # Prueba de Shapiro-Wilk
            sw_stat, sw_p_value = stats.shapiro(series)
            
            # Prueba de Kolmogorov-Smirnov
            ks_stat, ks_p_value = stats.kstest(series, 'norm')
            
            normality_tests[column] = {
                'jarque_bera_stat': jb_stat,
                'jarque_bera_p': jb_p_value,
                'shapiro_stat': sw_stat,
                'shapiro_p': sw_p_value,
                'ks_stat': ks_stat,
                'ks_p': ks_p_value,
                'normal_jb': jb_p_value > 0.05,
                'normal_sw': sw_p_value > 0.05,
                'normal_ks': ks_p_value > 0.05
            }
        
        return pd.DataFrame(normality_tests).T
    
    def calculate_drawdown(self):
        """Calcula el drawdown máximo"""
        drawdowns = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            # Rendimientos acumulados
            cumulative = (1 + series).cumprod()
            
            # Drawdown
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            
            drawdowns[column] = {
                'max_drawdown': drawdown.min(),
                'max_drawdown_date': drawdown.idxmin(),
                'current_drawdown': drawdown.iloc[-1],
                'days_under_water': (drawdown < 0).sum(),
                'recovery_days': self._calculate_recovery_days(drawdown)
            }
        
        return pd.DataFrame(drawdowns).T
    
    def _calculate_recovery_days(self, drawdown):
        """Calcula días para recuperarse del drawdown"""
        if drawdown.iloc[-1] >= 0:
            return 0
        
        # Encontrar el último máximo antes del mínimo
        min_idx = drawdown.idxmin()
        max_before = drawdown.loc[:min_idx].idxmax()
        
        # Contar días hasta recuperarse
        recovery_start = min_idx
        for i in range(min_idx + 1, len(drawdown)):
            if drawdown.iloc[i] >= 0:
                return i - min_idx
        
        return len(drawdown) - min_idx
    
    def get_distribution_analysis(self):
        """Análisis de distribución de rendimientos"""
        analysis = {}
        
        for column in self.returns.columns:
            series = self.returns[column].dropna()
            
            # Percentiles
            percentiles = series.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
            
            # Valor en riesgo (VaR) histórico
            var_95 = series.quantile(0.05)
            var_99 = series.quantile(0.01)
            
            # Expected Shortfall (ES)
            es_95 = series[series <= var_95].mean()
            es_99 = series[series <= var_99].mean()
            
            analysis[column] = {
                'percentiles': percentiles,
                'var_95': var_95,
                'var_99': var_99,
                'es_95': es_95,
                'es_99': es_99,
                'tail_ratio': series.quantile(0.95) / abs(series.quantile(0.05))
            }
        
        return analysis
    
    def generate_report(self):
        """Genera un reporte completo de análisis de rendimientos"""
        basic_stats = self.calculate_basic_statistics()
        annual_metrics = self.calculate_annualized_metrics()
        normality = self.test_normality()
        drawdown = self.calculate_drawdown()
        distribution = self.get_distribution_analysis()
        
        print("📊 Análisis de Rendimientos")
        print("=" * 50)
        
        print("\n📈 Estadísticas Básicas:")
        print(basic_stats.round(4))
        
        print("\n🎯 Métricas Anualizadas:")
        print(annual_metrics.round(4))
        
        print("\n🧪 Pruebas de Normalidad:")
        print("Jarque-Bera (p-value):")
        print(normality['jarque_bera_p'].round(4))
        print("Shapiro-Wilk (p-value):")
        print(normality['shapiro_p'].round(4))
        
        print("\n📉 Drawdown Máximo:")
        print(drawdown.round(4))
        
        return {
            'basic_statistics': basic_stats,
            'annual_metrics': annual_metrics,
            'normality_tests': normality,
            'drawdown_analysis': drawdown,
            'distribution_analysis': distribution
        }


def analyze_returns(returns_df):
    """Función principal para análisis de rendimientos"""
    ra = ReturnsAnalysis(returns_df)
    return ra.generate_report()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass