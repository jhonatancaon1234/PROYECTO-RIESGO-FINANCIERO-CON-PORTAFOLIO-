"""
Módulo para análisis CAPM (Capital Asset Pricing Model)
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from config import ANALYSIS_CONFIG


class CAPMAnalysis:
    """Clase para análisis CAPM"""
    
    def __init__(self, returns_df, risk_free_rate=None):
        self.returns = returns_df
        self.risk_free_rate = risk_free_rate or ANALYSIS_CONFIG['risk_free_rate']
        self.market_returns = None
        self.excess_returns = None
        self.betas = {}
        self.regressions = {}
    
    def prepare_data(self):
        """Prepara los datos para el análisis CAPM"""
        # Asumimos que SPY es el mercado
        if 'SPY' not in self.returns.columns:
            raise ValueError("SPY (S&P 500 ETF) no encontrado en los datos")
        
        # Retornos del mercado (SPY)
        self.market_returns = self.returns['SPY'].dropna()
        
        # Retornos excedentes (exceso sobre tasa libre de riesgo)
        self.excess_returns = self.returns.subtract(self.risk_free_rate / 252, axis=0)
        
        # Retornos excedentes del mercado
        market_excess = self.market_returns - (self.risk_free_rate / 252)
        
        return market_excess
    
    def calculate_beta(self, asset_returns, market_returns):
        """Calcula el Beta de un activo"""
        # Regresión lineal: R_i - R_f = α + β(R_m - R_f) + ε
        
        # Exceso de retornos
        asset_excess = asset_returns - (self.risk_free_rate / 252)
        market_excess = market_returns - (self.risk_free_rate / 252)
        
        # Alinear datos
        aligned_data = pd.concat([asset_excess, market_excess], axis=1).dropna()
        aligned_data.columns = ['asset', 'market']
        
        if len(aligned_data) < 30:  # Mínimo 30 observaciones
            return None, None, None
        
        # Regresión
        X = sm.add_constant(aligned_data['market'])
        y = aligned_data['asset']
        
        model = sm.OLS(y, X).fit()
        
        beta = model.params['market']
        alpha = model.params['const']
        r_squared = model.rsquared
        
        return beta, alpha, r_squared
    
    def calculate_all_betas(self):
        """Calcula el Beta para todos los activos"""
        market_excess = self.prepare_data()
        
        for symbol in self.returns.columns:
            if symbol == 'SPY':  # El mercado no tiene beta consigo mismo
                continue
            
            try:
                beta, alpha, r_squared = self.calculate_beta(
                    self.returns[symbol], 
                    self.market_returns
                )
                
                if beta is not None:
                    self.betas[symbol] = {
                        'beta': beta,
                        'alpha': alpha,
                        'r_squared': r_squared,
                        'classification': self._classify_beta(beta)
                    }
                    
                    print(f"✓ Beta calculado para {symbol}: {beta:.4f}")
                else:
                    print(f"✗ No se pudo calcular beta para {symbol}")
                    
            except Exception as e:
                print(f"✗ Error calculando beta para {symbol}: {str(e)}")
    
    def _classify_beta(self, beta):
        """Clasifica el beta según su valor"""
        if beta > 1.2:
            return "Alto Riesgo (Cíclico)"
        elif beta > 1.0:
            return "Riesgo Moderado"
        elif beta > 0.8:
            return "Riesgo Bajo"
        elif beta > 0.5:
            return "Muy Bajo Riesgo"
        else:
            return "Defensivo"
    
    def calculate_expected_returns(self):
        """Calcula retornos esperados según CAPM"""
        expected_returns = {}
        
        for symbol, beta_info in self.betas.items():
            beta = beta_info['beta']
            
            # CAPM: E(R_i) = R_f + β_i * (E(R_m) - R_f)
            market_premium = self.market_returns.mean() * 252 - self.risk_free_rate
            expected_return = self.risk_free_rate + beta * market_premium
            
            expected_returns[symbol] = {
                'expected_return': expected_return,
                'market_premium': market_premium,
                'beta': beta
            }
        
        return expected_returns
    
    def calculate_treynor_ratio(self):
        """Calcula el ratio de Treynor para cada activo"""
        treynor_ratios = {}
        
        # Retorno anualizado del mercado
        market_return_annual = self.market_returns.mean() * 252
        
        for symbol, beta_info in self.betas.items():
            beta = beta_info['beta']
            
            # Retorno anualizado del activo
            asset_return_annual = self.returns[symbol].mean() * 252
            
            # Ratio de Treynor: (R_p - R_f) / β_p
            treynor = (asset_return_annual - self.risk_free_rate) / beta if beta != 0 else 0
            
            treynor_ratios[symbol] = {
                'treynor_ratio': treynor,
                'asset_return': asset_return_annual,
                'beta': beta
            }
        
        return treynor_ratios
    
    def get_capm_summary(self):
        """Genera un resumen del análisis CAPM"""
        betas_df = pd.DataFrame(self.betas).T
        
        expected_returns = self.calculate_expected_returns()
        treynor_ratios = self.calculate_treynor_ratio()
        
        # Crear DataFrame de resultados
        summary = pd.DataFrame({
            'Beta': betas_df['beta'],
            'Alpha': betas_df['alpha'],
            'R_squared': betas_df['r_squared'],
            'Classification': betas_df['classification'],
            'Expected_Return': [expected_returns[s]['expected_return'] for s in betas_df.index],
            'Treynor_Ratio': [treynor_ratios[s]['treynor_ratio'] for s in betas_df.index]
        })
        
        return summary
    
    def generate_report(self):
        """Genera reporte completo de análisis CAPM"""
        print("📊 Análisis CAPM (Capital Asset Pricing Model)")
        print("=" * 60)
        
        # Calcular betas
        self.calculate_all_betas()
        
        # Resumen
        summary = self.get_capm_summary()
        
        print("\n📈 Betas y Clasificación de Riesgo:")
        print(summary.round(4))
        
        print(f"\n🎯 Métricas del Mercado (SPY):")
        print(f"  Retorno anualizado: {self.market_returns.mean() * 252:.4f}")
        print(f"  Volatilidad anualizada: {self.market_returns.std() * np.sqrt(252):.4f}")
        print(f"  Prima de riesgo: {(self.market_returns.mean() * 252) - self.risk_free_rate:.4f}")
        print(f"  Tasa libre de riesgo: {self.risk_free_rate:.4f}")
        
        print(f"\n🔍 Interpretación de Betas:")
        for symbol, beta_info in self.betas.items():
            beta = beta_info['beta']
            classification = beta_info['classification']
            print(f"  {symbol}: β={beta:.4f} - {classification}")
        
        return {
            'betas': self.betas,
            'summary': summary,
            'expected_returns': self.calculate_expected_returns(),
            'treynor_ratios': self.calculate_treynor_ratios()
        }


def analyze_capm(returns_df, risk_free_rate=None):
    """Función principal para análisis CAPM"""
    capm = CAPMAnalysis(returns_df, risk_free_rate)
    return capm.generate_report()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass