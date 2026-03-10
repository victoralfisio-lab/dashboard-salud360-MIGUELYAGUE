import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 🎨 1. CONFIGURACIÓN ESTÉTICA (ESTILO APP)
# ==========================================
st.set_page_config(page_title="Salud 360 - Miguel Yagüe", layout="wide")

# COLORES CORPORATIVOS
C_AZUL = "#223A76"
C_AZUL_C = "#72B7E2"
C_VERDE = "#27AE60"
C_ROJO = "#E74C3C"
C_NARANJA = "#F39C12"
C_GRIS = "#6B7280"
C_BG = "#F8FAFC"

# INYECCIÓN DE CSS PARA TARJETAS Y SOMBRAS
st.markdown(f"""
    <style>
    .main {{ background-color: {C_BG}; }}
    [data-testid="stMetricValue"] {{ color: {C_AZUL}; font-size: 36px; font-weight: 800; }}
    .kpi-card {{
        background-color: white;
        padding: 24px;
        border-radius: 20px;
        border-left: 6px solid {C_AZUL};
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    .kpi-title {{ color: {C_GRIS}; font-size: 14px; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px; text-transform: uppercase; }}
    .kpi-value {{ color: {C_AZUL}; font-size: 32px; font-weight: 800; margin: 0; }}
    .kpi-unit {{ font-size: 16px; font-weight: 500; color: {C_GRIS}; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🔗 2. CONEXIÓN A DATOS (GOOGLE SHEETS)
# ==========================================
SHEET_ID = "1IryC88kzy0mZHjwYgCkoGJ8vEyVRcP2ecI5RL2qhMFM"
GID = "1724629829"  # Hoja: MAKE
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)
def load_data():
    data = pd.read_csv(url)
    # TRUCO: Renombrar columnas a letras (A, B, C...) para evitar fallos de escritura
    def excel_col(n):
        res = ""
        while n >= 0:
            res = chr(n % 26 + 65) + res
            n = n // 26 - 1
        return res
    data.columns = [excel_col(i) for i in range(len(data.columns))]
    return data

# ==========================================
# 🏗️ 3. CONSTRUCCIÓN DEL DASHBOARD
# ==========================================
try:
    df = load_data()
    ultima_fila = df.iloc[-1] # El último registro del cliente

    # --- ENCABEZADO ---
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 0;'>⚡ SALUD 360</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {C_GRIS}; font-weight: 500;'>MÉTODO EVOLUCIÓN INTEGRAL | MIGUEL YAGÜE</p>", unsafe_allow_html=True)
    st.write("---")

    # --- BLOQUE 1: KPIs (SEGÚN CAPTURA) ---
    st.markdown("### 📍 ESTADO ACTUAL")
    k1, k2, k3, k4 = st.columns(4)

    # TARJETA 1: BIENESTAR (AX)
    with k1:
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: {C_AZUL};">
                <p class="kpi-title">🌟 BIENESTAR GLOBAL</p>
                <p class="kpi-value">{ultima_fila['AX']:.1f} <span class="kpi-unit">/ 10</span></p>
            </div>
        """, unsafe_allow_html=True)

    # TARJETA 2: PASOS (T)
    with k2:
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: {C_VERDE};">
                <p class="kpi-title">👟 PASOS DIARIOS</p>
                <p class="kpi-value">{int(ultima_fila['T']):,}</p>
            </div>
        """, unsafe_allow_html=True)

    # TARJETA 3: SUEÑO (AJ)
    with k3:
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: {C_AZUL_C};">
                <p class="kpi-title">🌙 HORAS SUEÑO</p>
                <p class="kpi-value">{ultima_fila['AJ']:.1f} <span class="kpi-unit">h</span></p>
            </div>
        """, unsafe_allow_html=True)

    # TARJETA 4: DOLOR (I)
    with k4:
        val_dolor = float(ultima_fila['I'])
        color_dol = C_ROJO if val_dolor > 4 else C_NARANJA
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: {color_dol};">
                <p class="kpi-title">💥 NIVEL DOLOR</p>
                <p class="kpi-value">{val_dolor:.1f} <span class="kpi-unit">/ 10</span></p>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.info("💡 Esperando la siguiente captura para generar el próximo bloque visual...")

except Exception as e:
    st.error(f"❌ ERROR AL CARGAR DATOS: {e}")
    st.warning("Revisa que la hoja 'MAKE' sea pública y tenga los datos en las columnas correctas.")
