import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Configuración de la página
st.set_page_config(
    page_title="📈 Análisis de Acciones Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para móvil
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1F4E78;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .buy-signal {
        background-color: #C6EFCE;
        color: #006100;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    .sell-signal {
        background-color: #FFC7CE;
        color: #9C0006;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    .hold-signal {
        background-color: #FFEB9C;
        color: #9C5700;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1F4E78;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Funciones de cálculo de indicadores técnicos

def calculate_sma(data, period):
    """Calcula Simple Moving Average"""
    return data['Close'].rolling(window=period).mean()

def calculate_ema(data, period):
    """Calcula Exponential Moving Average"""
    return data['Close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """Calcula Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data):
    """Calcula MACD"""
    ema12 = calculate_ema(data, 12)
    ema26 = calculate_ema(data, 26)
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_bollinger_bands(data, period=20):
    """Calcula Bollinger Bands"""
    sma = calculate_sma(data, period)
    std = data['Close'].rolling(window=period).std()
    upper = sma + (std * 2)
    lower = sma - (std * 2)
    bb_percent = (data['Close'] - lower) / (upper - lower)
    return upper, sma, lower, bb_percent

def calculate_technical_score(data):
    """Calcula score técnico basado en múltiples indicadores"""
    if len(data) < 200:
        return None, "Datos insuficientes (necesita al menos 200 días)"
    
    latest = data.iloc[-1]
    
    score = 0
    signals = {}
    
    # SMA 20
    sma20 = calculate_sma(data, 20).iloc[-1]
    if latest['Close'] > sma20:
        score += 15
        signals['SMA 20'] = '🟢 Alcista'
    else:
        signals['SMA 20'] = '🔴 Bajista'
    
    # SMA 50
    sma50 = calculate_sma(data, 50).iloc[-1]
    if latest['Close'] > sma50:
        score += 15
        signals['SMA 50'] = '🟢 Alcista'
    else:
        signals['SMA 50'] = '🔴 Bajista'
    
    # SMA 200
    sma200 = calculate_sma(data, 200).iloc[-1]
    if latest['Close'] > sma200:
        score += 20
        signals['SMA 200'] = '🟢 Alcista'
    else:
        signals['SMA 200'] = '🔴 Bajista'
    
    # Golden/Death Cross
    if sma50 > sma200:
        signals['Cross 50/200'] = '🟢 Golden Cross'
    else:
        signals['Cross 50/200'] = '🔴 Death Cross'
    
    # RSI
    rsi = calculate_rsi(data).iloc[-1]
    if 40 <= rsi <= 60:
        score += 15
        signals['RSI'] = f'🟢 Neutral ({rsi:.1f})'
    elif rsi < 40:
        score += 10
        signals['RSI'] = f'🟡 Sobreventa ({rsi:.1f})'
    else:
        score += 5
        signals['RSI'] = f'⚠️ Sobrecompra ({rsi:.1f})'
    
    # MACD
    macd, signal_line, histogram = calculate_macd(data)
    if macd.iloc[-1] > signal_line.iloc[-1]:
        score += 15
        signals['MACD'] = '🟢 Alcista'
    else:
        signals['MACD'] = '🔴 Bajista'
    
    # Volumen
    vol_avg = data['Volume'].tail(20).mean()
    vol_ratio = latest['Volume'] / vol_avg
    if vol_ratio > 1.5:
        score += 10
        signals['Volumen'] = f'🟢 Alto ({vol_ratio:.2f}x)'
    elif vol_ratio > 1:
        score += 5
        signals['Volumen'] = f'🟡 Normal ({vol_ratio:.2f}x)'
    else:
        signals['Volumen'] = f'🔴 Bajo ({vol_ratio:.2f}x)'
    
    # Bollinger Bands
    bb_upper, bb_middle, bb_lower, bb_percent = calculate_bollinger_bands(data)
    bb_pct = bb_percent.iloc[-1]
    if 0.2 < bb_pct < 0.8:
        score += 10
        signals['Bollinger'] = f'🟢 Medio ({bb_pct:.1%})'
    elif bb_pct <= 0.2:
        signals['Bollinger'] = f'🟡 Cerca inferior ({bb_pct:.1%})'
        score += 5
    else:
        signals['Bollinger'] = f'⚠️ Cerca superior ({bb_pct:.1%})'
        score += 5
    
    return score, signals

def get_recommendation(score):
    """Genera recomendación basada en score"""
    if score >= 75:
        return "🟢 COMPRA FUERTE", "buy"
    elif score >= 60:
        return "🟢 COMPRA", "buy"
    elif score >= 45:
        return "🟡 OBSERVAR", "hold"
    elif score >= 30:
        return "🟠 PRECAUCIÓN", "hold"
    else:
        return "🔴 EVITAR", "sell"

# Función simulada para obtener datos (ya que no tenemos acceso a internet)
def get_stock_data_demo(ticker):
    """
    Función demo que genera datos simulados.
    En producción, esto se reemplazaría con yfinance o API real.
    """
    # Generar 300 días de datos simulados
    dates = pd.date_range(end=datetime.now(), periods=300, freq='D')
    
    # Simular precios con tendencia y volatilidad
    np.random.seed(hash(ticker) % 2**32)
    
    base_price = np.random.uniform(2, 10)
    trend = np.random.uniform(-0.001, 0.003)
    volatility = np.random.uniform(0.01, 0.03)
    
    prices = [base_price]
    for i in range(1, 300):
        change = np.random.normal(trend, volatility)
        new_price = prices[-1] * (1 + change)
        prices.append(max(0.5, new_price))  # Evitar precios negativos
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'Low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        'Close': prices,
        'Volume': [int(np.random.uniform(500000, 5000000)) for _ in range(300)]
    })
    
    df.set_index('Date', inplace=True)
    return df

# INTERFAZ PRINCIPAL
st.markdown('<div class="main-header">📈 Análisis de Acciones Profesional</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    analysis_mode = st.radio(
        "Modo de análisis:",
        ["🎯 Acción Individual", "📊 Lista de Acciones"]
    )
    
    st.markdown("---")
    
    if analysis_mode == "🎯 Acción Individual":
        ticker = st.text_input(
            "Ticker de la acción:",
            placeholder="Ej: PNG.V, AAPL, MSFT",
            help="Ingresa el símbolo de la acción a analizar"
        ).upper()
        
        analyze_button = st.button("🔍 ANALIZAR", type="primary")
    
    else:
        tickers_input = st.text_area(
            "Lista de tickers (uno por línea):",
            placeholder="PNG.V\nAAPL\nMSFT\nGOOGL",
            height=150,
            help="Ingresa múltiples tickers, uno por línea"
        )
        
        analyze_button = st.button("🔍 ANALIZAR TODAS", type="primary")
    
    st.markdown("---")
    st.info("""
    **💡 Cómo funciona:**
    
    1. Ingresa ticker(s)
    2. Click en ANALIZAR
    3. Recibe recomendación
    
    **Indicadores usados:**
    - SMA 20/50/200
    - RSI, MACD
    - Bollinger Bands
    - Análisis de volumen
    """)

# ÁREA PRINCIPAL
if analysis_mode == "🎯 Acción Individual":
    if analyze_button and ticker:
        with st.spinner(f'Analizando {ticker}... 📊'):
            try:
                # Nota: En producción, usar yfinance aquí
                # import yfinance as yf
                # data = yf.download(ticker, period="1y", progress=False)
                
                # Por ahora usamos datos demo
                data = get_stock_data_demo(ticker)
                
                if data.empty:
                    st.error(f"❌ No se pudieron obtener datos para {ticker}")
                else:
                    # Calcular score técnico
                    score, signals = calculate_technical_score(data)
                    
                    if score is None:
                        st.error(signals)  # signals contiene el mensaje de error
                    else:
                        recommendation, rec_type = get_recommendation(score)
                        
                        # Mostrar resultados principales
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "💰 Precio Actual",
                                f"${data['Close'].iloc[-1]:.2f}",
                                f"{((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1) * 100):.2f}%"
                            )
                        
                        with col2:
                            st.metric(
                                "📊 Score Técnico",
                                f"{score}/100",
                                delta_color="off"
                            )
                        
                        with col3:
                            st.metric(
                                "📈 Volumen",
                                f"{data['Volume'].iloc[-1]:,.0f}",
                                delta_color="off"
                            )
                        
                        # Recomendación principal
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        if rec_type == "buy":
                            st.markdown(f'<div class="buy-signal">{recommendation}</div>', unsafe_allow_html=True)
                        elif rec_type == "sell":
                            st.markdown(f'<div class="sell-signal">{recommendation}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="hold-signal">{recommendation}</div>', unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Señales detalladas
                        st.subheader("📋 Señales Detalladas")
                        
                        cols = st.columns(2)
                        signal_items = list(signals.items())
                        
                        for idx, (indicator, signal) in enumerate(signal_items):
                            with cols[idx % 2]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <strong>{indicator}:</strong><br>
                                    {signal}
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Información adicional
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.subheader("📊 Datos Adicionales")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            sma20 = calculate_sma(data, 20).iloc[-1]
                            sma50 = calculate_sma(data, 50).iloc[-1]
                            sma200 = calculate_sma(data, 200).iloc[-1]
                            
                            st.write(f"**SMA 20:** ${sma20:.2f}")
                            st.write(f"**SMA 50:** ${sma50:.2f}")
                            st.write(f"**SMA 200:** ${sma200:.2f}")
                        
                        with col2:
                            bb_upper, bb_middle, bb_lower, _ = calculate_bollinger_bands(data)
                            st.write(f"**BB Superior:** ${bb_upper.iloc[-1]:.2f}")
                            st.write(f"**BB Media:** ${bb_middle.iloc[-1]:.2f}")
                            st.write(f"**BB Inferior:** ${bb_lower.iloc[-1]:.2f}")
                        
                        # Niveles de trading
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.subheader("🎯 Niveles de Trading")
                        
                        current_price = data['Close'].iloc[-1]
                        support = bb_lower.iloc[-1]
                        resistance = bb_upper.iloc[-1]
                        stop_loss = support * 0.97
                        
                        st.write(f"**💵 Precio Actual:** ${current_price:.2f}")
                        st.write(f"**🟢 Soporte (BB Inf):** ${support:.2f}")
                        st.write(f"**🔴 Resistencia (BB Sup):** ${resistance:.2f}")
                        st.write(f"**🛑 Stop Loss Sugerido:** ${stop_loss:.2f} (-3% desde soporte)")
                        
                        # Gráfico simple de precio
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.subheader("📈 Gráfico de Precio (últimos 90 días)")
                        st.line_chart(data['Close'].tail(90))
            
            except Exception as e:
                st.error(f"❌ Error al analizar {ticker}: {str(e)}")
    
    elif analyze_button:
        st.warning("⚠️ Por favor ingresa un ticker")

else:  # Modo lista de acciones
    if analyze_button and tickers_input:
        tickers = [t.strip().upper() for t in tickers_input.split('\n') if t.strip()]
        
        if not tickers:
            st.warning("⚠️ Por favor ingresa al menos un ticker")
        else:
            st.subheader(f"📊 Analizando {len(tickers)} acciones...")
            
            results = []
            progress_bar = st.progress(0)
            
            for idx, ticker in enumerate(tickers):
                try:
                    # Simular datos (reemplazar con yfinance en producción)
                    import yfinance as yf
data = yf.download(ticker, period="1y", progress=False)
                    
                    if not data.empty:
                        score, signals = calculate_technical_score(data)
                        
                        if score is not None:
                            recommendation, rec_type = get_recommendation(score)
                            
                            results.append({
                                'Ticker': ticker,
                                'Precio': data['Close'].iloc[-1],
                                'Score': score,
                                'Recomendación': recommendation,
                                'Tipo': rec_type
                            })
                
                except Exception as e:
                    st.warning(f"⚠️ Error con {ticker}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(tickers))
            
            progress_bar.empty()
            
            if results:
                # Ordenar por score
                results_df = pd.DataFrame(results).sort_values('Score', ascending=False)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("🏆 Ranking de Acciones")
                
                # Mostrar top 3
                st.markdown("### 🥇 Top 3 Oportunidades")
                
                for idx, row in results_df.head(3).iterrows():
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
                        
                        with col1:
                            st.markdown(f"**{row['Ticker']}**")
                        with col2:
                            st.markdown(f"${row['Precio']:.2f}")
                        with col3:
                            st.markdown(f"**{row['Score']}/100**")
                        with col4:
                            if row['Tipo'] == 'buy':
                                st.markdown(f"<span style='color: green;'>{row['Recomendación']}</span>", unsafe_allow_html=True)
                            elif row['Tipo'] == 'sell':
                                st.markdown(f"<span style='color: red;'>{row['Recomendación']}</span>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<span style='color: orange;'>{row['Recomendación']}</span>", unsafe_allow_html=True)
                        
                        st.markdown("---")
                
                # Tabla completa
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📋 Tabla Completa")
                
                # Formatear para display
                display_df = results_df.copy()
                display_df['Precio'] = display_df['Precio'].apply(lambda x: f"${x:.2f}")
                display_df = display_df[['Ticker', 'Precio', 'Score', 'Recomendación']]
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Estadísticas
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    buy_count = len(results_df[results_df['Tipo'] == 'buy'])
                    st.metric("🟢 Señales COMPRA", buy_count)
                
                with col2:
                    hold_count = len(results_df[results_df['Tipo'] == 'hold'])
                    st.metric("🟡 Señales OBSERVAR", hold_count)
                
                with col3:
                    sell_count = len(results_df[results_df['Tipo'] == 'sell'])
                    st.metric("🔴 Señales EVITAR", sell_count)
            
            else:
                st.error("❌ No se pudieron analizar las acciones")
    
    elif analyze_button:
        st.warning("⚠️ Por favor ingresa una lista de tickers")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>📊 Sistema de Análisis Técnico Profesional</p>
    <p>⚠️ Este sistema es educativo. No es asesoría financiera.</p>
    <p>💡 Siempre consulta con un profesional antes de invertir.</p>
</div>
""", unsafe_allow_html=True)
