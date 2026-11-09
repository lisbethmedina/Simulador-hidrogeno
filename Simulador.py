import numpy as np
import streamlit as st
import plotly.graph_objects as go

# ============================================================
# CONSTANTES FÍSICAS
# ============================================================
ENERGIA_HIDROGENO_EV = 13.605693122994
CONSTANTE_PLANCK_JS = 6.62607015e-34
CARGA_ELECTRON_C = 1.602176634e-19

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Simulador del Átomo de Hidrógeno",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ESTILOS DE LA INTERFAZ (CSS)
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    h1, h2, h3, p, label, div[data-testid="stMarkdownContainer"] {
        color: #f8fafc;
    }
    .encabezado {
        padding: 1.5rem;
        border-left: 5px solid #38bdf8;
        border-radius: 8px;
        background: rgba(30, 41, 59, 0.8);
        margin-bottom: 2rem;
    }
    .encabezado h1 {
        margin: 0;
        font-size: 2.2rem;
        color: #38bdf8;
    }
    .nota {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .stMetric {
        background-color: rgba(30, 41, 59, 0.6);
        padding: 10px;
        border-radius: 8px;
    }

    /* Cuadro de interpretación de los orbitales */
    .info-orbital {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 14px 16px;
        margin-top: 12px;
        color: #f8fafc !important;
        font-size: 15px;
        line-height: 1.6;
    }

    .info-orbital p {
        color: #f8fafc !important;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================
st.markdown("""
<div class="encabezado">
    <h1>⚛️ Simulador del Átomo de Hidrógeno</h1>
    <p class="nota">
        Modelo cuántico, niveles de energía, transiciones electrónicas y espectro de emisión.
        Proyecto Final de Física - Unidad 3.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FUNCIONES MATEMÁTICAS Y FÍSICAS
# ============================================================
def calcular_energia_nivel(n):
    """Calcula la energía de un nivel usando el modelo de Bohr."""
    return -ENERGIA_HIDROGENO_EV / (n ** 2)

def calcular_transicion(n_inicial, n_final):
