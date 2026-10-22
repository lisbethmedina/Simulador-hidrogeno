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
    """Calcula la energía del fotón, longitud de onda y frecuencia."""
    energia_foton = ENERGIA_HIDROGENO_EV * (1 / (n_final ** 2) - 1 / (n_inicial ** 2))
    longitud_onda_nm = 1239.841984 / energia_foton
    frecuencia_hz = (energia_foton * CARGA_ELECTRON_C) / CONSTANTE_PLANCK_JS
    return energia_foton, longitud_onda_nm, frecuencia_hz

def calcular_funcion_onda(orbital, x, y, z):
    """Calcula la función de onda para el orbital seleccionado (en unidades de a₀)."""
    radio = np.sqrt(x**2 + y**2 + z**2)
    
    if orbital == "1s":
        return np.exp(-radio) / np.sqrt(np.pi)
    elif orbital == "2s":
        return (2 - radio) * np.exp(-radio / 2) / (4 * np.sqrt(2 * np.pi))
    elif orbital == "2p (eje z)":
        return z * np.exp(-radio / 2) / (4 * np.sqrt(2 * np.pi))
    elif orbital == "2p (eje x)":
        return x * np.exp(-radio / 2) / (4 * np.sqrt(2 * np.pi))
    else:
        return np.exp(-radio) / np.sqrt(np.pi)

def crear_grafica_orbital(orbital, extension, resolucion, umbral):
    """Construye la visualización tridimensional del orbital mediante isosuperficies."""
    eje = np.linspace(-extension, extension, resolucion)
    X, Y, Z = np.meshgrid(eje, eje, eje, indexing="ij")
    
    funcion = calcular_funcion_onda(orbital, X, Y, Z)
    densidad = funcion ** 2
    
    densidad_maxima = float(np.max(densidad))
    nivel_minimo = max(densidad_maxima * umbral / 100, 1e-10)

    figura = go.Figure(data=go.Isosurface(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=densidad.ravel(),
        isomin=nivel_minimo,
        isomax=densidad_maxima * 0.98,
        surface_count=3,
        caps=dict(x_show=False, y_show=False, z_show=False),
        colorscale=[[0, "#38bdf8"], [0.5, "#6366f1"], [1, "#f0abfc"]],
        opacity=0.55,
        showscale=False,
        hovertemplate="x=%{x:.2f} a₀<br>y=%{y:.2f} a₀<br>z=%{z:.2f} a₀<br>Densidad=%{value:.3e}<extra></extra>"
    ))

    figura.update_layout(
        height=600, margin=dict(l=0, r=0, t=25, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#eaf2ff"),
        scene=dict(
            xaxis_title="x (a₀)", yaxis_title="y (a₀)", zaxis_title="z (a₀)",
            bgcolor="rgba(0,0,0,0)", aspectmode="cube",
            xaxis=dict(gridcolor="#29435f", zerolinecolor="#58708d"),
            yaxis=dict(gridcolor="#29435f", zerolinecolor="#58708d"),
            zaxis=dict(gridcolor="#29435f", zerolinecolor="#58708d")
        )
    )
    return figura

def crear_grafica_niveles(nivel_seleccionado=3, campo_magnetico=0):
    """Dibuja los niveles de energía con efecto Zeeman si hay campo magnético."""
    niveles = np.arange(1, 7)
    mu_B = 5.788e-5  # Magnetón de Bohr en eV/T
    
    figura = go.Figure()

    for n in niveles:
        energia_base = calcular_energia_nivel(int(n))
        
        # Determinar los posibles valores de m_l para este nivel
        l_max = n - 1
        m_l_values = list(range(-l_max, l_max + 1))
        
        if campo_magnetico == 0:
            # Sin campo magnético: nivel normal
            color = "#38bdf8" if n == nivel_seleccionado else "#718096"
            ancho = 4 if n == nivel_seleccionado else 2
            
            figura.add_trace(go.Scatter(
                x=[0.2, 0.8], y=[energia_base, energia_base], mode="lines+markers",
                line=dict(width=ancho, color=color), 
                marker=dict(size=10, color=color),
                name=f"n={n}: {energia_base:.3f} eV",
                hovertemplate=f"Nivel n={n}<br>Energía={energia_base:.4f} eV<extra></extra>",
                showlegend=False
            ))
            
            figura.add_annotation(
                x=0.85, y=energia_base,
                text=f"<b>n={n}</b><br>{energia_base:.2f} eV",
                showarrow=False,
                font=dict(color="#eaf2ff", size=11),
                xanchor="left",
                bgcolor="rgba(30, 41, 59, 0.7)",
                bordercolor="#38bdf8" if n == nivel_seleccionado else "#718096",
                borderwidth=1,
                borderpad=4
            )
        else:
            # CON campo magnético: efecto Zeeman (splitting)
            for i, m_l in enumerate(m_l_values):
                # Calcular el desplazamiento por efecto Zeeman
                delta_E = mu_B * campo_magnetico * m_l
                energia_zeeman = energia_base + delta_E
                
                # Color diferente para cada m_l
                if n == nivel_seleccionado:
                    colores_m_l = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6", "#8b5cf6"]
                    color = colores_m_l[i % len(colores_m_l)]
                else:
                    color = "#718096"
                
                ancho = 3 if n == nivel_seleccionado else 2
                
                figura.add_trace(go.Scatter(
                    x=[0.2 + i*0.05, 0.8 - i*0.05], y=[energia_zeeman, energia_zeeman], 
                    mode="lines+markers",
                    line=dict(width=ancho, color=color), 
                    marker=dict(size=8, color=color),
                    name=f"n={n}, m_l={m_l}",
                    hovertemplate=f"n={n}, m_l={m_l}<br>E={energia_zeeman:.4f} eV<br>ΔE={delta_E:.4e} eV<extra></extra>",
                    showlegend=False
                ))
                
                # Etiqueta solo para el nivel seleccionado
                if n == nivel_seleccionado:
                    figura.add_annotation(
                        x=0.85, y=energia_zeeman,
                        text=f"n={n}<br>m_l={m_l}<br>{energia_zeeman:.3f} eV",
                        showarrow=False,
                        font=dict(color="#eaf2ff", size=9),
                        xanchor="left",
                        bgcolor="rgba(30, 41, 59, 0.8)",
                        bordercolor=color,
                        borderwidth=1,
                        borderpad=3
                    )

    # Línea de ionización
    figura.add_hline(y=0, line_dash="dash", line_color="#ef4444", opacity=0.7, line_width=2)
    figura.add_annotation(
        x=0.5, y=0.15,
        text=" Límite de ionización (E = 0 eV)",
        showarrow=False,
        font=dict(color="#ef4444", size=12),
        xanchor="center"
    )

    # Título dinámico
    if campo_magnetico > 0:
        titulo = f"Niveles de Energía con Efecto Zeeman (B = {campo_magnetico:.1f} T)"
    else:
        titulo = "Niveles de Energía Cuantizados"

    figura.update_layout(
        height=550, 
        margin=dict(l=60, r=150, t=30, b=40),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        font=dict(color="#eaf2ff", family="Arial"),
        title=dict(text=titulo, x=0.5, font=dict(size=16, color="#38bdf8")),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(
            title="Energía (eV)",
            gridcolor="#29435f",
            zerolinecolor="#718096",
            range=[-14.5, 1],
            tickvals=[-13.6, -3.4, -1.51, -0.85, -0.54, -0.38, 0],
            ticktext=["-13.60 (n=1)", "-3.40 (n=2)", "-1.51 (n=3)", 
                     "-0.85 (n=4)", "-0.54 (n=5)", "-0.38 (n=6)", "0 (E libre)"],
            tickfont=dict(size=10, color="#94a3b8")
        )
    )

    return figura

def crear_grafica_espectro():
    """Grafica las líneas de la serie de Balmer en el espectro visible."""
    longitudes_onda, nombres_transiciones, energias_foton, colores = [], [], [], []

    for nivel_inicial in range(3, 9):
        energia, longitud, _ = calcular_transicion(nivel_inicial, 2)
        longitudes_onda.append(longitud)
        nombres_transiciones.append(f"{nivel_inicial} → 2")
        energias_foton.append(energia)

        if longitud < 450: color = "#8b5cf6"
        elif longitud < 495: color = "#3b82f6"
        elif longitud < 570: color = "#22c55e"
        elif longitud < 590: color = "#eab308"
        elif longitud < 620: color = "#f97316"
        elif longitud <= 750: color = "#ef4444"
        else: color = "#94a3b8"
        colores.append(color)

    figura = go.Figure(data=go.Bar(
        x=longitudes_onda, y=[1] * len(longitudes_onda), width=[2.5] * len(longitudes_onda),
        marker_color=colores, customdata=np.array([nombres_transiciones, energias_foton]).T,
        hovertemplate="Transición %{customdata[0]}<br>Longitud de onda=%{x:.2f} nm<br>Energía=%{customdata[1]:.4f} eV<extra></extra>"
    ))

    figura.update_layout(
        height=250, margin=dict(l=15, r=15, t=10, b=35),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eaf2ff"), showlegend=False,
        xaxis=dict(title="Longitud de onda (nm)", range=[350, 700], gridcolor="#29435f"),
        yaxis=dict(visible=False, range=[0, 1.5])
    )
    return figura

# ============================================================
# INTERFAZ DE USUARIO (PESTAÑAS)
# ============================================================
pestanas = st.tabs([
    "1. Visualización de Orbitales",
    "2. Niveles de Energía",
    "3. Transiciones y Espectro",
    "4. Fundamento Teórico"
])

# --- PESTAÑA 1: ORBITALES ---
with pestanas[0]:
    st.subheader("Visualizador de Orbitales Atómicos")
    col_opc, col_graf = st.columns([1, 2.2], gap="large")

    with col_opc:
        orbital = st.selectbox("Seleccione un orbital", ["1s", "2s", "2p (eje z)", "2p (eje x)"])
        extension = st.slider("Extensión del espacio (a₀)", 4.0, 14.0, 8.0, 1.0)
        resolucion = st.slider("Resolución de la malla", 18, 42, 28, 2)
        umbral = st.slider("Umbral de densidad (%)", 2, 35, 10, 1)

        st.markdown("**Interpretación física:**")
        st.write("La isosuperficie representa las regiones del espacio donde la densidad de probabilidad $|\\psi|^2$ es significativa. No representa una trayectoria clásica del electrón.")

        if orbital == "1s":
            st.info("El orbital 1s presenta simetría esférica y no posee nodos.")
        elif orbital == "2s":
            st.info("El orbital 2s posee un nodo radial esférico en $r = 2a_0$.")
        else:
            st.info("Los orbitales 2p presentan dos lóbulos separados por un plano nodal que pasa por el núcleo.")

    with col_graf:
        with st.spinner("Calculando distribución de probabilidad..."):
            fig_orb = crear_grafica_orbital(orbital, extension, resolucion, umbral)
        st.plotly_chart(fig_orb, use_container_width=True)

# --- PESTAÑA 2: NIVELES DE ENERGÍA ---
with pestanas[1]:
    st.subheader("Cuantización de la Energía y Efecto Zeeman")
    col_graf, col_dat = st.columns([1.2, 1])

    with col_graf:
        nivel = st.slider("Seleccione el nivel de energía principal (n)", 1, 6, 3)
        
        st.markdown("**Campo Magnético Externo (Efecto Zeeman)**")
        campo_B = st.slider("Intensidad del campo magnético B (Tesla)", 0.0, 10.0, 0.0, 0.5)
        
        if campo_B > 0:
            st.info(f"🔬 **Efecto Zeeman activado:** B = {campo_B:.1f} T. Los niveles se dividen según el número cuántico magnético m_l.")
        
        st.plotly_chart(crear_grafica_niveles(nivel, campo_B), use_container_width=True)

    with col_dat:
        energia = calcular_energia_nivel(nivel)
        energia_fund = calcular_energia_nivel(1)

        st.metric(f"Energía para n = {nivel}", f"{energia:.5f} eV")
        st.metric("Diferencia con el estado fundamental", f"{energia - energia_fund:.5f} eV")

        st.markdown("**Ecuación de Bohr:**")
        st.latex(r"E_n = -\frac{13.6057 \text{ eV}}{n^2}")
        
        if campo_B > 0:
            st.markdown("**Desplazamiento Zeeman:**")
            st.latex(r"\Delta E = \mu_B \cdot B \cdot m_l")
            st.write("Donde μ_B = 5.788×10⁻⁵ eV/T es el magnetón de Bohr.")
        
        st.write("El signo negativo indica que el electrón se encuentra en un estado ligado. Cuando $n \\to \\infty$, $E \\to 0$, lo que corresponde al límite de ionización del átomo.")

    # Sección explicativa del efecto Zeeman
    if campo_B > 0:
        st.divider()
        st.subheader("📡 Efecto Zeeman: Aplicaciones en Telecomunicaciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ¿Qué es el efecto Zeeman?")
            st.write("""
            Cuando un átomo se somete a un campo magnético externo, sus niveles de energía 
            se **dividen** (splitting) en múltiples subniveles. Esto ocurre porque el momento 
            magnético orbital del electrón interactúa con el campo magnético aplicado.
            
            La separación energética es proporcional a:
            - La intensidad del campo magnético **B**
            - El número cuántico magnético **m_l**
            - El magnetón de Bohr **μ_B**
            """)
        
        with col2:
            st.markdown("### Aplicaciones en Telecomunicaciones")
            st.write("""
            1. **Fibra Óptica:** El efecto Zeeman se utiliza en aisladores ópticos y 
               moduladores que controlan la polarización de la luz en redes de fibra óptica.
            
            2. **Espectroscopía:** Permite identificar elementos químicos en estrellas y 
               plasmas mediante el análisis de líneas espectrales divididas.
            
            3. **Resonancia Magnética:** Técnica basada en transiciones entre niveles 
               divididos por campo magnético, usada en telecomunicaciones cuánticas.
            
            4. **Antenas y Propagación:** Los campos magnéticos afectan la propagación 
               de ondas electromagnéticas en el medio interestelar y la ionosfera.
            """)

# --- PESTAÑA 3: TRANSICIONES Y ESPECTRO ---
with pestanas[2]:
    st.subheader("Transiciones Electrónicas y Espectro de Emisión")
    col_calc, col_esp = st.columns([1, 1.3])

    with col_calc:
        n_ini = st.selectbox("Nivel inicial ($n_i$)", [2, 3, 4, 5, 6, 7, 8], index=1)
        n_fin = st.selectbox("Nivel final ($n_f$)", [1, 2, 3, 4, 5, 6, 7], index=1)

        if n_ini <= n_fin:
            st.warning("Para calcular una emisión, el nivel inicial debe ser mayor que el nivel final ($n_i > n_f$).")
        else:
            E_foton, lambda_nm, freq_hz = calcular_transicion(n_ini, n_fin)

            st.metric("Energía del fotón emitido", f"{E_foton:.5f} eV")
            st.metric("Longitud de onda", f"{lambda_nm:.3f} nm")
            st.metric("Frecuencia", f"{freq_hz:.4e} Hz")

            if 380 <= lambda_nm <= 750:
                st.success("La radiación emitida se encuentra en el espectro visible.")
            elif lambda_nm < 380:
                st.info("La radiación emitida corresponde al espectro ultravioleta.")
            else:
                st.info("La radiación emitida corresponde al espectro infrarrojo.")

            st.latex(r"\Delta E = E_i - E_f = hf = \frac{hc}{\lambda}")

    with col_esp:
        st.markdown("**Serie de Balmer: transiciones hacia el nivel $n = 2$**")
        st.plotly_chart(crear_grafica_espectro(), use_container_width=True)

# --- PESTAÑA 4: FUNDAMENTO TEÓRICO ---
with pestanas[3]:
    st.subheader("Fundamento Físico y Validación del Modelo")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Modelo Atómico de Bohr (1913)")
        st.write("Bohr postuló que el electrón se mueve en órbitas circulares cuantizadas. La energía de estos niveles discretos está dada por:")
        st.latex(r"E_n = -\frac{13.6 \text{ eV}}{n^2}")
        st.write("Este modelo explica perfectamente las líneas espectrales del hidrógeno, pero no describe la distribución espacial real del electrón.")

        st.markdown("### 2. Ecuación de Schrödinger (1926)")
        st.latex(r"\hat{H}\psi = E\psi")
        st.write("La mecánica cuántica ondulatoria reemplaza las órbitas definidas de Bohr por **orbitales** (funciones de onda $\psi$), describiendo la probabilidad de encontrar al electrón en el espacio.")

    with col2:
        st.markdown("### 3. Densidad de Probabilidad")
        st.latex(r"\rho(x,y,z) = |\psi(x,y,z)|^2")
        st.write("Representa la 'nube electrónica'. Las superficies 3D que visualizas en la Pestaña 1 son isosuperficies de esta densidad de probabilidad.")

        st.markdown("### 4. Validación: Transición $3 \\to 2$")
        E_val, lam_val, _ = calcular_transicion(3, 2)
        st.write(f"Energía calculada: **{E_val:.4f} eV**")
        st.write(f"Longitud de onda: **{lam_val:.2f} nm**")
        st.write("Este valor coincide con la línea espectral $H\\alpha$ (656.3 nm) de la Serie de Balmer, validando la cuantización de la energía propuesta por Bohr.")

    st.divider()
    st.markdown("### Alcance y Limitaciones")
    st.write(
        "El presente simulador integra el **modelo de Bohr** (para calcular niveles de energía y espectro de emisión) y el **modelo cuántico de Schrödinger** (para visualizar la forma de los orbitales). "
        "Como modelo educativo, no contempla efectos de estructura fina, espín del electrón, ni la interacción con campos electromagnéticos externos."
    )
