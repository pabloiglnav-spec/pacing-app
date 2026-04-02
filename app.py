import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pacing Triatlón — Pablo Iglesias Navarrete", layout="centered")

# ============================================
# 1. HERO HEADER (LOGO + TÍTULO + AUTOR + BIZUM)
# ============================================

hero_html = """
<div style='text-align:center; margin-top:-20px;'>
    <img src='logo.png' width='200' style='margin-bottom:10px;'>
    <h1 style='margin-bottom:0;'>Calculadora de Pacing Triatlón</h1>
    <h3 style='margin-top:0; color:#555;'>70.3 / Ironman Full</h3>

    <p style='font-size:18px; margin-top:10px;'>
        Herramienta creada por <strong>Pablo Iglesias Navarrete</strong><br>
        Entrenador Nacional de Triatlón y Natación
    </p>

    <p style='font-size:18px; margin-top:15px;'>
        ☕ Si esta herramienta te ayuda, puedes invitarme a un café o colaborar por Bizum:<br>
        <strong>600 254 690</strong>
    </p>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

# ============================================
# 2. TABLAS IF
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
# 3. INTERFAZ
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
    categoria_peso = "Ligero" if grasa < 10 else "Medio" if grasa <= 15 else "Pesado"

st.write(f"**Categoría asignada:** {categoria_peso}")

# ============================================
# 5. SELECCIÓN DE TABLA IF
# ============================================

df_if = df_703 if distancia == "70.3" else df_full

fila = df_if[
    (df_if["Experiencia"] == experiencia) &
    (df_if["Peso"] == categoria_peso) &
    (df_if["Desnivel"] == desnivel)
]

if fila.empty:
    st.error("No se encontró combinación en la tabla IF.")
else:
    if_min = fila["IF_min"].iloc[0]
    if_max = fila["IF_max"].iloc[0]
    if_rec = (if_min + if_max) / 2

    np_obj = ftp * if_rec

    if distancia == "70.3":
        pot_subidas = ftp * (if_rec + 0.08)
        pot_llano   = ftp * (if_rec - 0.02)
        pot_bajadas = ftp * (if_rec - 0.10)
    else:
        pot_subidas = ftp * (if_rec + 0.05)
        pot_llano   = ftp * (if_rec - 0.01)
        pot_bajadas = ftp * (if_rec - 0.08)

    st.header("Resultados del Pacing")
    st.write(f"**IF recomendado:** {if_rec:.2f}")
    st.write(f"**NP objetivo:** {np_obj:.0f} W")

    st.subheader("Potencia relativa (W/kg)")
    st.write(f"**FTP relativo:** {ftp/peso:.2f} W/kg")
    st.write(f"**NP relativo:** {np_obj/peso:.2f} W/kg")

    if peso_magro:
        st.write(f"**FTP relativo magro:** {ftp/peso_magro:.2f} W/kg")
        st.write(f"**NP relativo magro:** {np_obj/peso_magro:.2f} W/kg")

    st.subheader("Pacing por terreno")
    st.write(f"**Subidas:** {pot_subidas:.0f} W ({pot_subidas/peso:.2f} W/kg)")
    st.write(f"**Llano:** {pot_llano:.0f} W ({pot_llano/peso:.2f} W/kg)")
    st.write(f"**Bajadas:** {pot_bajadas:.0f} W ({pot_bajadas/peso:.2f} W/kg)")

    # ============================================
    # 6. EXCEL
    # ============================================

    df_calc = pd.DataFrame({
        "Variable": [
            "Distancia","FTP","Peso","% Grasa","Peso magro","Experiencia",
            "Categoría Peso","Desnivel","IF_min","IF_max","IF_recomendado",
            "NP","Subidas","Llano","Bajadas"
        ],
        "Valor": [
            distancia, ftp, peso, grasa, peso_magro, experiencia,
            categoria_peso, desnivel, if_min, if_max, if_rec,
            np_obj, pot_subidas, pot_llano, pot_bajadas
        ]
    })

    excel_file = "pacing_triatlon.xlsx"
    with pd.ExcelWriter(excel_file) as writer:
        df_if.to_excel(writer, sheet_name="Tabla_IF", index=False)
        df_calc.to_excel(writer, sheet_name="Pacing", index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            label="Descargar Excel",
            data=f,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ============================================
# 7. SECCIÓN "ENTRENA CONMIGO"
# ============================================

st.markdown("---")
st.markdown("## 💪 Entrena conmigo")
st.markdown(
    "- 🏊 Natación técnica y eficiente\n"
    "- 🚴 Pacing y control del esfuerzo en ciclismo\n"
    "- 🏃 Carrera a pie con control de carga\n"
    "- 🧠 Planificación científica y seguimiento semanal\n"
    "- 📊 Análisis de datos (W/kg, NP, TSS, IF, HRV…)\n"
    "- 🌿 Adaptación total a tu vida, trabajo y familia"
)

st.markdown("### ¿Quieres que sea tu entrenador?")

st.markdown(
    "<div style='text-align:center; margin-top:20px;'>"
    "<a href='https://wa.me/34600254690' target='_blank' style='"
    "background-color:#00c853; color:white; padding:12px 25px; "
    "border-radius:8px; text-decoration:none; font-size:20px; font-weight:bold;'>"
    "🚀 Empezar a entrenar hoy</a></div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================
# 8. FOOTER
# ============================================

footer_css = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #111111;
    color: white;
    text-align: center;
    padding: 10px 0;
    font-size: 15px;
    opacity: 0.95;
}
.footer a {
    color: #4EA8FF;
    text-decoration: none;
    font-weight: bold;
}
.footer a:hover {
    color: #82C7FF;
}
</style>
"""

footer_html = """
<div class='footer'>
    <img src='logo.png' width='70'><br>
    © Herramienta creada por <strong>Pablo Iglesias Navarrete</strong> — 
    Entrenador Nacional de Triatlón y Natación — Instagram: 
    <a href='https://www.instagram.com/pabloiglesiasnavarrete/' target='_blank'>
        @pabloiglesiasnavarrete
    </a>
</div>
"""

st.markdown(footer_css, unsafe_allow_html=True)
st.markdown(footer_html, unsafe_allow_html=True)
