import streamlit as st

# Datos para cada línea de crédito
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Créditos libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazo_min": 12,
        "plazo_max": 60,
        "tasa_mensual": 1.9715,  # Tasa mensual en %
        "tasa_anual_efectiva": 26.4,  # Tasa E.A. en %
        "aval_porcentaje": 0.10,  # 10% del capital prestado
    },
    "LoansiMicroFlex": {
        "descripcion": "Crédito rotativo para competir con el crédito gota a gota, orientado a personas en sectores informales.",
        "monto_min": 50000,
        "monto_max": 300000,
        "plazo_min": 4,
        "plazo_max": 8,
        "tasa_mensual": 2.0718,  # Tasa mensual en %
        "tasa_anual_efectiva": 27.9,  # Tasa E.A. en %
        "aval_porcentaje": 0.12,  # 12% del capital prestado
    }
}

# Costos asociados al crédito (no visibles en la interfaz principal)
COSTOS_ASOCIADOS = {
    "Pagaré Digital": 2800,
    "Carta de Instrucción": 2800,
    "Custodia TVE": 5600,
    "Consulta Datacrédito": 11000
}

# Sumar todos los costos asociados
total_costos_asociados = sum(COSTOS_ASOCIADOS.values())

# Título de la aplicación y estilo
st.markdown("<h1 style='color: #4A90E2; text-align: center; font-weight: bold;'>Simulador de Crédito Loansi</h1>", unsafe_allow_html=True)

# Selección de línea de crédito
tipo_credito = st.selectbox("Selecciona la Línea de Crédito", options=LINEAS_DE_CREDITO.keys())
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Mostrar descripción del crédito
st.write(f"**Descripción**: {detalles['descripcion']}")

# Selección del monto con formato numérico
monto = st.number_input(
    "Monto Solicitado (COP):",
    min_value=detalles["monto_min"],
    max_value=detalles["monto_max"],
    step=50000,
    format="%d"
)

# Cálculo del aval
aval = monto * detalles["aval_porcentaje"]

# Cálculo del total a financiar (monto + aval + costos asociados)
total_financiar = monto + aval + total_costos_asociados

# Selección de plazo
if tipo_credito == "LoansiFlex":
    plazo = st.slider("Plazo en Meses:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=12)
    frecuencia_pago = "Mensual"
else:
    plazo = st.slider("Plazo en Semanas:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=1)
    frecuencia_pago = st.selectbox("Frecuencia de Pago", ["Semanal", "Quincenal"])

# Cálculo de la cuota
if tipo_credito == "LoansiFlex":
    # Calcular la cuota mensual usando la fórmula de amortización
    cuota = (total_financiar * (detalles["tasa_mensual"] / 100)) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
else:
    # Conversión de tasa mensual a semanal o quincenal
    tasa_semanal = (1 + detalles["tasa_mensual"] / 100) ** (1/4) - 1 if frecuencia_pago == "Semanal" else (1 + detalles["tasa_mensual"] / 100) ** (1/2) - 1
    cuota = (total_financiar * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo)

# Mostrar resultados
st.markdown("### Resultado de Simulación")
st.write(f"**Monto Solicitado**: COP {monto:,.0f}")
st.write(f"**Tasa de Interés Mensual**: {detalles['tasa_mensual']}%")
st.write(f"**Interés Efectivo Anual (E.A.)**: {detalles['tasa_anual_efectiva']}%")
st.write(f"**Frecuencia de Pago**: {frecuencia_pago}")
st.write(f"**Cuota Estimada**: COP {cuota:,.0f}")

# Detalle adicional en sección desplegable
with st.expander("Ver Detalles del Crédito"):
    total_interes = cuota * plazo - total_financiar
    total_pagar = cuota * plazo
    st.write(f"**Número de Cuotas**: {plazo}")
    st.write(f"**Costo del Aval y Otros**: COP {total_costos_asociados + aval:,.0f}")
    st.write(f"**Total del Interés a Pagar**: COP {total_interes:,.0f}")
    st.write(f"**Total a Pagar**: COP {total_pagar:,.0f}")

# Botón para solicitar el crédito
st.write("---")
st.markdown("<h3 style='text-align: center;'>¿Interesado en solicitar este crédito?</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Para más información, comuníquese con nosotros por WhatsApp:</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><a href='https://wa.me/XXXXXXXXXXX' target='_blank' style='color: #4A90E2; font-weight: bold;'>Hacer solicitud vía WhatsApp</a></p>", unsafe_allow_html=True)
