"""
Módulo para funciones de visualización y plotting
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class PlottingUtils:
    """Clase para funciones de visualización"""
    
    def __init__(self):
        self.colors = {
            'AAPL': '#007AFF',
            'MSFT': '#00BCF2', 
            'XOM': '#FF9500',
            'KO': '#F44336',
            'SPY': '#4CAF50'
        }
    
    def plot_price_chart(self, prices_df, symbol):
        """Gráfico de precios de un activo"""
        fig = go.Figure()
        
        # Precio de cierre
        fig.add_trace(go.Scatter(
            x=prices_df.index,
            y=prices_df[symbol],
            mode='lines',
            name=f'{symbol} Precio',
            line=dict(color=self.colors.get(symbol, '#2E86AB'), width=2)
        ))
        
        fig.update_layout(
            title=f'Precio de {symbol}',
            xaxis_title='Fecha',
            yaxis_title='Precio ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_technical_indicators(self, data, symbol):
        """Gráfico de indicadores técnicos"""
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Precio y Medias Móviles', 'RSI', 'MACD'),
            vertical_spacing=0.08,
            row_heights=[0.5, 0.25, 0.25]
        )
        
        # Precio y medias móviles
        fig.add_trace(go.Scatter(
            x=data.index, y=data[symbol], mode='lines', name='Precio',
            line=dict(color='black', width=2)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['SMA_Short'], mode='lines', name='SMA 20',
            line=dict(color='orange', width=1)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['SMA_Long'], mode='lines', name='SMA 50',
            line=dict(color='red', width=1)
        ), row=1, col=1)
        
        # RSI
        fig.add_trace(go.Scatter(
            x=data.index, y=data['RSI'], mode='lines', name='RSI',
            line=dict(color='purple', width=2)
        ), row=2, col=1)
        
        # Líneas de sobrecompra/sobreventa
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        fig.add_trace(go.Scatter(
            x=data.index, y=data['MACD'], mode='lines', name='MACD',
            line=dict(color='blue', width=2)
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['MACD_Signal'], mode='lines', name='Signal',
            line=dict(color='red', width=1)
        ), row=3, col=1)
        
        fig.update_layout(
            height=600,
            title_text=f'Análisis Técnico - {symbol}',
            template='plotly_white'
        )
        
        return fig
    
    def plot_returns_distribution(self, returns_df, symbol):
        """Gráfico de distribución de retornos"""
        fig = go.Figure()
        
        # Histograma
        fig.add_trace(go.Histogram(
            x=returns_df[symbol],
            nbinsx=50,
            name=f'Retornos {symbol}',
            opacity=0.7,
            marker_color=self.colors.get(symbol, '#2E86AB')
        ))
        
        fig.update_layout(
            title=f'Distribución de Retornos - {symbol}',
            xaxis_title='Retorno',
            yaxis_title='Frecuencia',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_correlation_matrix(self, correlation_matrix):
        """Gráfico de matriz de correlación"""
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=correlation_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Matriz de Correlación de Retornos',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def plot_efficient_frontier(self, efficient_frontier, optimal_portfolios):
        """Gráfico de frontera eficiente"""
        fig = go.Figure()
        
        # Frontera eficiente
        fig.add_trace(go.Scatter(
            x=efficient_frontier['volatility'],
            y=efficient_frontier['return'],
            mode='lines',
            name='Frontera Eficiente',
            line=dict(color='blue', width=3)
        ))
        
        # Portafolios óptimos
        for name, portfolio in optimal_portfolios.items():
            fig.add_trace(go.Scatter(
                x=[portfolio['volatility']],
                y=[portfolio['return']],
                mode='markers',
                name=name.replace('_', ' ').title(),
                marker=dict(size=10, symbol='star')
            ))
        
        fig.update_layout(
            title='Frontera Eficiente de Markowitz',
            xaxis_title='Volatilidad (Desviación Estándar)',
            yaxis_title='Retorno Esperado',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def plot_portfolio_weights(self, weights, portfolio_name):
        """Gráfico de pesos del portafolio"""
        fig = go.Figure(data=go.Pie(
            labels=list(weights.keys()),
            values=list(weights.values()),
            hole=0.3,
            colors=[self.colors.get(asset, f'rgb({np.random.randint(0,255)},{np.random.randint(0,255)},{np.random.randint(0,255)})') 
                   for asset in weights.keys()]
        ))
        
        fig.update_layout(
            title=f'Composición del Portafolio - {portfolio_name}',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_risk_metrics(self, risk_metrics_df):
        """Gráfico de métricas de riesgo"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('VaR Histórico', 'CVaR Histórico', 'Volatilidad Anualizada', 'Sharpe Ratio'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        assets = risk_metrics_df.index
        
        # VaR
        fig.add_trace(go.Bar(
            x=assets, y=risk_metrics_df['var_historical'],
            name='VaR Histórico',
            marker_color='red'
        ), row=1, col=1)
        
        # CVaR
        fig.add_trace(go.Bar(
            x=assets, y=risk_metrics_df['cvar_historical'],
            name='CVaR Histórico',
            marker_color='darkred'
        ), row=1, col=2)
        
        # Volatilidad
        fig.add_trace(go.Bar(
            x=assets, y=risk_metrics_df['annual_volatility'],
            name='Volatilidad Anualizada',
            marker_color='orange'
        ), row=2, col=1)
        
        # Sharpe
        fig.add_trace(go.Bar(
            x=assets, y=risk_metrics_df['sharpe_ratio'],
            name='Sharpe Ratio',
            marker_color='green'
        ), row=2, col=2)
        
        fig.update_layout(
            height=600,
            title_text='Métricas de Riesgo por Activo',
            template='plotly_white'
        )
        
        return fig
    
    def plot_trading_signals(self, signals_data, symbol):
        """Gráfico de señales de trading"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(f'Precio y Señales - {symbol}', 'RSI'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Precio y señales
        fig.add_trace(go.Scatter(
            x=signals_data.index, y=signals_data['price'],
            mode='lines', name='Precio',
            line=dict(color='black', width=2)
        ), row=1, col=1)
        
        # Señales de compra
        buy_signals = signals_data[signals_data['signal'] == 1]
        fig.add_trace(go.Scatter(
            x=buy_signals.index, y=buy_signals['price'],
            mode='markers', name='Señal de Compra',
            marker=dict(color='green', symbol='triangle-up', size=8)
        ), row=1, col=1)
        
        # Señales de venta
        sell_signals = signals_data[signals_data['signal'] == -1]
        fig.add_trace(go.Scatter(
            x=sell_signals.index, y=sell_signals['price'],
            mode='markers', name='Señal de Venta',
            marker=dict(color='red', symbol='triangle-down', size=8)
        ), row=1, col=1)
        
        # RSI
        fig.add_trace(go.Scatter(
            x=signals_data.index, y=signals_data['rsi'],
            mode='lines', name='RSI',
            line=dict(color='purple', width=2)
        ), row=2, col=1)
        
        # Líneas de sobrecompra/sobreventa
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        fig.update_layout(
            height=500,
            title_text=f'Señales de Trading - {symbol}',
            template='plotly_white'
        )
        
        return fig
    
    def plot_cumulative_returns(self, returns_df, portfolio_returns=None):
        """Gráfico de retornos acumulados"""
        fig = go.Figure()
        
        # Retornos acumulados de activos individuales
        for symbol in returns_df.columns:
            cumulative = (1 + returns_df[symbol]).cumprod() - 1
            fig.add_trace(go.Scatter(
                x=cumulative.index,
                y=cumulative,
                mode='lines',
                name=symbol,
                line=dict(color=self.colors.get(symbol, None))
            ))
        
        # Retorno acumulado del portafolio (si se proporciona)
        if portfolio_returns is not None:
            portfolio_cumulative = (1 + portfolio_returns).cumprod() - 1
            fig.add_trace(go.Scatter(
                x=portfolio_cumulative.index,
                y=portfolio_cumulative,
                mode='lines',
                name='Portafolio',
                line=dict(color='black', width=3)
            ))
        
        fig.update_layout(
            title='Retornos Acumulados',
            xaxis_title='Fecha',
            yaxis_title='Retorno Acumulado',
            template='plotly_white',
            height=500
        )
        
        return fig


def create_dashboard_plots():
    """Función para crear instancias de plotting"""
    return PlottingUtils()


if __name__ == "__main__":
    # Este módulo se importará desde otros archivos
    pass