import streamlit as st
import pandas as pd

# ============================
# CONFIGURACIÓN DE PÁGINA
# ============================

st.set_page_config(
    page_title="Calculadora 3K → 5K — Pablo Iglesias Navarrete",
    layout="centered"
)

# ============================
# ESTILOS PREMIUM
# ============================

st.markdown("""
<style>

body {
    background-color: #f7f7f7;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #222;
}

.sub-title {
    font-size: 22px;
    text-align: center;
    color: #444;
    margin-top: -10px;
}

.hero-box {
    background: linear-gradient(135deg, #0072ff, #00c6ff);
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

.result-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 18px;
}

.result-title {
    font-size: 20px;
    font-weight: 700;
    color: #0072ff;
}

.table-container {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ============================
# HERO HEADER
# ============================

st.markdown("""
<div class="hero-box">
    <div class="big-title">Calculadora de Ritmos 3K → 5K</div>
    <div class="sub-title">Basada en datos reales de zonas fisiológicas</div>
</div>
""", unsafe_allow_html=True)

# ============================
# INPUT DEL TIEMPO 3K
# ============================

st.markdown("### 🕒 Introduce tu tiempo en 3000 m")

col1, col2 = st.columns(2)
with col1:
    min_3k = st.number_input("Minutos", min_value=5, max_value=30, value=12)
with col2:
    seg_3k = st.number_input("Segundos", min_value=0, max_value=59, value=0)

tiempo_3k = min_3k * 60 + seg_3k

# ============================
# FACTOR REAL DE TU TABLA
# ============================

factor_3k_to_5k = 1410 / 846.8
vo2_5k = tiempo_3k * factor_3k_to_5k

# ============================
# FACTORES DE ZONAS
# ============================

zonas = {
    "AEL": 1.428,
    "AELMED": 1.333,
    "AELINT": 1.250,
    "UA": 1.177,
    "SUB1": 1.111,
    "SUB2": 1.075,
    "UAN": 1.053,
    "VO2": 1.000
}

# ============================
# FACTORES POR DISTANCIA
# ============================

factores_distancia = {
    500: 0.0928,
    1000: 0.1950,
    1500: 0.2985,
    3000: 0.6005,
    5000: 1.0000
}

# ============================
# FORMATO
# ============================

def formato(t):
    m = int(t // 60)
    s = int(t % 60)
    return f"{m}:{s:02d}"

# ============================
# RESULTADOS PRINCIPALES
# ============================

st.markdown("## 🔥 Resultados principales")

st.markdown(f"""
<div class="result-card">
    <div class="result-title">VO₂ estimado para 5000 m</div>
    <div style="font-size:28px; font-weight:700;">{formato(vo2_5k)}</div>
</div>

<div class="result-card">
    <div class="result-title">Ritmo VO₂ estimado</div>
    <div style="font-size:28px; font-weight:700;">{formato(vo2_5k/5)} / km</div>
</div>
""", unsafe_allow_html=True)

# ============================
# TABLA COMPLETA
# ============================

st.markdown("## 📊 Tabla completa de ritmos por distancia y zona")

filas = []

for zona, factor_zona in zonas.items():
    tiempo_5k_zona = vo2_5k * factor_zona

    for dist, factor_dist in factores_distancia.items():
        tiempo_dist = tiempo_5k_zona * factor_dist
        ritmo_km = tiempo_dist / (dist/1000)

        filas.append([
            zona,
            dist,
            formato(tiempo_dist),
            formato(ritmo_km)
        ])

df = pd.DataFrame(filas, columns=["Zona", "Distancia (m)", "Tiempo", "Ritmo/km"])

st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================
# FOOTER
# ============================

st.markdown("""
---
### ☕ ¿Te ayuda esta herramienta?
Puedes invitarme a un café o colaborar por Bizum:  
**600 254 690**

**Pablo Iglesias Navarrete**  
Entrenador Nacional de Triatlón y Natación
""")
