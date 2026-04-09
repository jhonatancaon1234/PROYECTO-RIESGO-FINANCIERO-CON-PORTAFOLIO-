"""
Frontend Streamlit - Dashboard de Riesgo Financiero
Consume el Backend FastAPI
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import json

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Riesgo Financiero",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de API
API_BASE_URL = "http://localhost:8000"

# CSS personalizado - Diseño profesional
st.markdown("""
<style>
    /* Encabezado principal */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 6px rgba(0,0,0,0.1);
        letter-spacing: -1px;
    }
    
    /* Subtítulo de secciones */
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar profesional */
    .css-1d391kg {
        background-color: #1E3A8A !important;
        border-right: 1px solid #3B82F6;
    }
    
    /* Títulos de sidebar */
    .css-1oe59io {
        color: white !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Métricas con estilo profesional */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.15);
    }
    
    /* Texto positivo y negativo */
    .positive {
        color: #166534 !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .negative {
        color: #991b1b !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* Botones profesionales */
    .stButton > button {
        background-color: #3B82F6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background-color: #2563EB !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px -3px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Tabs con estilo profesional */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #334155;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3B82F6;
        color: white;
        border-bottom: 3px solid #1E3A8A;
    }
    
    /* Contenedores de contenido */
    .stContainer {
        background-color: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* DataFrames con estilo profesional */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Gráficos con borde profesional */
    .js-plotly-plot .plotly .plot-container {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Texto de alerta profesional */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
        background-color: #eff6ff;
        color: #1e40af;
    }
    
    /* Footer discreto */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #e2e8f0;
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

# Funciones de API
def call_api(endpoint, data=None):
    """Llama a un endpoint de la API"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

# Carga de datos
if not st.session_state.data_loaded:
    with st.spinner('Cargando datos financieros desde la API...'):
        try:
            data_request = {
                "assets": selected_assets,
                "confidence_level": confidence_level
            }
            
            api_response = call_api("/data", data_request)
            
            if api_response and api_response.get("success"):
                data = api_response["data"]
                
                # Convertir datos a DataFrames
                prices = pd.DataFrame(data["prices"])
                returns = pd.DataFrame(data["returns"])
                
                # Convertir índices a datetime
                prices.index = pd.to_datetime(prices.index)
                returns.index = pd.to_datetime(returns.index)
                
                st.session_state.prices = prices
                st.session_state.returns = returns
                st.session_state.data_loaded = True
                st.success("✅ Datos cargados exitosamente desde la API!")
            else:
                st.error("❌ No se pudieron cargar los datos desde la API")
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
            with st.spinner('Calculando indicadores técnicos...'):
                # Llamar a API para análisis técnico
                tech_request = {
                    "symbol": selected_symbol,
                    "window_sma_short": 20,
                    "window_sma_long": 50,
                    "window_rsi": 14
                }
                
                tech_response = call_api("/technical-analysis", tech_request)
                
                if tech_response and tech_response.get("success"):
                    indicators = tech_response["data"]
                    
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
                        fig.add_trace(go.Scatter(
                            x=prices.index,
                            y=[indicators['sma_short']] * len(prices),
                            mode='lines',
                            name='SMA 20',
                            line=dict(color='orange', width=1)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=prices.index,
                            y=[indicators['sma_long']] * len(prices),
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
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(
                            x=prices.index,
                            y=[indicators['rsi']] * len(prices),
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
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if indicators['rsi'] < 30:
                            st.success(f"🟢 RSI: {indicators['rsi']:.2f} - Señal de COMPRA (Sobreventa)")
                        elif indicators['rsi'] > 70:
                            st.error(f"🔴 RSI: {indicators['rsi']:.2f} - Señal de VENTA (Sobrecompra)")
                        else:
                            st.warning(f"🟡 RSI: {indicators['rsi']:.2f} - Señal NEUTRAL")
                    
                    with col2:
                        if indicators['sma_short'] > indicators['sma_long']:
                            st.success("🟢 SMA: Señal de COMPRA (Tendencia alcista)")
                        else:
                            st.error("🔴 SMA: Señal de VENTA (Tendencia bajista)")
                    
                    with col3:
                        # Obtener precio actual
                        current_price = prices[selected_symbol].iloc[-1]
                        st.metric(f"Precio Actual - {selected_symbol}", f"${current_price:.2f}")
                    
                    # Recomendación
                    st.markdown(f"### 🎯 Recomendación: {indicators['recommendation']}")
    
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
        volatility_data = {}
        for symbol in returns.columns:
            vol_request = {"symbol": symbol, "window": 30}
            vol_response = call_api("/volatility", vol_request)
            
            if vol_response and vol_response.get("success"):
                volatility_data[symbol] = vol_response["data"]["historical_volatility"]
        
        if volatility_data:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(volatility_data.keys()),
                y=list(volatility_data.values()),
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
        
        if selected_vol_asset:
            with st.spinner('Calculando volatilidad...'):
                vol_request = {"symbol": selected_vol_asset, "window": 30}
                vol_response = call_api("/volatility", vol_request)
                
                if vol_response and vol_response.get("success"):
                    vol_data = vol_response["data"]
                    
                    fig_vol = go.Figure()
                    fig_vol.add_trace(go.Scatter(
                        x=prices.index,
                        y=[vol_data["historical_volatility"]] * len(prices),
                        mode='lines',
                        name='Volatilidad Histórica',
                        line=dict(color='#2E86AB', width=2)
                    ))
                    
                    fig_vol.add_trace(go.Scatter(
                        x=prices.index,
                        y=[vol_data["garch_volatility"]] * len(prices),
                        mode='lines',
                        name='Volatilidad GARCH',
                        line=dict(color='#FF6B6B', width=2)
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
        
        with st.spinner('Calculando CAPM...'):
            capm_request = {
                "assets": [symbol for symbol in returns.columns if symbol != 'SPY'],
                "market_symbol": "SPY"
            }
            
            capm_response = call_api("/capm", capm_request)
            
            if capm_response and capm_response.get("success"):
                capm_data = capm_response["data"]
                
                # Tabla de Betas
                beta_df = pd.DataFrame(capm_data).T
                st.dataframe(beta_df.round(4))
                
                # Gráfico de Betas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Clasificación de Riesgo")
                    for symbol, beta_info in capm_data.items():
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
                    fig_beta = go.Figure()
                    fig_beta.add_trace(go.Bar(
                        x=list(capm_data.keys()),
                        y=[b['beta'] for b in capm_data.values()],
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
        
        var_data = {}
        cvar_data = {}
        
        for symbol in returns.columns:
            with st.spinner(f'Calculando VaR para {symbol}...'):
                var_request = {
                    "symbol": symbol,
                    "confidence_level": confidence_level
                }
                
                var_response = call_api("/risk-metrics", var_request)
                
                if var_response and var_response.get("success"):
                    metrics = var_response["data"]
                    var_data[symbol] = metrics['var']
                    cvar_data[symbol] = metrics['cvar']
        
        # Tabla de métricas de riesgo
        risk_df = pd.DataFrame({
            'VaR': var_data,
            'CVaR': cvar_data
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
        
        with st.spinner('Optimizando portafolio...'):
            portfolio_request = {
                "assets": selected_assets,
                "target_return": None,
                "risk_tolerance": 0.5
            }
            
            portfolio_response = call_api("/portfolio-optimize", portfolio_request)
            
            if portfolio_response and portfolio_response.get("success"):
                portfolio_data = portfolio_response["data"]
                
                # Métricas de portafolios
                min_var_data = portfolio_data['min_variance']
                max_sharpe_data = portfolio_data['max_sharpe']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🎯 Portafolio de Mínima Varianza")
                    st.metric("Retorno Anualizado", f"{min_var_data['expected_return']:.4f}")
                    st.metric("Volatilidad Anualizada", f"{min_var_data['volatility']:.4f}")
                    st.metric("Sharpe Ratio", f"{min_var_data['sharpe_ratio']:.4f}")
                    
                    # Gráfico de pesos
                    weights_df = pd.DataFrame(list(min_var_data['weights'].items()), columns=['Activo', 'Peso'])
                    fig_min_var = px.pie(weights_df, values='Peso', names='Activo', title="Composición - Mínima Varianza")
                    st.plotly_chart(fig_min_var, use_container_width=True)
                
                with col2:
                    st.markdown("### 🎯 Portafolio de Máximo Sharpe")
                    st.metric("Retorno Anualizado", f"{max_sharpe_data['expected_return']:.4f}")
                    st.metric("Volatilidad Anualizada", f"{max_sharpe_data['volatility']:.4f}")
                    st.metric("Sharpe Ratio", f"{max_sharpe_data['sharpe_ratio']:.4f}")
                    
                    # Gráfico de pesos
                    weights_df = pd.DataFrame(list(max_sharpe_data['weights'].items()), columns=['Activo', 'Peso'])
                    fig_max_sharpe = px.pie(weights_df, values='Peso', names='Activo', title="Composición - Máximo Sharpe")
                    st.plotly_chart(fig_max_sharpe, use_container_width=True)
    
    # 7. Señales de Trading
    with tab7:
        st.markdown('<div class="sub-header">🎯 Sistema de Señales de Trading</div>', unsafe_allow_html=True)
        
        signals_data = {}
        
        for symbol in returns.columns:
            with st.spinner(f'Generando señales para {symbol}...'):
                signal_request = {
                    "symbol": symbol,
                    "strategy": "combined"
                }
                
                signal_response = call_api("/trading-signals", signal_request)
                
                if signal_response and signal_response.get("success"):
                    signals_data[symbol] = signal_response["data"]
        
        if signals_data:
            # Tabla de señales
            signals_df = pd.DataFrame(signals_data).T
            st.dataframe(signals_df)
            
            # Gráficos de señales
            selected_signal_asset = st.selectbox("Seleccionar Activo para Gráfico de Señales", options=returns.columns, key="signal_symbol")
            
            if selected_signal_asset and selected_signal_asset in signals_data:
                signal_info = signals_data[selected_signal_asset]
                
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
                
                # Señal actual
                signal_type = signal_info['signal_type']
                price = signal_info['price']
                
                if signal_type == 'BUY':
                    fig_signals.add_trace(go.Scatter(
                        x=[prices.index[-1]],
                        y=[price],
                        mode='markers',
                        name='Señal de Compra',
                        marker=dict(color='green', symbol='triangle-up', size=15)
                    ))
                elif signal_type == 'SELL':
                    fig_signals.add_trace(go.Scatter(
                        x=[prices.index[-1]],
                        y=[price],
                        mode='markers',
                        name='Señal de Venta',
                        marker=dict(color='red', symbol='triangle-down', size=15)
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
        
        with st.spinner('Comparando con benchmark...'):
            benchmark_request = {
                "assets": [symbol for symbol in returns.columns if symbol != 'SPY'],
                "benchmark_symbol": "SPY"
            }
            
            benchmark_response = call_api("/benchmark", benchmark_request)
            
            if benchmark_response and benchmark_response.get("success"):
                benchmark_data = benchmark_response["data"]
                
                # Gráfico de retornos acumulados
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
                performance_df = pd.DataFrame(benchmark_data).T
                st.dataframe(performance_df.round(4))
                
                # Gráfico de Alpha
                if not performance_df.empty:
                    fig_alpha = go.Figure()
                    fig_alpha.add_trace(go.Bar(
                        x=performance_df.index,
                        y=performance_df['alpha'],
                        name='Alpha',
                        marker_color=['green' if x > 0 else 'red' for x in performance_df['alpha']]
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
        <p><strong>Nota:</strong> Asegúrate de que el Backend FastAPI esté corriendo en <code>http://localhost:8000</code></p>
        <p><strong>Activos incluidos:</strong> Apple (AAPL), Microsoft (MSFT), Exxon (XOM), Coca-Cola (KO), S&P 500 (SPY)</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Dashboard de Riesgo Financiero - Backend FastAPI + Frontend Streamlit<br>
    Proyecto Universitario - Análisis de Riesgo Financiero con Portafolio
</div>
""", unsafe_allow_html=True)