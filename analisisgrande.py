import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(layout="wide")
st.title("Dashboard de Salud y Estilo de Vida")

# --- Cargar los datos desde el mismo directorio ---
df = pd.read_csv("CopiaAnalisisDatosGrande.csv")


# Renombrar columnas para facilidad si es necesario
df.columns = df.columns.str.strip()  # Elimina espacios extra

# --- Filtros iniciales (sin aplicar aún) ---
gender_map = {1: "Hombre", 2: "Mujer"}
smokes_map = {0: "No fuma", 1: "Fuma"}

df['Gender'] = df['Gender'].map(gender_map)
df['smokes'] = df['smokes'].map(smokes_map)

# --- Layout en dos columnas ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("¿Fuman?")
    counts = df['smokes'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(
        counts,
        labels=counts.index,
        colors=['orange', 'saddlebrown'],  # No fuma = naranja, Fuma = café
        autopct='%1.1f%%',
        startangle=90
    )
    ax1.axis('equal')
    st.pyplot(fig1)

with col2:
    st.subheader("Distribución por Género")
    counts = df['Gender'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(
        counts,
        labels=counts.index,
        colors=['blue', 'pink'],  # Hombre = azul, Mujer = rosa
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.axis('equal')
    st.pyplot(fig2)

# --- Filtros Interactivos ---
st.markdown("---")
st.subheader("Filtros")

colf1, colf2 = st.columns(2)

with colf1:
    selected_gender = st.radio("Selecciona el género:", options=["Todos", "Hombre", "Mujer"])

with colf2:
    selected_smoke = st.radio("Selecciona hábito de fumar:", options=["Todos", "Fuma", "No fuma"])

# --- Aplicar filtros al DataFrame ---
filtered_df = df.copy()

if selected_gender != "Todos":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_smoke != "Todos":
    filtered_df = filtered_df[filtered_df['smokes'] == selected_smoke]

# --- Gráfico de barras horizontal ---
st.markdown("---")
st.subheader("Indicadores de Bienestar")

# Asegúrate de que las columnas existen
variables = ['anxiety_frequency', 'depression_frequency', 'transport_time']
filtered_df = filtered_df.dropna(subset=variables)

promedios = filtered_df[variables].mean().sort_values()

fig3, ax3 = plt.subplots()
sns.barplot(x=promedios.values, y=promedios.index, palette="coolwarm", ax=ax3)
ax3.set_xlabel("Promedio")
ax3.set_ylabel("Variable")
st.pyplot(fig3)
