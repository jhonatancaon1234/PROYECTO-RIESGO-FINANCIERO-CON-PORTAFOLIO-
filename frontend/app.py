"""
Frontend Streamlit - Dashboard de Riesgo Financiero Profesional
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
    page_title="Dashboard de Riesgo Financiero - Sistema Profesional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de API
API_BASE_URL = "http://localhost:8000"

# CSS personalizado - Diseño profesional avanzado
st.markdown("""
<style>
    /* Colores corporativos profesionales */
    :root {
        --primary-dark: #1E3A5F;
        --primary-blue: #2E6B9E;
        --primary-light: #4A90B8;
        --accent-green: #2ECC71;
        --accent-red: #E74C3C;
        --accent-orange: #F39C12;
        --bg-dark: #0F1B28;
        --bg-medium: #1A2738;
        --bg-light: #2C3E50;
        --text-primary: #FFFFFF;
        --text-secondary: #BDC3C7;
        --text-muted: #7F8C8D;
        --border-color: #34495E;
        --card-bg: linear-gradient(135deg, #1A2738 0%, #2C3E50 100%);
    }
    
    /* Encabezado principal - Estilo Trading/Financiero */
    .main-header {
        font-size: 2.8rem;
        font-weight: 900;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
        letter-spacing: -0.5px;
        border-bottom: 3px solid #4A90B8;
        padding-bottom: 1rem;
        font-family: 'Segoe UI', system-ui, sans-serif;
        background: linear-gradient(135deg, #1A2738 0%, #2C3E50 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        border: 2px solid #4A90B8;
        box-shadow: 0 8px 25px rgba(74, 144, 184, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "📈";
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 3rem;
        opacity: 0.8;
    }
    
    .main-header::after {
        content: "📊";
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 3rem;
        opacity: 0.8;
    }
    
    .header-title {
        background: linear-gradient(135deg, #4A90B8 0%, #2ECC71 50%, #4A90B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
        padding: 0 3rem;
    }
    
    .header-subtitle {
        color: #BDC3C7;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    /* Subtítulo de secciones - Estilo Profesional */
    .sub-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4A90B8;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #4A90B8;
        padding-left: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar profesional - Estilo Terminal */
    .css-1d391kg {
        background: linear-gradient(180deg, #0F1B28 0%, #1A2738 100%) !important;
        border-right: 2px solid #34495E;
        box-shadow: 4px 0 20px rgba(0,0,0,0.3);
    }
    
    /* Títulos de sidebar */
    .css-1oe59io {
        color: #4A90B8 !important;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Métricas con estilo profesional */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #4A90B8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        color: #FFFFFF;
        border: 1px solid #34495E;
    }
    
    .metric-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(74, 144, 184, 0.3);
        border-color: #4A90B8;
    }
    
    /* Texto positivo y negativo */
    .positive {
        color: #2ECC71 !important;
        font-weight: 800;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .negative {
        color: #E74C3C !important;
        font-weight: 800;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Botones profesionales */
    .stButton > button {
        background: linear-gradient(135deg, #4A90B8 0%, #2E6B9E 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(74, 144, 184, 0.4) !important;
        font-size: 0.9rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5BA0C8 0%, #3E7BAE 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(74, 144, 184, 0.6) !important;
    }
    
    /* Tabs con estilo profesional */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background: linear-gradient(180deg, #1A2738 0%, #0F1B28 100%);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #34495E;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #2C3E50 0%, #1A2738 100%);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: #BDC3C7;
        border: 1px solid #34495E;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85rem;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4A90B8 0%, #2E6B9E 100%);
        color: #FFFFFF;
        border-color: #4A90B8;
        box-shadow: 0 4px 15px rgba(74, 144, 184, 0.4);
    }
    
    /* Contenedores de contenido */
    .stContainer {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        border: 1px solid #34495E;
    }
    
    /* DataFrames con estilo profesional */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #34495E;
    }
    
    /* Gráficos con borde profesional */
    .js-plotly-plot .plotly .plot-container {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #34495E;
        background: #1A2738;
    }
    
    /* Texto de alerta profesional */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #4A90B8;
        background: linear-gradient(135deg, #1A2738 0%, #2C3E50 100%);
        color: #BDC3C7;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #34495E;
    }
    
    /* Footer discreto */
    .footer {
        text-align: center;
        color: #7F8C8D;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #34495E;
        background: linear-gradient(180deg, #0F1B28 0%, #1A2738 100%);
    }
    
    /* Tarjetas de interpretación */
    .insight-card {
        background: linear-gradient(135deg, #1A2738 0%, #2C3E50 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #34495E;
        border-left: 4px solid #4A90B8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .insight-card h4 {
        color: #4A90B8;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .insight-card p {
        color: #BDC3C7;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .insight-card strong {
        color: #FFFFFF;
    }
    
    /* Métricas destacadas */
    .highlight-metric {
        background: linear-gradient(135deg, #4A90B8 0%, #2E6B9E 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(74, 144, 184, 0.3);
    }
    
    .highlight-metric .value {
        font-size: 2rem;
        font-weight: 900;
        color: #FFFFFF;
    }
    
    .highlight-metric .label {
        font-size: 0.9rem;
        color: #E0E0E0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Indicadores de estado */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.25rem;
        font-size: 0.9rem;
    }
    
    .status-buy {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
        color: white;
        box-shadow: 0 2px 10px rgba(46, 204, 113, 0.3);
    }
    
    .status-sell {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
        color: white;
        box-shadow: 0 2px 10px rgba(231, 76, 60, 0.3);
    }
    
    .status-hold {
        background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
        color: white;
        box-shadow: 0 2px 10px rgba(243, 156, 18, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Título principal - Estilo Trading/Financiero
st.markdown("""
<div class="main-header">
    <h1 class="header-title">SISTEMA PROFESIONAL DE GESTIÓN DE PORTAFOLIO</h1>
    <p class="header-subtitle">Análisis Avanzado de Riesgo Financiero y Optimización de Portafolios</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## ⚙️ CONFIGURACIÓN DEL SISTEMA")
st.sidebar.markdown("---")

# Selección de activos
assets = ['AAPL', 'MSFT', 'XOM', 'KO', 'SPY']
selected_assets = st.sidebar.multiselect(
    "📈 ACTIVOS DEL PORTAFOLIO",
    options=assets,
    default=assets,
    help="Seleccione las acciones que desea incluir en el análisis"
)

# Período de análisis
period_options = {
    "6 meses": 180,
    "1 año": 365,
    "2 años": 730,
    "5 años": 1825
}
selected_period = st.sidebar.selectbox(
    "📅 PERÍODO DE ANÁLISIS",
    options=list(period_options.keys()),
    index=2,
    help="Seleccione el horizonte temporal para el análisis"
)

# Nivel de confianza para VaR
confidence_level = st.sidebar.slider(
    "⚠️ NIVEL DE CONFIANZA (VaR)",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01,
    help="Nivel de significancia para el cálculo del Value at Risk"
)

# Botón para cargar datos
if st.sidebar.button("🔄 ACTUALIZAR DATOS"):
    st.session_state.data_loaded = False

# Estado de carga de datos
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Funciones de API
def call_api(endpoint, data=None, timeout=30):
    """Llama a un endpoint de la API con manejo robusto de errores"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        # Configurar timeout para evitar bloqueos
        if data:
            response = requests.post(url, json=data, timeout=timeout)
        else:
            response = requests.get(url, timeout=timeout)
        
        # Verificar código de estado
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                st.error(f"❌ Error decodificando respuesta JSON: {str(e)}")
                return None
        else:
            st.error(f"❌ Error en API ({response.status_code}): {response.text[:200]}")
            return None
            
    except requests.exceptions.Timeout:
        st.error(f"⏰ Timeout: La API no respondió en {timeout} segundos")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Error de conexión: No se pudo conectar con la API. ¿Está el backend corriendo?")
        return None
    except Exception as e:
        st.error(f"💥 Error inesperado: {str(e)}")
        return None

# Carga de datos
if not st.session_state.data_loaded:
    with st.spinner('📡 Conectando con el servidor de datos...'):
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
                st.success("✅ Datos cargados exitosamente desde el servidor")
            else:
                st.error("❌ No se pudieron cargar los datos desde el servidor")
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
    
    # Resumen ejecutivo
    st.markdown('<div class="sub-header">📋 RESUMEN EJECUTIVO</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem; font-weight: 900; color: #4A90B8;">{}</div>
            <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Activos Analizados</div>
        </div>
        """.format(len(returns.columns)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2rem; font-weight: 900; color: #2ECC71;">{}</div>
            <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Días de Datos</div>
        </div>
        """.format(len(returns)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem; font-weight: 700; color: #F39C12;">{}</div>
            <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Fecha Inicio</div>
        </div>
        """.format(prices.index[0].strftime('%Y-%m-%d')), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem; font-weight: 700; color: #E74C3C;">{}</div>
            <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Fecha Fin</div>
        </div>
        """.format(prices.index[-1].strftime('%Y-%m-%d')), unsafe_allow_html=True)
    
    # Pestañas del dashboard
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🔍 ANÁLISIS TÉCNICO",
        "📊 RENDIMIENTOS", 
        "📈 VOLATILIDAD",
        "🎯 CAPM",
        "⚠️ RIESGO (VaR/CVaR)",
        "⚖️ MARKOWITZ",
        "🎯 SEÑALES",
        "🏆 BENCHMARK"
    ])
    
    # 1. Análisis Técnico
    with tab1:
        st.markdown('<div class="sub-header">🔍 ANÁLISIS TÉCNICO PROFESIONAL</div>', unsafe_allow_html=True)
        
        # Selección de activo
        selected_symbol = st.selectbox("🎯 SELECCIONAR ACTIVO", options=prices.columns, key="tech_symbol")
        
        if selected_symbol:
            with st.spinner('📊 Calculando indicadores técnicos...'):
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
                    
                    # Columna izquierda - Gráfico de precios
                    col1, col2 = st.columns([2, 1])
                    
                    # Mapeo de nombres completos de activos
                    asset_names = {
                        'AAPL': 'Apple Inc.',
                        'MSFT': 'Microsoft Corporation',
                        'XOM': 'Exxon Mobil Corporation',
                        'KO': 'The Coca-Cola Company',
                        'SPY': 'S&P 500 ETF Trust'
                    }
                    
                    with col1:
                        st.markdown("### 📈 EVOLUCIÓN DE PRECIOS Y MEDIAS MÓVILES")
                        
                        # Mostrar nombre completo del activo
                        st.markdown(f"""
                        <div class="highlight-metric" style="margin-bottom: 1rem;">
                            <div class="value">{selected_symbol}</div>
                            <div class="label">{asset_names.get(selected_symbol, selected_symbol)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Interpretación humanizada
                        st.markdown("""
                        <div class="insight-card">
                            <h4>💡 ¿QUÉ NOS DICEN LAS MEDIAS MÓVILES?</h4>
                            <p><strong>Imagine las medias móviles como el "promedio móvil" del precio:</strong></p>
                            <p>• <strong>SMA 20 (línea naranja):</strong> Es como el "promedio del último mes" - reacciona rápido a los cambios del mercado</p>
                            <p>• <strong>SMA 50 (línea roja):</strong> Es como el "promedio de los últimos 2 meses" - muestra la tendencia general</p>
                            <p>• <strong>Señal de COMPRA:</strong> Cuando la línea naranja cruza POR ENCIMA de la roja → ¡El precio está subiendo!</p>
                            <p>• <strong>Señal de VENTA:</strong> Cuando la línea naranja cruza POR DEBAJO de la roja → ¡El precio está bajando!</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Gráfico de precios con indicadores
                        fig = go.Figure()
                        
                        # Precio
                        fig.add_trace(go.Scatter(
                            x=prices.index,
                            y=prices[selected_symbol],
                            mode='lines',
                            name=f'{selected_symbol} Precio',
                            line=dict(color='#4A90B8', width=3)
                        ))
                        
                        # Medias móviles
                        fig.add_trace(go.Scatter(
                            x=prices.index,
                            y=[indicators['sma_short']] * len(prices),
                            mode='lines',
                            name='SMA 20 (Corta)',
                            line=dict(color='#F39C12', width=2)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=prices.index,
                            y=[indicators['sma_long']] * len(prices),
                            mode='lines',
                            name='SMA 50 (Larga)',
                            line=dict(color='#E74C3C', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f'Análisis Técnico - {selected_symbol}',
                            xaxis_title='Fecha',
                            yaxis_title='Precio ($)',
                            template='plotly_dark',
                            height=350,
                            plot_bgcolor='#1A2738',
                            paper_bgcolor='#1A2738',
                            font=dict(color='#BDC3C7'),
                            title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown("### 📊 RSI - ÍNDICE DE FUERZA RELATIVA")
                        
                        # Interpretación humanizada
                        st.markdown("""
                        <div class="insight-card">
                            <h4>💡 ¿QUÉ NOS DICE EL RSI?</h4>
                            <p><strong>El RSI es como un "termómetro" del mercado:</strong></p>
                            <p>• <strong>RSI > 70 (Zona roja):</strong> ¡El activo está "caliente"! Demasiada gente lo compra → Posible corrección</p>
                            <p>• <strong>RSI < 30 (Zona verde):</strong> ¡El activo está "frío"! Demasiada gente lo vende → Posible rebote</p>
                            <p>• <strong>RSI 30-70 (Zona amarilla):</strong> Temperatura normal → Mercado estable</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Calcular RSI histórico correctamente
                        close_prices = prices[selected_symbol]
                        delta = close_prices.diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi_values = 100 - (100 / (1 + rs))
                        
                        # Gráfico de RSI
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(
                            x=prices.index,
                            y=rsi_values,
                            mode='lines',
                            name='RSI',
                            line=dict(color='#9B59B6', width=2)
                        ))
                        
                        # Líneas de sobrecompra/sobreventa
                        fig_rsi.add_hline(y=70, line_dash="dash", line_color="#E74C3C", annotation_text="Sobrecompra (>70)")
                        fig_rsi.add_hline(y=30, line_dash="dash", line_color="#2ECC71", annotation_text="Sobreventa (<30)")
                        
                        fig_rsi.update_layout(
                            title='RSI (14 días)',
                            xaxis_title='Fecha',
                            yaxis_title='RSI',
                            template='plotly_dark',
                            height=350,
                            plot_bgcolor='#1A2738',
                            paper_bgcolor='#1A2738',
                            font=dict(color='#BDC3C7'),
                            title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
                        )
                        
                        st.plotly_chart(fig_rsi, use_container_width=True)
                    
                    # Señales actuales
                    st.markdown("### 🎯 SEÑALES ACTUALES DEL MERCADO")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if indicators['rsi'] < 30:
                            st.markdown("""
                            <div class="status-indicator status-buy">
                                🟢 RSI: {:.2f} - ¡OPORTUNIDAD DE COMPRA!
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">El activo está sobrevendido - Posible rebote al alza</p>
                            """.format(indicators['rsi']), unsafe_allow_html=True)
                        elif indicators['rsi'] > 70:
                            st.markdown("""
                            <div class="status-indicator status-sell">
                                🔴 RSI: {:.2f} - ¡PELIGRO DE SOBRECOMPRA!
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">El activo está sobrecomprado - Posible corrección</p>
                            """.format(indicators['rsi']), unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="status-indicator status-hold">
                                🟡 RSI: {:.2f} - ZONA NEUTRAL
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">El activo está en rango normal - Esperar señal clara</p>
                            """.format(indicators['rsi']), unsafe_allow_html=True)
                    
                    with col2:
                        if indicators['sma_short'] > indicators['sma_long']:
                            st.markdown("""
                            <div class="status-indicator status-buy">
                                🟢 TENDENCIA ALCISTA
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">SMA 20 > SMA 50 - El precio está en tendencia positiva</p>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="status-indicator status-sell">
                                🔴 TENDENCIA BAJISTA
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">SMA 20 < SMA 50 - El precio está en tendencia negativa</p>
                            """, unsafe_allow_html=True)
                    
                    with col3:
                        # Obtener precio actual
                        current_price = prices[selected_symbol].iloc[-1]
                        st.markdown(f"""
                        <div class="highlight-metric">
                            <div class="value">${current_price:.2f}</div>
                            <div class="label">PRECIO ACTUAL</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Recomendación final
                    st.markdown(f"""
                    <div class="insight-card" style="border-left-color: {'#2ECC71' if indicators['recommendation'] == 'BUY' else '#E74C3C' if indicators['recommendation'] == 'SELL' else '#F39C12'};">
                        <h4>🎯 RECOMENDACIÓN DEL SISTEMA: {indicators['recommendation']}</h4>
                        <p><strong>Basado en el análisis técnico combinado (SMA + RSI), el sistema recomienda:</strong></p>
                        <p>Esta recomendación considera tanto la tendencia del precio (medias móviles) como el momento del mercado (RSI) para proporcionar una señal más confiable.</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # 2. Análisis de Rendimientos
    with tab2:
        st.markdown('<div class="sub-header">📊 ANÁLISIS DE RENDIMIENTOS</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿CÓMO INTERPRETAR LOS RENDIMIENTOS?</h4>
            <p><strong>Los rendimientos nos dicen cuánto gana o pierde un activo día a día:</strong></p>
            <p>• <strong>Media (Mean):</strong> Es el "promedio diario" de ganancias/pérdidas. Si es 0.001, significa 0.1% diario promedio</p>
            <p>• <strong>Desviación Estándar (Std):</strong> Mide qué tan "volátil" es el activo. Mayor número = más incertidumbre</p>
            <p>• <strong>Mínimo y Máximo:</strong> Los peores y mejores días que ha tenido el activo en el período analizado</p>
            <p><strong>Ejemplo práctico:</strong> Si un activo tiene media 0.001 (0.1% diario) y std 0.02 (2%), gana 0.1% promedio pero con fluctuaciones de ±2% diario</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Estadísticas básicas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 ESTADÍSTICAS DESCRIPTIVAS")
            
            # Tabla de estadísticas
            basic_stats = returns.describe().T
            st.dataframe(basic_stats[['mean', 'std', 'min', 'max']].round(4), use_container_width=True)
        
        with col2:
            st.markdown("### 📈 DISTRIBUCIÓN DE RENDIMIENTOS")
            
            # Distribución de rendimientos
            selected_asset_ret = st.selectbox("Seleccionar Activo", options=returns.columns, key="dist_symbol")
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=returns[selected_asset_ret],
                nbinsx=50,
                name=f'Retornos {selected_asset_ret}',
                opacity=0.8,
                marker_color='#4A90B8'
            ))
            
            fig.update_layout(
                title=f'Distribución de Retornos - {selected_asset_ret}',
                xaxis_title='Retorno Diario',
                yaxis_title='Frecuencia',
                template='plotly_dark',
                height=350,
                plot_bgcolor='#1A2738',
                paper_bgcolor='#1A2738',
                font=dict(color='#BDC3C7'),
                title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlación
        st.markdown("### 🔗 MATRIZ DE CORRELACIÓN - ¿CÓMO SE MUEVEN LOS ACTIVOS JUNTOS?")
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿QUÉ NOS DICE LA CORRELACIÓN?</h4>
            <p><strong>La correlación mide cómo se mueven los activos entre sí:</strong></p>
            <p>• <strong>Correlación +1 (Rojo intenso):</strong> Los activos se mueven IDÉNTICAMENTE - Si uno sube 1%, el otro también</p>
            <p>• <strong>Correlación 0 (Blanco):</strong> No hay relación - Los movimientos son independientes</p>
            <p>• <strong>Correlación -1 (Azul intenso):</strong> Los activos se mueven EN DIRECCIONES OPUESTAS - Ideal para diversificar</p>
            <p><strong>Ejemplo práctico:</strong> Si AAPL y MSFT tienen correlación 0.8, cuando AAPL sube 1%, MSFT tiende a subir 0.8%</p>
            <p><strong>Para diversificar:</strong> Busque activos con correlación baja o negativa para reducir el riesgo del portafolio</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            textfont={"size": 12, "color": "white"},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Correlación entre Activos',
            template='plotly_dark',
            height=400,
            plot_bgcolor='#1A2738',
            paper_bgcolor='#1A2738',
            font=dict(color='#BDC3C7'),
            title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 3. Análisis de Volatilidad
    with tab3:
        st.markdown('<div class="sub-header">📈 ANÁLISIS DE VOLATILIDAD Y RIESGO</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿QUÉ ES LA VOLATILIDAD Y POR QUÉ IMPORTA?</h4>
            <p><strong>La volatilidad es como el "nivel de incertidumbre" o "montaña rusa" del precio:</strong></p>
            <p>• <strong>Alta volatilidad (30%+):</strong> Como una montaña rusa - Grandes subidas y bajadas - Mayor riesgo, mayor potencial de ganancia</p>
            <p>• <strong>Baja volatilidad (10-15%):</strong> Como un paseo en bicicleta - Movimientos suaves - Menor riesgo, más estabilidad</p>
            <p>• <strong>Interpretación práctica:</strong> 20% de volatilidad significa que el precio puede variar ±20% en un año</p>
            <p>• <strong>GARCH:</strong> Es un modelo que "predice" la volatilidad futura basado en patrones pasados</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Volatilidad histórica
        volatility_data = {}
        for symbol in returns.columns:
            vol_request = {"symbol": symbol, "window": 30}
            vol_response = call_api("/volatility", vol_request)
            
            if vol_response and vol_response.get("success"):
                volatility_data[symbol] = vol_response["data"]["historical_volatility"]
        
        if volatility_data:
            st.markdown("### 📊 VOLATILIDAD POR ACTIVO - ¿CUÁL ES MÁS RIESGOSO?")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(volatility_data.keys()),
                y=list(volatility_data.values()),
                name='Volatilidad Anualizada',
                marker_color=['#4A90B8', '#2ECC71', '#F39C12', '#E74C3C', '#9B59B6']
            ))
            
            fig.update_layout(
                title='Volatilidad Anualizada por Activo',
                xaxis_title='Activo',
                yaxis_title='Volatilidad (%)',
                template='plotly_dark',
                height=350,
                plot_bgcolor='#1A2738',
                paper_bgcolor='#1A2738',
                font=dict(color='#BDC3C7'),
                title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Volatilidad en el tiempo
        selected_vol_asset = st.selectbox("Seleccionar Activo para Ver Evolución", options=returns.columns, key="vol_symbol")
        
        if selected_vol_asset:
            with st.spinner('Calculando volatilidad...'):
                vol_request = {"symbol": selected_vol_asset, "window": 30}
                vol_response = call_api("/volatility", vol_request)
                
                if vol_response and vol_response.get("success"):
                    vol_data = vol_response["data"]
                    
                    st.markdown(f"### 📈 EVOLUCIÓN DE VOLATILIDAD - {selected_vol_asset}")
                    
                    fig_vol = go.Figure()
                    # Calcular volatilidad histórica móvil (30 días)
                    rolling_vol = returns[selected_vol_asset].rolling(window=30).std() * np.sqrt(252)
                    
                    fig_vol.add_trace(go.Scatter(
                        x=prices.index,
                        y=rolling_vol,
                        mode='lines',
                        name='Volatilidad Histórica (30 días)',
                        line=dict(color='#4A90B8', width=2)
                    ))
                    
                    # Línea de volatilidad GARCH
                    fig_vol.add_hline(
                        y=vol_data["garch_volatility"],
                        line_dash="dash",
                        line_color="#E74C3C",
                        annotation_text=f"GARCH (Predicción): {vol_data['garch_volatility']:.4f}"
                    )
                    
                    fig_vol.update_layout(
                        title=f'Volatilidad Histórica - {selected_vol_asset}',
                        xaxis_title='Fecha',
                        yaxis_title='Volatilidad',
                        template='plotly_dark',
                        height=350,
                        plot_bgcolor='#1A2738',
                        paper_bgcolor='#1A2738',
                        font=dict(color='#BDC3C7'),
                        title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
                    )
                    
                    st.plotly_chart(fig_vol, use_container_width=True)
    
    # 4. Análisis CAPM
    with tab4:
        st.markdown('<div class="sub-header">🎯 ANÁLISIS CAPM - RIESGO SISTEMÁTICO</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿QUÉ ES EL CAPM Y PARA QUÉ SIRVE?</h4>
            <p><strong>El CAPM nos ayuda a entender cuánto riesgo "del mercado" tiene un activo:</strong></p>
            <p>• <strong>Beta (β):</strong> Mide qué tan "nervioso" es el activo comparado con el mercado (SPY)</p>
            <p>  - β = 1: Se mueve IGUAL que el mercado</p>
            <p>  - β > 1: Es MÁS nervioso - Amplifica los movimientos del mercado</p>
            <p>  - β < 1: Es MENOS nervioso - Amortigua los movimientos del mercado</p>
            <p>• <strong>Alpha (α):</strong> Mide el "valor agregado" - ¿El activo supera al mercado después de ajustar por riesgo?</p>
            <p>• <strong>R-cuadrado (R²):</strong> Qué tan "confiable" es la beta - Si es alto (>0.7), la beta es confiable</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner('Calculando CAPM...'):
            capm_request = {
                "assets": [symbol for symbol in returns.columns if symbol != 'SPY'],
                "market_symbol": "SPY"
            }
            
            capm_response = call_api("/capm", capm_request)
            
            if capm_response and capm_response.get("success"):
                capm_data = capm_response["data"]
                
                # Tabla de Betas
                st.markdown("### 📊 BETAS Y RIESGO SISTEMÁTICO")
                beta_df = pd.DataFrame(capm_data).T
                st.dataframe(beta_df.round(4), use_container_width=True)
                
                # Gráfico de Betas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🎯 CLASIFICACIÓN DE RIESGO POR ACTIVO")
                    
                    for symbol, beta_info in capm_data.items():
                        beta = beta_info['beta']
                        if beta > 1.2:
                            st.markdown(f"""
                            <div class="status-indicator status-sell">
                                🔴 {symbol}: β={beta:.3f} - ALTO RIESGO (Cíclico)
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">Amplifica los movimientos del mercado - Mayor volatilidad</p>
                            """, unsafe_allow_html=True)
                        elif beta > 1.0:
                            st.markdown(f"""
                            <div class="status-indicator status-hold">
                                🟡 {symbol}: β={beta:.3f} - RIESGO MODERADO
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">Ligeramente más volátil que el mercado</p>
                            """, unsafe_allow_html=True)
                        elif beta > 0.8:
                            st.markdown(f"""
                            <div class="status-indicator status-buy">
                                🟢 {symbol}: β={beta:.3f} - BAJO RIESGO
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">Menos volátil que el mercado - Más estable</p>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="status-indicator status-buy">
                                🟢 {symbol}: β={beta:.3f} - DEFENSIVO
                            </div>
                            <p style="color: #BDC3C7; font-size: 0.9rem;">Muy estable - Ideal para tiempos de crisis</p>
                            """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### 📊 GRÁFICO DE BETAS")
                    
                    fig_beta = go.Figure()
                    fig_beta.add_trace(go.Bar(
                        x=list(capm_data.keys()),
                        y=[b['beta'] for b in capm_data.values()],
                        name='Beta',
                        marker_color=['#4A90B8', '#2ECC71', '#F39C12', '#E74C3C']
                    ))
                    
                    # Línea de beta = 1
                    fig_beta.add_hline(y=1, line_dash="dash", line_color="#BDC3C7", annotation_text="Beta = 1 (Mercado)")
                    
                    fig_beta.update_layout(
                        title='Betas de los Activos vs Mercado',
                        xaxis_title='Activo',
                        yaxis_title='Beta (β)',
                        template='plotly_dark',
                        height=350,
                        plot_bgcolor='#1A2738',
                        paper_bgcolor='#1A2738',
                        font=dict(color='#BDC3C7'),
                        title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
                    )
                    
                    st.plotly_chart(fig_beta, use_container_width=True)
    
    # 5. VaR y CVaR
    with tab5:
        st.markdown('<div class="sub-header">⚠️ GESTIÓN DE RIESGO - VALUE AT RISK (VaR) & CVaR</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿CÓMO MEDIR EL RIESGO DE PÉRDIDA?</h4>
            <p><strong>El VaR y CVaR nos ayudan a responder: "¿Cuánto puedo perder en el peor de los casos?"</strong></p>
            <p>• <strong>Value at Risk (VaR):</strong> "¿Cuál es la MÁXIMA pérdida que puedo tener en un día normal?"</p>
            <p>  - Ejemplo: VaR = 0.03 (3%) con 95% confianza → Hay 95% de probabilidad de no perder más del 3% en un día</p>
            <p>  - Si tienes $10,000 invertidos → Pérdida máxima esperada: $300 (en el 95% de los días)</p>
            <p>• <strong>Conditional VaR (CVaR):</strong> "¿Cuánto pierdo en los DÍAS PEORES (el 5% restante)?</p>
            <p>  - Ejemplo: CVaR = 0.05 (5%) → En los peores días (5% del tiempo), la pérdida promedio es 5%</p>
            <p>• <strong>Diferencia clave:</strong> VaR te dice el límite "normal", CVaR te dice qué pasa cuando las cosas salen MAL</p>
        </div>
        """, unsafe_allow_html=True)
        
        var_data = {}
        cvar_data = {}
        
        for symbol in returns.columns:
            with st.spinner(f'Calculando riesgo para {symbol}...'):
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
        
        st.markdown("### 📊 MÉTRICAS DE RIESGO POR ACTIVO")
        st.dataframe(risk_df.round(4), use_container_width=True)
        
        # Gráficos de riesgo
        col1, col2 = st.columns(2)
        
        # Mapa de colores por activo
        color_map = {
            'AAPL': '#4A90B8',
            'MSFT': '#2ECC71',
            'XOM': '#F39C12',
            'KO': '#E74C3C',
            'SPY': '#9B59B6'
        }
        
        with col1:
            st.markdown("### ⚠️ VALUE AT RISK (VaR)")
            
            fig_var = go.Figure()
            fig_var.add_trace(go.Bar(
                x=risk_df.index,
                y=risk_df['VaR'],
                name=f'VaR ({(1-confidence_level)*100:.0f}% Confianza)',
                marker_color=[color_map.get(asset, '#FF6B6B') for asset in risk_df.index],
                marker_line_color='#2C3E50',
                marker_line_width=2
            ))
            
            fig_var.update_layout(
                title=f'Value at Risk - {(1-confidence_level)*100:.0f}% de Confianza',
                xaxis_title='Activo',
                yaxis_title='VaR (Pérdida Máxima Esperada)',
                template='plotly_dark',
                height=350,
                plot_bgcolor='#1A2738',
                paper_bgcolor='#1A2738',
                font=dict(color='#BDC3C7'),
                title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif'),
                xaxis=dict(showgrid=True, gridcolor='#2C3E50', gridwidth=1),
                yaxis=dict(showgrid=True, gridcolor='#2C3E50', gridwidth=1)
            )
            
            st.plotly_chart(fig_var, use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ CONDITIONAL VaR (CVaR)")
            
            fig_cvar = go.Figure()
            fig_cvar.add_trace(go.Bar(
                x=risk_df.index,
                y=risk_df['CVaR'],
                name='CVaR (Pérdida en Peor Escenario)',
                marker_color=[color_map.get(asset, '#8B0000') for asset in risk_df.index],
                marker_line_color='#2C3E50',
                marker_line_width=2
            ))
            
            fig_cvar.update_layout(
                title='Conditional Value at Risk (Pérdida en Peores Días)',
                xaxis_title='Activo',
                yaxis_title='CVaR',
                template='plotly_dark',
                height=350,
                plot_bgcolor='#1A2738',
                paper_bgcolor='#1A2738',
                font=dict(color='#BDC3C7'),
                title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif'),
                xaxis=dict(showgrid=True, gridcolor='#2C3E50', gridwidth=1),
                yaxis=dict(showgrid=True, gridcolor='#2C3E50', gridwidth=1)
            )
            
            st.plotly_chart(fig_cvar, use_container_width=True)
    
    # 6. Optimización Markowitz
    with tab6:
        st.markdown('<div class="sub-header">⚖️ OPTIMIZACIÓN DE PORTAFOLIO - TEORÍA MODERNA</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿CÓMO CONSTRUIR EL PORTAFOLIO PERFECTO?</h4>
            <p><strong>La Teoría Moderna de Portafolio nos ayuda a encontrar el equilibrio perfecto entre riesgo y retorno:</strong></p>
            <p>• <strong>Portafolio de Mínima Varianza:</strong> "El más SEGURO posible" - Minimiza el riesgo mediante diversificación inteligente</p>
            <p>  - Ideal para inversores conservadores o en tiempos de incertidumbre</p>
            <p>  - Combina activos que no se mueven juntos para reducir la volatilidad total</p>
            <p>• <strong>Portafolio de Máximo Sharpe:</strong> "El más EFICIENTE posible" - Máximo retorno por cada unidad de riesgo</p>
            <p>  - Ideal para inversores que buscan el mejor equilibrio riesgo-retorno</p>
            <p>  - Es el portafolio "óptimo" en la frontera eficiente</p>
            <p>• <strong>Sharpe Ratio:</strong> Mide la "eficiencia" - ¿Cuánto retorno obtengo por cada unidad de riesgo?</p>
            <p>  - > 2: Excelente | 1-2: Bueno | < 1: Regular</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                    st.markdown("### 🎯 PORTAFOLIO DE MÍNIMA VARIANZA (El Más Seguro)")
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: 900; color: #2ECC71;">{min_var_data['expected_return']:.2%}</div>
                        <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Retorno Anual Esperado</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: 900; color: #F39C12;">{min_var_data['volatility']:.2%}</div>
                        <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Riesgo (Volatilidad)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: 900; color: #4A90B8;">{min_var_data['sharpe_ratio']:.2f}</div>
                        <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Sharpe Ratio (Eficiencia)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Gráfico de pesos
                    weights_df = pd.DataFrame(list(min_var_data['weights'].items()), columns=['Activo', 'Peso'])
                    
                    # Asignar colores específicos por activo
                    color_map = {
                        'AAPL': '#4A90B8',
                        'MSFT': '#2ECC71',
                        'XOM': '#F39C12',
                        'KO': '#E74C3C',
                        'SPY': '#9B59B6'
                    }
                    
                    fig_min_var = px.pie(weights_df, values='Peso', names='Activo', title="Composición - Mínima Varianza",
                                        color='Activo',
                                        color_discrete_map=color_map)
                    st.plotly_chart(fig_min_var, use_container_width=True)
                
                with col2:
                    st.markdown("### 🎯 PORTAFOLIO DE MÁXIMO SHARPE (El Más Eficiente)")
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: 900; color: #2ECC71;">{max_sharpe_data['expected_return']:.2%}</div>
                        <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Retorno Anual Esperado</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: 900; color: #F39C12;">{max_sharpe_data['volatility']:.2%}</div>
                        <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Riesgo (Volatilidad)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: 900; color: #4A90B8;">{max_sharpe_data['sharpe_ratio']:.2f}</div>
                        <div style="color: #BDC3C7; text-transform: uppercase; font-size: 0.9rem;">Sharpe Ratio (Eficiencia)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Gráfico de pesos
                    weights_df = pd.DataFrame(list(max_sharpe_data['weights'].items()), columns=['Activo', 'Peso'])
                    
                    # Usar el mismo mapa de colores
                    fig_max_sharpe = px.pie(weights_df, values='Peso', names='Activo', title="Composición - Máximo Sharpe",
                                           color='Activo',
                                           color_discrete_map=color_map)
                    st.plotly_chart(fig_max_sharpe, use_container_width=True)
    
    # 7. Señales de Trading
    with tab7:
        st.markdown('<div class="sub-header">🎯 SISTEMA DE SEÑALES DE TRADING</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿CÓMO FUNCIONA EL SISTEMA DE SEÑALES?</h4>
            <p><strong>Nuestro sistema combina dos indicadores poderosos para generar señales de compra/venta:</strong></p>
            <p>• <strong>Señal de COMPRA (BUY):</strong> Cuando se cumplen DOS condiciones:</p>
            <p>  1. SMA 20 > SMA 50 (tendencia alcista confirmada)</p>
            <p>  2. RSI < 30 (el activo está "barato" - sobrevendido)</p>
            <p>• <strong>Señal de VENTA (SELL):</strong> Cuando se cumplen DOS condiciones:</p>
            <p>  1. SMA 20 < SMA 50 (tendencia bajista confirmada)</p>
            <p>  2. RSI > 70 (el activo está "caro" - sobrecomprado)</p>
            <p>• <strong>Señal NEUTRAL (HOLD):</strong> Cuando no se cumplen ambas condiciones simultáneamente</p>
            <p><strong>En el gráfico:</strong> Los triángulos verdes (▲) muestran dónde hubieran sido buenas compras, los rojos (▼) dónde hubieran sido buenas ventas</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            st.markdown("### 📊 RESUMEN DE SEÑALES ACTUALES")
            st.dataframe(signals_df, use_container_width=True)
            
            # Gráficos de señales
            selected_signal_asset = st.selectbox("Seleccionar Activo para Ver Histórico de Señales", options=returns.columns, key="signal_symbol")
            
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
                    line=dict(color='#4A90B8', width=2)
                ))
                
                # Calcular señales históricas basadas en SMA y RSI
                close_prices = prices[selected_signal_asset]
                
                # SMA 20 y SMA 50
                sma_20 = close_prices.rolling(window=20).mean()
                sma_50 = close_prices.rolling(window=50).mean()
                
                # RSI
                delta = close_prices.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                # Identificar señales de compra y venta a lo largo del tiempo
                buy_dates = []
                sell_dates = []
                buy_prices = []
                sell_prices = []
                
                for i in range(50, len(close_prices)):  # Empezar después de que SMA50 tenga datos
                    # Señal de COMPRA: SMA20 > SMA50 y RSI < 30
                    if sma_20.iloc[i] > sma_50.iloc[i] and rsi.iloc[i] < 30:
                        buy_dates.append(close_prices.index[i])
                        buy_prices.append(close_prices.iloc[i])
                    # Señal de VENTA: SMA20 < SMA50 y RSI > 70
                    elif sma_20.iloc[i] < sma_50.iloc[i] and rsi.iloc[i] > 70:
                        sell_dates.append(close_prices.index[i])
                        sell_prices.append(close_prices.iloc[i])
                
                # Mostrar señales de COMPRA en el gráfico
                if buy_dates:
                    fig_signals.add_trace(go.Scatter(
                        x=buy_dates,
                        y=buy_prices,
                        mode='markers',
                        name='Señales de COMPRA (▲)',
                        marker=dict(color='#2ECC71', symbol='triangle-up', size=15),
                        text=[f'COMPRA<br>Precio: ${p:.2f}<br>RSI: {rsi.loc[d]:.2f}' for d, p in zip(buy_dates, buy_prices)],
                        hoverinfo='text'
                    ))
                
                # Mostrar señales de VENTA en el gráfico
                if sell_dates:
                    fig_signals.add_trace(go.Scatter(
                        x=sell_dates,
                        y=sell_prices,
                        mode='markers',
                        name='Señales de VENTA (▼)',
                        marker=dict(color='#E74C3C', symbol='triangle-down', size=15),
                        text=[f'VENTA<br>Precio: ${p:.2f}<br>RSI: {rsi.loc[d]:.2f}' for d, p in zip(sell_dates, sell_prices)],
                        hoverinfo='text'
                    ))
                
                # Si no hay señales históricas, mostrar mensaje
                if not buy_dates and not sell_dates:
                    fig_signals.add_annotation(
                        x=prices.index[len(prices)//2],
                        y=close_prices.iloc[len(close_prices)//2],
                        text="No hay señales claras de compra/venta en el período analizado",
                        showarrow=False,
                        font=dict(size=14, color="#BDC3C7"),
                        bgcolor="rgba(74, 144, 184, 0.8)",
                        bordercolor="#4A90B8",
                        borderwidth=1,
                        borderpad=10
                    )
                
                fig_signals.update_layout(
                    title=f'Histórico de Señales de Trading - {selected_signal_asset}',
                    xaxis_title='Fecha',
                    yaxis_title='Precio ($)',
                    template='plotly_dark',
                    height=400,
                    plot_bgcolor='#1A2738',
                    paper_bgcolor='#1A2738',
                    font=dict(color='#BDC3C7'),
                    title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
                )
                
                st.plotly_chart(fig_signals, use_container_width=True)
    
    # 8. Comparación con Benchmark
    with tab8:
        st.markdown('<div class="sub-header">🏆 ANÁLISIS VS BENCHMARK (S&P 500)</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>💡 ¿CÓMO SE DESEMPEÑAN NUESTROS ACTIVOS VS EL MERCADO?</h4>
            <p><strong>Comparamos cada activo contra el S&P 500 (SPY) para ver si superan o no al mercado:</strong></p>
            <p>• <strong>Retornos Acumulados:</strong> Muestra cuánto hubiera ganado $1 invertido en cada activo a lo largo del tiempo</p>
            <p>  - Línea más alta = Mejor desempeño vs el mercado</p>
            <p>• <strong>Alpha (α):</strong> El "valor agregado" - ¿El activo supera al mercado después de ajustar por riesgo?</p>
            <p>  - Alpha positivo = Supera al mercado (¡Excelente!)</p>
            <p>  - Alpha negativo = Bajo desempeño vs el mercado</p>
            <p>• <strong>Beta (β):</strong> Qué tan "nervioso" es comparado con el mercado</p>
            <p>• <strong>Information Ratio:</strong> Mide la "eficiencia" en generar alpha - ¿Vale la pena el riesgo extra?</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                
                colors = ['#4A90B8', '#2ECC71', '#F39C12', '#E74C3C', '#9B59B6']
                for i, symbol in enumerate(returns.columns):
                    fig_benchmark.add_trace(go.Scatter(
                        x=cumulative_returns.index,
                        y=cumulative_returns[symbol],
                        mode='lines',
                        name=symbol,
                        line=dict(color=colors[i % len(colors)], width=2)
                    ))
                
                fig_benchmark.update_layout(
                    title='Retornos Acumulados vs Benchmark (S&P 500)',
                    xaxis_title='Fecha',
                    yaxis_title='Retorno Acumulado',
                    template='plotly_dark',
                    height=400,
                    plot_bgcolor='#1A2738',
                    paper_bgcolor='#1A2738',
                    font=dict(color='#BDC3C7', size=11),
                    title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif'),
                    legend=dict(
                        font=dict(size=12, color='#FFFFFF'),
                        bgcolor='rgba(26, 39, 56, 0.8)',
                        bordercolor='#4A90B8',
                        borderwidth=1
                    )
                )
                
                st.plotly_chart(fig_benchmark, use_container_width=True)
                
                # Métricas de performance vs benchmark
                performance_df = pd.DataFrame(benchmark_data).T
                st.markdown("### 📊 MÉTRICAS DE PERFORMANCE VS BENCHMARK")
                st.dataframe(performance_df.round(4), use_container_width=True)
                
                # Gráfico de Alpha
                if not performance_df.empty:
                    st.markdown("### 📈 ALPHA - ¿QUIÉN SUPERA AL MERCADO?")
                    
                    fig_alpha = go.Figure()
                    fig_alpha.add_trace(go.Bar(
                        x=performance_df.index,
                        y=performance_df['alpha'],
                        name='Alpha',
                        marker_color=['#2ECC71' if x > 0 else '#E74C3C' for x in performance_df['alpha']]
                    ))
                    
                    fig_alpha.add_hline(y=0, line_dash="dash", line_color="#BDC3C7")
                    fig_alpha.update_layout(
                        title='Alpha vs Benchmark (S&P 500) - Valor Agregado',
                        xaxis_title='Activo',
                        yaxis_title='Alpha (α)',
                        template='plotly_dark',
                        height=350,
                        plot_bgcolor='#1A2738',
                        paper_bgcolor='#1A2738',
                        font=dict(color='#BDC3C7'),
                        title_font=dict(color='#FFFFFF', size=14, family='Arial, sans-serif')
                    )
                    
                    st.plotly_chart(fig_alpha, use_container_width=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #1A2738 0%, #2C3E50 100%); border-radius: 16px; border: 1px solid #34495E;">
        <h2 style="color: #4A90B8; font-size: 2.5rem; margin-bottom: 1rem;">🚀 SISTEMA DE GESTIÓN DE PORTAFOLIO</h2>
        <p style="color: #BDC3C7; font-size: 1.1rem; margin-bottom: 2rem;">Haga clic en "ACTUALIZAR DATOS" para comenzar el análisis profesional</p>
        <p style="color: #7F8C8D; font-size: 0.9rem;">
            <strong>Activos disponibles:</strong> Apple (AAPL), Microsoft (MSFT), Exxon (XOM), Coca-Cola (KO), S&P 500 (SPY)<br>
            <strong>Nota:</strong> Asegúrate de que el Backend FastAPI esté corriendo en <code style="background: #34495E; padding: 0.2rem 0.5rem; border-radius: 4px;">http://localhost:8000</code>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <strong>Sistema Profesional de Gestión de Portafolio</strong> | Backend FastAPI + Frontend Streamlit<br>
    Proyecto Universitario - Análisis de Riesgo Financiero con Portafolio | 2024
</div>
""", unsafe_allow_html=True)