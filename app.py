import streamlit as st
import json
import os

st.set_page_config(page_title="Presupuestos Coches de Bodas Aranjuez", page_icon="💒", layout="centered")

# Cargar configuración de precios desde JSON
CONFIG_PATH = "config_precios.json"

if not os.path.exists(CONFIG_PATH):
    st.error("❌ No se encontró el archivo 'config_precios.json'. Añádelo localmente (está ignorado en .gitignore).")
    st.stop()

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    precios = json.load(f)

st.title("💍 Generador de Presupuestos - Coches de Bodas Aranjuez")
st.write("Completa la información para calcular el presupuesto del coche de boda:")

# Tipo de boda
tipo_boda = st.radio("Tipo de boda:", ["Boda completa", "Boda civil"])

# Coche
tipo_coche = st.selectbox("Coche:", ["Rolls Royce", "Mercedes", "Bentley"])

# Adornos
adornos = st.checkbox("Incluir adornos (+20€)", value=True)

# Recogida del novio (solo boda completa)
recogida_novio = False
if tipo_boda == "Boda completa":
    recogida_novio = st.checkbox("Recoger también al novio (+20€)", value=False)

# Distancia
distancia = st.number_input("Distancia total (km):", min_value=0.0, step=1.0, value=10.0)

# Duración (solo bodas civiles)
duracion_horas = 1.0
if tipo_boda == "Boda civil":
    duracion_horas = st.number_input("Duración total (horas):", min_value=1.0, step=0.5, value=1.0)

# --- Cálculo del precio ---
total = 0

if tipo_boda == "Boda completa":
    base = precios["boda_completa"][tipo_coche.lower().replace(" ", "_")]
    total += base
    if adornos:
        total += precios["boda_completa"]["adornos"]
    if recogida_novio:
        total += precios["boda_completa"]["recogida_novio"]
else:
    base = precios["boda_civil"][tipo_coche.lower().replace(" ", "_")]
    total += base
    if adornos:
        total += precios["boda_civil"]["adornos"]
    if duracion_horas > 1:
        extra_media_horas = (duracion_horas - 1) / 0.5
        total += precios["boda_civil"]["hora_extra_media"] * extra_media_horas

# Suplemento por distancia
if distancia > precios["suplemento_distancia"]["limite_km"]:
    extra_km = distancia - precios["suplemento_distancia"]["limite_km"]
    total += extra_km * precios["suplemento_distancia"]["precio_km_extra"]

# --- Mostrar resultado ---
st.markdown("### 💰 Presupuesto estimado:")
st.metric(label="Precio total", value=f"{total:.2f} €")

with st.expander("Ver desglose detallado"):
    st.write(f"Tipo de boda: {tipo_boda}")
    st.write(f"Coche: {tipo_coche}")
    st.write(f"Adornos: {'Sí' if adornos else 'No'}")
    if tipo_boda == "Boda completa":
        st.write(f"Recogida del novio: {'Sí' if recogida_novio else 'No'}")
    if tipo_boda == "Boda civil":
        st.write(f"Duración: {duracion_horas:.1f} horas")
    st.write(f"Distancia: {distancia} km")
    st.write(f"**Total: {total:.2f} €**")
