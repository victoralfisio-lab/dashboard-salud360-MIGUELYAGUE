import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Salud 360", layout="wide")

# Estilos
st.markdown("""
    <style>
    .main { background-color: #F7F9FC; }
    [data-testid="stMetricValue"] { color: #223A76; font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 SALUD 360: DASHBOARD EVOLUCIÓN")

# --- CONEXIÓN ---
SHEET_ID = "1IryC88kzy0mZHjwYgCkoGJ8vEyVRcP2ecI5RL2qhMFM"
GID = "1724629829"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60)
def load_data():
    # Leemos el CSV y forzamos que no use la primera fila como nombres si da error
    data = pd.read_csv(url)
    return data

try:
    df = load_data()
    
    # --- MAGIA: Renombramos las columnas por su LETRA de Excel ---
    # Esto hace que no importe qué nombre tengan en el Excel
    def col_name(n):
        res = ""
        while n >= 0:
            res = chr(n % 26 + 65) + res
            n = n // 26 - 1
        return res
    
    df.columns = [col_name(i) for i in range(len(df.columns))]

    # --- DATOS ÚLTIMA FILA ---
    last_row = df.iloc[-1]

    # --- KPIs ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("BIENESTAR GLOBAL", f"{last_row['AX']}")
    c2.metric("PASOS", f"{last_row['T']}")
    c3.metric("ESTRÉS", f"{last_row['H']}/10")
    c4.metric("DOLOR", f"{last_row['I']}/10")

    st.divider()

    # --- GRÁFICOS ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 Evolución Bienestar")
        fig1 = px.area(df, x='B', y='AX', color_discrete_sequence=["#223A76"])
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.subheader("🧠 Estrés (Rojo) vs Dolor (Naranja)")
        fig2 = px.line(df, x='B', y=['H', 'I'], color_discrete_map={'H': '#E74C3C', 'I': '#F39C12'})
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📝 Notas Recientes")
    st.table(df[['B', 'AE']].tail(5))

except Exception as e:
    st.error(f"Error al leer las columnas. Detalles: {e}")
    st.info("Revisa que la hoja 'MAKE' tenga datos y que el enlace sea público.")
