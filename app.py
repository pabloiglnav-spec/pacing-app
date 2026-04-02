import streamlit as st
import pandas as pd

# ============================================
# 0. CONFIGURACIÓN INICIAL
# ============================================

st.set_page_config(page_title="Pacing Triatlón — Pablo Iglesias Navarrete", layout="centered")

# ============================================
# 1. TÍTULO + LOGO + BIZUM
# ============================================

st.title("Calculadora de Pacing Triatlón (70.3 / Ironman Full)")

# LOGO CENTRADO BONITO
st.markdown("""
<div style='text-align:center; margin-top:20px; margin-bottom:10px;'>
    <img src='logo.png' width='220' style='border-radius:10px;'>
</div>
""", unsafe_allow_html=True)

# BIZUM + CAFÉ
st.markdown("""
<div style='text-align:center; font-size:20px; margin-top:10px;'>
    ☕ Si esta herramienta te ayuda, puedes invitarme a un café o colaborar por Bizum:<br>
    <strong>600 254 690</strong>
</div>
""", unsafe_allow_html=True)

# ============================================
# 2. TABLAS IF PARA 70.3 Y IRONMAN FULL
# ============================================

data_703 = [
    ("Baja","Ligero","Bajo",0.74,0.78),
    ("Baja","Ligero","Medio",0.72,0.76),
    ("Baja","Ligero","Alto",0.70,0.74),
    ("Baja","Medio","Bajo",0.72,0.76),
    ("Baja","Medio","Medio",0.70,0.74),
    ("Baja","Medio","Alto",0.68,0.72),
    ("Baja","Pesado","Bajo",0.70,0.74),
    ("Baja","Pesado","Medio",0.68,0.72),
    ("Baja","Pesado","Alto",0.66,0.70),

    ("Media","Ligero","Bajo",0.78,0.82),
    ("Media","Ligero","Medio",0.76,0.80),
    ("Media","Ligero","Alto",0.74,0.78),
    ("Media","Medio","Bajo",0.76,0.80),
    ("Media","Medio","Medio",0.74,0.78),
    ("Media","Medio","Alto",0.72,0.76),
    ("Media","Pesado","Bajo",0.74,0.78),
    ("Media","Pesado","Medio",0.72,0.76),
    ("Media","Pesado","Alto",0.70,0.74),

    ("Alta","Ligero","Bajo",0.82,0.85),
    ("Alta","Ligero","Medio",0.80,0.83),
    ("Alta","Ligero","Alto",0.78,0.82),
    ("Alta","Medio","Bajo",0.80,0.83),
    ("Alta","Medio","Medio",0.78,0.82),
    ("Alta","Medio","Alto",0.76,0.80),
    ("Alta","Pesado","Bajo",0.78,0.82),
    ("Alta","Pesado","Medio",0.76,0.80),
    ("Alta","Pesado","Alto",0.74,0.78),
]

data_full = [
    ("Baja","Ligero","Bajo",0.60,0.65),
    ("Baja","Ligero","Medio",0.59,0.64),
    ("Baja","Ligero","Alto",0.58,0.63),
    ("Baja","Medio","Bajo",0.59,0.64),
    ("Baja","Medio","Medio",0.58,0.63),
    ("Baja","Medio","Alto",0.57,0.62),
    ("Baja","Pesado","Bajo",0.58,0.63),
    ("Baja","Pesado","Medio",0.57,0.62),
    ("Baja","Pesado","Alto",0.56,0.61),

    ("Media","Ligero","Bajo",0.65,0.69),
    ("Media","Ligero","Medio",0.64,0.68),
    ("Media","Ligero","Alto",0.63,0.67),
    ("Media","Medio","Bajo",0.64,0.68),
    ("Media","Medio","Medio",0.63,0.67),
    ("Media","Medio","Alto",0.62,0.66),
    ("Media","Pesado","Bajo",0.63,0.67),
    ("Media","Pesado","Medio",0.62,0.66),
    ("Media","Pesado","Alto",0.61,0.65),

    ("Alta","Ligero","Bajo",0.69,0.72),
    ("Alta","Ligero","Medio",0.68,0.71),
    ("Alta","Ligero","Alto",0.67,0.70),
    ("Alta","Medio","Bajo",0.68,0.71),
    ("Alta","Medio","Medio",0.67,0.70),
    ("Alta","Medio","Alto",0.66,0.69),
    ("Alta","Pesado","Bajo",0.67,0.70),
    ("Alta","Pesado","Medio",0.66,0.69),
    ("Alta","Pesado","Alto",0.65,0.68),
]

df_703 = pd.DataFrame(data_703, columns=["Experiencia","Peso","Desnivel","IF_min","IF_max"])
df_full = pd.DataFrame(data_full, columns=["Experiencia","Peso","Desnivel","IF_min","IF_max"])

# ============================================
# 3. INTERFAZ DE USUARIO
# ============================================

distancia = st.selectbox("Selecciona la distancia", ["70.3", "Ironman Full"])

ftp = st.number_input("FTP (W)", min_value=100, max_value=500, value=250)
peso = st.number_input("Peso corporal (kg)", min_value=40.0, max_value=150.0, value=70.0)

tiene_grasa = st.radio("¿Tienes el dato de % de grasa?", ["No", "Sí"])

if tiene_grasa == "Sí":
    grasa = st.number_input("Porcentaje de grasa corporal (%)", min_value=3.0, max_value=40.0, value=15.0)
    peso_magro = peso * (1 - grasa/100)
else:
    grasa = None
    peso_magro = None

experiencia = st.selectbox("Experiencia", ["Baja","Media","Alta"])
desnivel = st.selectbox("Desnivel del circuito", ["Bajo","Medio","Alto"])

# ============================================
# 4. CATEGORÍA DE PESO
# ============================================

if grasa is None:
    categoria_peso = "Medio"
else:
    if grasa < 10:
        categoria_peso = "Ligero"
    elif grasa <= 15:
        categoria_peso = "Medio"
    else:
        categoria_peso = "Pesado"

st.write(f"**Categoría asignada:** {categoria_peso}")

# ============================================
# 5. SELECCIÓN DE TABLA IF
# ============================================

df_if = df_703 if distancia == "70.3" else df_full

fila = df