"""
Dashboard de Análisis de Riesgo Financiero - Streamlit App
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importar módulos del proyecto
from data.data_loader import DataLoader, load_financial_data
from data.data_processor import DataProcessor, process_financial_data
from analysis.technical_analysis import TechnicalAnalysis, analyze_technical
from analysis.returns_analysis import ReturnsAnalysis, analyze_returns
from analysis.volatility_models import VolatilityModels, analyze_volatility
from analysis.capm_analysis import CAPMAnalysis, analyze_capm
from analysis.risk_metrics import RiskMetrics, calculate_risk_metrics
from analysis.portfolio_optimization import PortfolioOptimization, optimize_portfolio
from signals.trading_signals import TradingSignals, generate_trading_signals
from utils.plotting import PlottingUtils

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Riesgo Financiero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1E88E5;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
    }
    .positive {
        color: #2E7D32;
        font-weight: bold;
    }
    .negative {
        color: #C62828;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-header">📊 Dashboard de Riesgo Financiero</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 📈 Configuración")
st.sidebar.markdown("---")

# Selección de activos
assets = ['AAPL', 'MSFT', 'XOM', 'KO', 'SPY']
selected_assets = st.sidebar.multiselect(
    "Seleccionar Activos",
    options=assets,
    default=assets
)

# Período de análisis
period_options = {
    "6 meses": 180,
    "1 año": 365,
    "2 años": 730,
    "5 años": 1825
}
selected_period = st.sidebar.selectbox(
    "Período de Análisis",
    options=list(period_options.keys()),
    index=2
)

# Nivel de confianza para VaR
confidence_level = st.sidebar.slider(
    "Nivel de Confianza para VaR",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01
)

# Botón para cargar datos
if st.sidebar.button("🔄 Cargar Datos"):
    st.session_state.data_loaded = False

# Estado de carga de datos
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Carga de datos
if not st.session_state.data_loaded:
    with st.spinner('Cargando datos financieros...'):
        try:
            prices, returns = load_financial_data()
            if prices is not None and not prices.empty:
                st.session_state.prices = prices
                st.session_state.returns = returns
                st.session_state.data_loaded = True
                st.success("✅ Datos cargados exitosamente!")
            else:
                st.error("❌ No se pudieron cargar los datos financieros")
        except Exception as e:
            st.error(f"❌ Error al cargar datos: {str(e)}")

# Si los datos están cargados, mostrar el dashboard
if st.session_state.data_loaded:
    prices = st.session_state.prices
    returns = st.session_state.returns
    
    # Filtros de datos
    if selected_assets:
        prices = prices[selected_assets]
        returns = returns[selected_assets]
    
    # Resumen general
    st.markdown('<div class="sub-header">📈 Resumen General</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Número de Activos",
            value=len(returns.columns)
        )
    
    with col2:
        st.metric(
            label="📅 Días de Datos",
            value=len(returns)
        )
    
    with col3:
        st.metric(
            label="📅 Fecha Inicio",
            value=prices.index[0].strftime('%Y-%m-%d')
        )
    
    with col4:
        st.metric(
            label="📅 Fecha Fin",
            value=prices.index[-1].strftime('%Y-%m-%d')
        )
    
    # Pestañas del dashboard
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🔍 Análisis Técnico",
        "📊 Rendimientos", 
        "📈 Volatilidad",
        "🎯 CAPM",
        "⚠️ VaR & CVaR",
        "⚖️ Markowitz",
        "🎯 Señales",
        "🏆 Benchmark"
    ])
    
    # 1. Análisis Técnico
    with tab1:
        st.markdown('<div class="sub-header">🔍 Análisis Técnico</div>', unsafe_allow_html=True)
        
        # Selección de activo
        selected_symbol = st.selectbox("Seleccionar Activo", options=prices.columns, key="tech_symbol")
        
        if selected_symbol:
            # Gráfico de precios
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de precios con indicadores
                fig = go.Figure()
                
                # Precio
                fig.add_trace(go.Scatter(
                    x=prices.index,
                    y=prices[selected_symbol],
                    mode='lines',
                    name=f'{selected_symbol} Precio',
                    line=dict(color='#2E86AB', width=2)
                ))
                
                # Medias móviles
                sma_20 = prices[selected_symbol].rolling(window=20).mean()
                sma_50 = prices[selected_symbol].rolling(window=50).mean()
                
                fig.add_trace(go.Scatter(
                    x=prices.index,
                    y=sma_20,
                    mode='lines',
                    name='SMA 20',
                    line=dict(color='orange', width=1)
                ))
                
                fig.add_trace(go.Scatter(
                    x=prices.index,
                    y=sma_50,
                    mode='lines',
                    name='SMA 50',
                    line=dict(color='red', width=1)
                ))
                
                fig.update_layout(
                    title=f'Análisis Técnico - {selected_symbol}',
                    xaxis_title='Fecha',
                    yaxis_title='Precio ($)',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # RSI
                delta = prices[selected_symbol].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(
                    x=rsi.index,
                    y=rsi,
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=2)
                ))
                
                # Líneas de sobrecompra/sobreventa
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sobrecompra")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sobreventa")
                
                fig_rsi.update_layout(
                    title='RSI (14)',
                    xaxis_title='Fecha',
                    yaxis_title='RSI',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig_rsi, use_container_width=True)
            
            # Señales actuales
            latest_price = prices[selected_symbol].iloc[-1]
            latest_rsi = rsi.iloc[-1]
            latest_sma_20 = sma_20.iloc[-1]
            latest_sma_50 = sma_50.iloc[-1]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if latest_rsi < 30:
                    st.success(f"🟢 RSI: {latest_rsi:.2f} - Señal de COMPRA (Sobreventa)")
                elif latest_rsi > 70:
                    st.error(f"🔴 RSI: {latest_rsi:.2f} - Señal de VENTA (Sobrecompra)")
                else:
                    st.warning(f"🟡 RSI: {latest_rsi:.2f} - Señal NEUTRAL")
            
            with col2:
                if latest_sma_20 > latest_sma_50:
                    st.success("🟢 SMA: Señal de COMPRA (Tendencia alcista)")
                else:
                    st.error("🔴 SMA: Señal de VENTA (Tendencia bajista)")
            
            with col3:
                st.metric(f"Precio Actual - {selected_symbol}", f"${latest_price:.2f}")
    
    # 2. Análisis de Rendimientos
    with tab2:
        st.markdown('<div class="sub-header">📊 Análisis de Rendimientos</div>', unsafe_allow_html=True)
        
        # Estadísticas básicas
        col1, col2 = st.columns(2)
        
        with col1:
            # Tabla de estadísticas
            basic_stats = returns.describe().T
            st.dataframe(basic_stats[['mean', 'std', 'min', 'max']].round(4))
        
        with col2:
            # Distribución de rendimientos
            selected_asset_ret = st.selectbox("Seleccionar Activo para Distribución", options=returns.columns, key="dist_symbol")
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=returns[selected_asset_ret],
                nbinsx=50,
                name=f'Retornos {selected_asset_ret}',
                opacity=0.7,
                marker_color='#2E86AB'
            ))
            
            fig.update_layout(
                title=f'Distribución de Retornos - {selected_asset_ret}',
                xaxis_title='Retorno',
                yaxis_title='Frecuencia',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlación
        st.markdown("### 🔗 Matriz de Correlación")
        correlation = returns.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=correlation.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Correlación entre Activos',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 3. Análisis de Volatilidad
    with tab3:
        st.markdown('<div class="sub-header">📈 Análisis de Volatilidad</div>', unsafe_allow_html=True)
        
        # Volatilidad histórica
        volatility = returns.std() * np.sqrt(252)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=volatility.index,
            y=volatility.values,
            name='Volatilidad Anualizada',
            marker_color=['#1E88E5', '#43A047', '#FB8C00', '#E53935', '#6D4C41']
        ))
        
        fig.update_layout(
            title='Volatilidad Anualizada por Activo',
            xaxis_title='Activo',
            yaxis_title='Volatilidad',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Volatilidad en el tiempo
        selected_vol_asset = st.selectbox("Seleccionar Activo para Volatilidad Móvil", options=returns.columns, key="vol_symbol")
        
        rolling_vol = returns[selected_vol_asset].rolling(window=30).std() * np.sqrt(252)
        
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(
            x=rolling_vol.index,
            y=rolling_vol,
            mode='lines',
            name='Volatilidad Móvil (30 días)',
            line=dict(color='#2E86AB', width=2)
        ))
        
        fig_vol.update_layout(
            title=f'Volatilidad Histórica - {selected_vol_asset}',
            xaxis_title='Fecha',
            yaxis_title='Volatilidad',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig_vol, use_container_width=True)
    
    # 4. Análisis CAPM
    with tab4:
        st.markdown('<div class="sub-header">🎯 Análisis CAPM</div>', unsafe_allow_html=True)
        
        # Calcular Betas
        market_returns = returns['SPY']
        betas = {}
        
        for symbol in returns.columns:
            if symbol == 'SPY':
                continue
            
            # Regresión lineal
            import statsmodels.api as sm
            X = sm.add_constant(market_returns)
            y = returns[symbol]
            
            model = sm.OLS(y, X).fit()
            betas[symbol] = {
                'beta': model.params['SPY'],
                'alpha': model.params['const'],
                'r_squared': model.rsquared
            }
        
        # Tabla de Betas
        beta_df = pd.DataFrame(betas).T
        st.dataframe(beta_df.round(4))
        
        # Clasificación de riesgo
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Clasificación de Riesgo")
            for symbol, beta_info in betas.items():
                beta = beta_info['beta']
                if beta > 1.2:
                    st.error(f"🔴 {symbol}: β={beta:.4f} - Alto Riesgo (Cíclico)")
                elif beta > 1.0:
                    st.warning(f"🟡 {symbol}: β={beta:.4f} - Riesgo Moderado")
                elif beta > 0.8:
                    st.info(f"🔵 {symbol}: β={beta:.4f} - Riesgo Bajo")
                else:
                    st.success(f"🟢 {symbol}: β={beta:.4f} - Defensivo")
        
        with col2:
            # Gráfico de Betas
            fig_beta = go.Figure()
            fig_beta.add_trace(go.Bar(
                x=list(betas.keys()),
                y=[b['beta'] for b in betas.values()],
                name='Beta',
                marker_color=['#1E88E5', '#43A047', '#FB8C00', '#E53935']
            ))
            
            # Línea de beta = 1
            fig_beta.add_hline(y=1, line_dash="dash", line_color="black", annotation_text="Beta = 1 (Mercado)")
            
            fig_beta.update_layout(
                title='Betas de los Activos',
                xaxis_title='Activo',
                yaxis_title='Beta',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_beta, use_container_width=True)
    
    # 5. VaR y CVaR
    with tab5:
        st.markdown('<div class="sub-header">⚠️ Value at Risk (VaR) & Conditional VaR</div>', unsafe_allow_html=True)
        
        # Calcular VaR y CVaR
        var_values = {}
        cvar_values = {}
        
        for symbol in returns.columns:
            # VaR Histórico
            var_hist = np.percentile(returns[symbol], confidence_level * 100)
            
            # CVaR Histórico
            tail_losses = returns[symbol][returns[symbol] <= var_hist]
            cvar_hist = tail_losses.mean() if len(tail_losses) > 0 else var_hist
            
            var_values[symbol] = var_hist
            cvar_values[symbol] = cvar_hist
        
        # Tabla de métricas de riesgo
        risk_df = pd.DataFrame({
            'VaR': var_values,
            'CVaR': cvar_values
        })
        
        st.dataframe(risk_df.round(4))
        
        # Gráficos de riesgo
        col1, col2 = st.columns(2)
        
        with col1:
            fig_var = go.Figure()
            fig_var.add_trace(go.Bar(
                x=risk_df.index,
                y=risk_df['VaR'],
                name=f'VaR ({confidence_level*100:.0f}%)',
                marker_color='red'
            ))
            
            fig_var.update_layout(
                title=f'Value at Risk - {confidence_level*100:.0f}% de Confianza',
                xaxis_title='Activo',
                yaxis_title='VaR',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_var, use_container_width=True)
        
        with col2:
            fig_cvar = go.Figure()
            fig_cvar.add_trace(go.Bar(
                x=risk_df.index,
                y=risk_df['CVaR'],
                name='CVaR',
                marker_color='darkred'
            ))
            
            fig_cvar.update_layout(
                title='Conditional Value at Risk',
                xaxis_title='Activo',
                yaxis_title='CVaR',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_cvar, use_container_width=True)
    
    # 6. Optimización Markowitz
    with tab6:
        st.markdown('<div class="sub-header">⚖️ Optimización de Portafolio (Markowitz)</div>', unsafe_allow_html=True)
        
        # Optimización
        expected_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        
        # Portafolio de mínima varianza
        from scipy.optimize import minimize
        
        n_assets = len(returns.columns)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0.0, 0.4) for _ in range(n_assets))
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Mínima varianza
        min_var_result = minimize(
            lambda w: np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))),
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Máximo Sharpe
        risk_free_rate = 0.02
        max_sharpe_result = minimize(
            lambda w: -(np.sum(w * expected_returns) - risk_free_rate) / np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))),
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Crear DataFrames de resultados
        min_var_weights = pd.DataFrame({
            'Activo': returns.columns,
            'Peso': min_var_result.x
        })
        
        max_sharpe_weights = pd.DataFrame({
            'Activo': returns.columns,
            'Peso': max_sharpe_result.x
        })
        
        # Métricas de portafolios
        min_var_return = np.sum(min_var_result.x * expected_returns)
        min_var_vol = np.sqrt(np.dot(min_var_result.x.T, np.dot(cov_matrix, min_var_result.x)))
        min_var_sharpe = (min_var_return - risk_free_rate) / min_var_vol
        
        max_sharpe_return = np.sum(max_sharpe_result.x * expected_returns)
        max_sharpe_vol = np.sqrt(np.dot(max_sharpe_result.x.T, np.dot(cov_matrix, max_sharpe_result.x)))
        max_sharpe_sharpe = (max_sharpe_return - risk_free_rate) / max_sharpe_vol
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Portafolio de Mínima Varianza")
            st.metric("Retorno Anualizado", f"{min_var_return:.4f}")
            st.metric("Volatilidad Anualizada", f"{min_var_vol:.4f}")
            st.metric("Sharpe Ratio", f"{min_var_sharpe:.4f}")
            
            fig_min_var = go.Figure(data=go.Pie(
                labels=min_var_weights['Activo'],
                values=min_var_weights['Peso'],
                hole=0.3
            ))
            fig_min_var.update_layout(title="Composición - Mínima Varianza")
            st.plotly_chart(fig_min_var, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Portafolio de Máximo Sharpe")
            st.metric("Retorno Anualizado", f"{max_sharpe_return:.4f}")
            st.metric("Volatilidad Anualizada", f"{max_sharpe_vol:.4f}")
            st.metric("Sharpe Ratio", f"{max_sharpe_sharpe:.4f}")
            
            fig_max_sharpe = go.Figure(data=go.Pie(
                labels=max_sharpe_weights['Activo'],
                values=max_sharpe_weights['Peso'],
                hole=0.3
            ))
            fig_max_sharpe.update_layout(title="Composición - Máximo Sharpe")
            st.plotly_chart(fig_max_sharpe, use_container_width=True)
    
    # 7. Señales de Trading
    with tab7:
        st.markdown('<div class="sub-header">🎯 Sistema de Señales de Trading</div>', unsafe_allow_html=True)
        
        # Generar señales combinadas
        signals = {}
        
        for symbol in returns.columns:
            # Señales SMA
            sma_20 = prices[symbol].rolling(20).mean()
            sma_50 = prices[symbol].rolling(50).mean()
            sma_signal = 1 if sma_20.iloc[-1] > sma_50.iloc[-1] else -1
            
            # Señales RSI
            delta = prices[symbol].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_signal = 1 if rsi.iloc[-1] < 30 else (-1 if rsi.iloc[-1] > 70 else 0)
            
            # Señal combinada
            combined_signal = (sma_signal + rsi_signal) / 2
            
            signals[symbol] = {
                'sma': sma_signal,
                'rsi': rsi_signal,
                'combined': combined_signal,
                'recommendation': 'COMPRAR' if combined_signal > 0.3 else ('VENDER' if combined_signal < -0.3 else 'MANTENER')
            }
        
        # Tabla de señales
        signals_df = pd.DataFrame(signals).T
        st.dataframe(signals_df)
        
        # Gráficos de señales
        selected_signal_asset = st.selectbox("Seleccionar Activo para Gráfico de Señales", options=returns.columns, key="signal_symbol")
        
        if selected_signal_asset:
            # Gráfico de precios con señales
            fig_signals = go.Figure()
            
            # Precio
            fig_signals.add_trace(go.Scatter(
                x=prices.index,
                y=prices[selected_signal_asset],
                mode='lines',
                name=f'{selected_signal_asset} Precio',
                line=dict(color='black', width=2)
            ))
            
            # Señales de compra
            buy_signals = prices[prices[selected_signal_asset].rolling(20).mean() > prices[selected_signal_asset].rolling(50).mean()]
            if not buy_signals.empty:
                fig_signals.add_trace(go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals[selected_signal_asset],
                    mode='markers',
                    name='Señal de Compra',
                    marker=dict(color='green', symbol='triangle-up', size=8)
                ))
            
            # Señales de venta
            sell_signals = prices[prices[selected_signal_asset].rolling(20).mean() < prices[selected_signal_asset].rolling(50).mean()]
            if not sell_signals.empty:
                fig_signals.add_trace(go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals[selected_signal_asset],
                    mode='markers',
                    name='Señal de Venta',
                    marker=dict(color='red', symbol='triangle-down', size=8)
                ))
            
            fig_signals.update_layout(
                title=f'Señales de Trading - {selected_signal_asset}',
                xaxis_title='Fecha',
                yaxis_title='Precio ($)',
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig_signals, use_container_width=True)
    
    # 8. Comparación con Benchmark
    with tab8:
        st.markdown('<div class="sub-header">🏆 Comparación con Benchmark (SPY)</div>', unsafe_allow_html=True)
        
        # Retornos acumulados
        cumulative_returns = (1 + returns).cumprod() - 1
        
        fig_benchmark = go.Figure()
        
        for symbol in returns.columns:
            fig_benchmark.add_trace(go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[symbol],
                mode='lines',
                name=symbol,
                line=dict(width=2)
            ))
        
        fig_benchmark.update_layout(
            title='Retornos Acumulados vs Benchmark',
            xaxis_title='Fecha',
            yaxis_title='Retorno Acumulado',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig_benchmark, use_container_width=True)
        
        # Métricas de performance vs benchmark
        spy_returns = returns['SPY']
        
        performance_metrics = {}
        
        for symbol in returns.columns:
            if symbol == 'SPY':
                continue
            
            asset_returns = returns[symbol]
            
            # Alpha (exceso de retorno)
            alpha = (asset_returns.mean() - spy_returns.mean()) * 252
            
            # Beta (ya calculado)
            beta = betas[symbol]['beta'] if symbol in betas else 1.0
            
            # Information Ratio
            tracking_error = (asset_returns - spy_returns).std() * np.sqrt(252)
            info_ratio = alpha / tracking_error if tracking_error != 0 else 0
            
            performance_metrics[symbol] = {
                'Alpha': alpha,
                'Beta': beta,
                'Info_Ratio': info_ratio
            }
        
        performance_df = pd.DataFrame(performance_metrics).T
        st.dataframe(performance_df.round(4))
        
        # Gráfico de Alpha
        fig_alpha = go.Figure()
        fig_alpha.add_trace(go.Bar(
            x=performance_df.index,
            y=performance_df['Alpha'],
            name='Alpha',
            marker_color=['green' if x > 0 else 'red' for x in performance_df['Alpha']]
        ))
        
        fig_alpha.add_hline(y=0, line_dash="dash", line_color="black")
        fig_alpha.update_layout(
            title='Alpha vs Benchmark (SPY)',
            xaxis_title='Activo',
            yaxis_title='Alpha',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig_alpha, use_container_width=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2>🚀 Dashboard de Riesgo Financiero</h2>
        <p>Por favor, haga clic en "Cargar Datos" para comenzar el análisis.</p>
        <p><strong>Activos incluidos:</strong> Apple (AAPL), Microsoft (MSFT), Exxon (XOM), Coca-Cola (KO), S&P 500 (SPY)</p>
    </div>
    """, unsafe_allow_html=True)