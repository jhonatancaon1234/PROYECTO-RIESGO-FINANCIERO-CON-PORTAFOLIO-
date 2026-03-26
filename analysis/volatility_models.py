"""
Módulo para modelar volatilidad con modelos ARCH/GARCH
"""

import pandas as pd
import numpy as np
from arch import arch_model
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from config import GARCH_CONFIG, ANALYSIS_CONFIG


class VolatilityModels:
    """Clase para modelar volatilidad con ARCH/GARCH"""
    
    def __init__(self, returns_df):
        self.returns = returns_df
        self.models = {}
        self.fitted_models = {}
    
    def fit_garch_model(self, symbol, p=1, q=1, mean='Zero', vol='Garch', dist='normal'):
        """Ajusta un modelo GARCH a un activo específico"""
        if symbol not in self.returns.columns:
            return None
        
        # Obtener retornos del activo
        returns = self.returns[symbol].dropna()
        
        # Crear modelo ARCH
        model = arch_model(
            returns * 100,  # Escalar para mejor convergencia
            p=p,
            q=q,
            mean=mean,
            vol=vol,
            dist=dist
        )
        
        # Ajustar modelo
        fitted_model = model.fit(disp='off')
        
        # Guardar resultados
        self.models[symbol] = model
        self.fitted_models[symbol] = fitted_model
        
        return fitted_model
    
    def fit_all_models(self):
        """Ajusta modelos GARCH a todos los activos"""
        config = GARCH_CONFIG
        
        for symbol in self.returns.columns:
            try:
                model = self.fit_garch_model(
                    symbol,
                    p=config['p'],
                    q=config['q'],
                    mean=config['mean'],
                    vol=config['vol'],
                    dist=config['dist']
                )
                
                if model is not None:
                    print(f"✓ Modelo GARCH ajustado para {symbol}")
                else:
                    print(f"✗ No se pudo ajustar modelo para {symbol}")
                    
            except Exception as e:
                print(f"✗ Error ajustando modelo para {symbol}: {str(e)}")
    
    def get_model_summary(self, symbol):
        """Obtiene resumen del modelo ajustado"""
        if symbol not in self.fitted_models:
            return None
        
        model = self.fitted_models[symbol]
        
        # Métricas del modelo
        summary = {
            'aic': model.aic,
            'bic': model.bic,
            'log_likelihood': model.loglikelihood,
            'params': model.params,
            't_values': model.tvalues,
            'p_values': model.pvalues
        }
        
        return summary
    
    def forecast_volatility(self, symbol, horizon=10):
        """Pronostica volatilidad futura"""
        if symbol not in self.fitted_models:
            return None
        
        model = self.fitted_models[symbol]
        
        # Pronóstico
        forecast = model.forecast(horizon=horizon)
        
        # Volatilidad condicional
        conditional_vol = np.sqrt(forecast.variance.iloc[-1]) / 100  # Desescalar
        
        return conditional_vol
    
    def calculate_conditional_volatility(self, symbol):
        """Calcula volatilidad condicional histórica"""
        if symbol not in self.fitted_models:
            return None
        
        model = self.fitted_models[symbol]
        
        # Volatilidad condicional
        conditional_vol = model.conditional_volatility / 100  # Desescalar
        
        return conditional_vol
    
    def compare_models(self):
        """Compara diferentes especificaciones de modelos"""
        comparisons = {}
        
        for symbol in self.returns.columns:
            returns = self.returns[symbol].dropna()
            
            # Modelos a comparar
            models_to_test = [
                {'p': 1, 'q': 0, 'name': 'ARCH(1)'},
                {'p': 1, 'q': 1, 'name': 'GARCH(1,1)'},
                {'p': 2, 'q': 1, 'name': 'GARCH(2,1)'},
                {'p': 1, 'q': 2, 'name': 'GARCH(1,2)'}
            ]
            
            model_results = {}
            
            for model_spec in models_to_test:
                try:
                    model = arch_model(
                        returns * 100,
                        p=model_spec['p'],
                        q=model_spec['q'],
                        mean='Zero',
                        vol='Garch',
                        dist='normal'
                    )
                    
                    fitted = model.fit(disp='off')
                    
                    model_results[model_spec['name']] = {
                        'aic': fitted.aic,
                        'bic': fitted.bic,
                        'log_likelihood': fitted.loglikelihood,
                        'params': fitted.params
                    }
                    
                except Exception as e:
                    print(f"Error con modelo {model_spec['name']} para {symbol}: {str(e)}")
            
            comparisons[symbol] = model_results
        
        return comparisons
    
    def get_volatility_analysis(self):
        """Genera análisis completo de volatilidad"""
        analysis = {}
        
        for symbol in self.returns.columns:
            if symbol not in self.fitted_models:
                continue
            
            model = self.fitted_models[symbol]
            
            # Volatilidad condicional
            cond_vol = self.calculate_conditional_volatility(symbol)
            
            # Pronóstico a 10 días
            forecast_vol = self.forecast_volatility(symbol, horizon=10)
            
            # Métricas de volatilidad
            analysis[symbol] = {
                'conditional_volatility': cond_vol,
                'forecast_volatility': forecast_vol,
                'current_volatility': cond_vol.iloc[-1] if cond_vol is not None else None,
                'annualized_volatility': cond_vol.iloc[-1] * np.sqrt(252) if cond_vol is not None else None,
                'model_summary': self.get_model_summary(symbol)
            }
        
        return analysis
    
    def generate_report(self):
        """Genera reporte de análisis de volatilidad"""
        print("📊 Análisis de Volatilidad con GARCH")
        print("=" * 50)
        
        # Comparar modelos
        comparisons = self.compare_models()
        
        print("\n🔍 Comparación de Modelos:")
        for symbol, models in comparisons.items():
            print(f"\n{symbol}:")
            for model_name, results in models.items():
                print(f"  {model_name}: AIC={results['aic']:.2f}, BIC={results['bic']:.2f}")
        
        # Análisis de volatilidad
        volatility_analysis = self.get_volatility_analysis()
        
        print("\n📈 Análisis de Volatilidad:")
        for symbol, analysis in volatility_analysis.items():
            current_vol = analysis['current_volatility']
            annual_vol = analysis['annualized_volatility']
            
            if current_vol is not None:
                print(f"\n{symbol}:")
                print(f"  Volatilidad actual: {current_vol:.4f}")
                print(f"  Volatilidad anualizada: {annual_vol:.4f}")
        
        return {
            'model_comparisons': comparisons,
            'volatility_analysis': volatility_analysis,
            'fitted_models': self.fitted_models
        }


def analyze_volatility(returns_df):
    """Función principal para análisis de volatilidad"""
    vm = VolatilityModels(returns_df)
    vm.fit_all_models()
    return vm.generate_report()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass