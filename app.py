import streamlit as st
import pandas as pd

# ============================================
# 1. TABLA IF (BASE DE DATOS)
# ============================================

data = [
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

df_if = pd.DataFrame(data, columns=["Experiencia","Peso","Desnivel","IF_min","IF_max"])

# ============================================
# 2. INTERFAZ STREAMLIT
# ============================================

st.title("Calculadora de Pacing 70.3 con % de Grasa")
st.subheader("Clasificación automática del atleta según composición corporal")

ftp = st.number_input("FTP (W)", min_value=100, max_value=500, value=250)

experiencia = st.selectbox("Experiencia", ["Baja","Media","Alta"])
desnivel = st.selectbox("Desnivel del circuito", ["Bajo","Medio","Alto"])

grasa = st.number_input("Porcentaje de grasa corporal (%)", min_value=3.0, max_value=40.0, value=15.0)

# ============================================
# 3. CLASIFICACIÓN AUTOMÁTICA POR % GRASA
# ============================================

if grasa < 10:
    categoria_peso = "Ligero"
elif grasa <= 15:
    categoria_peso = "Medio"
else:
    categoria_peso = "Pesado"

st.write(f"**Categoría asignada automáticamente:** {categoria_peso}")

# ============================================
# 4. CÁLCULO DEL PACING
# ============================================

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
    pot_subidas = ftp * (if_rec + 0.08)
    pot_llano   = ftp * (if_rec - 0.02)
    pot_bajadas = ftp * (if_rec - 0.10)

    st.header("Resultados del Pacing")

    st.write(f"**IF mínimo:** {if_min:.2f}")
    st.write(f"**IF máximo:** {if_max:.2f}")
    st.write(f"**IF recomendado:** {if_rec:.2f}")
    st.write(f"**NP objetivo:** {np_obj:.0f} W")

    st.subheader("Pacing por terreno")
    st.write(f"**Subidas:** {pot_subidas:.0f} W")
    st.write(f"**Llano:** {pot_llano:.0f} W")
    st.write(f"**Bajadas:** {pot_bajadas:.0f} W")

    # ============================================
    # 5. DESCARGA DE EXCEL
    # ============================================

    df_calc = pd.DataFrame({
        "Variable": ["FTP","Experiencia","% Grasa","Categoría Peso","Desnivel","IF_min","IF_max","IF_recomendado","NP","Subidas","Llano","Bajadas"],
        "Valor": [ftp,experiencia,grasa,categoria_peso,desnivel,if_min,if_max,if_rec,np_obj,pot_subidas,pot_llano,pot_bajadas]
    })

    excel_file = "pacing_70_3.xlsx"
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
# 6. BOTÓN DE DONACIÓN POR BIZUM (SIN QR)
# ============================================

st.markdown("---")
st.markdown("### ☕ ¿Te ha gustado la herramienta? Invítame a un café por Bizum")

st.markdown("""
<div style="font-size:22px; text-align:center; padding-top:10px;">
    📱 <strong>Bizum: 600 254 690</strong><br>
    ¡Gracias por apoyar este proyecto!
</div>
""", unsafe_allow_html=True)

# ============================================
# 7. AVISO DE PROPIEDAD
# ============================================

st.markdown("---")
st.markdown("""
<div style="text-align:center; font-size:16px; color:gray; padding-top:10px;">
    © Esta herramienta es propiedad de <strong>Pablo Iglesias Navarrete</strong>,<br>
    Entrenador Nacional de Triatlón y Natación.
</div>
""", unsafe_allow_html=True)

# ============================================
# 8. FOOTER FIJO CON ENLACE A INSTAGRAM
# ============================================

st.markdown("""
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

<div class="footer">
    © Herramienta creada por <strong>Pablo Iglesias Navarrete</strong> —  
    Entrenador Nacional de Triatlón y Natación —  
    Sígueme en Instagram: 
    <a href="https://www.instagram.com/pabloiglesiasnavarrete/" target="_blank">
        @pabloiglesiasnavarrete
    </a>
</div>
""", unsafe_allow_html=True)
