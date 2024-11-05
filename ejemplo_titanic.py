import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Carga el archivo CSV "database_titanic.csv" en un DataFrame de pandas.
df = pd.read_csv("T-001-S1.csv")

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

colores = ["red", "blue", "green", "purple", "yellow", "brown"]

# Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
with st.sidebar:
    st.sidebar.title("Mi primera barra lateral de streamlit")
    st.sidebar.header("Hola barra lateral!")
    st.sidebar.write("Esto es una barra lateral")

    st.sidebar.image("imagen1.png")
    
    if st.sidebar.button("Haz clic para cambiar el color de los graficos"):
        st.sidebar.write(color)
    if st.sidebar.button("Haz clic pero en la barra lateral"):
        st.sidebar.write("Haz hecho clic en el boton de la barra lateral")

    user_input = st.sidebar.text_input("escribe algo en la barra")
    st.sidebar.write("Escribiste en la barra:", user_input)
    
    # Título para la sección de opciones en la barra lateral.
    st.write("# Opciones")
    
    # Crea un control deslizante (slider) que permite al usuario seleccionar un número de bins
    # en el rango de 0 a 10, con un valor predeterminado de 2.
    div = st.slider('Número de bins:', 0, 10, 2)
    
    # Muestra el valor actual del slider en la barra lateral.
    st.write("Bins=", div)

i = random.randint(0, 5)
color1 = colores[i]
i = random.randint(0, 5)
color2 = colores[i]
# Desplegamos un histograma con los datos del eje X
fig, ax = plt.subplots()
ax.scatter(df['I(A)'], df['P(W)'], color='blue', alpha=0.5)
ax.set_xlabel('Corriente (A)')
ax.set_ylabel('Potencia (W)')
ax.set_title('Dispersión de Corriente vs Potencia')


# Combinar Fecha y Hora en un timestamp
df['Timestamp'] = pd.to_datetime(df['Fecha medida'] + ' ' + df['Hora medida'], format='%d/%m/%y %H:%M:%S')
fig, ax = plt.subplots()
ax.plot(df['Timestamp'], df['P(W)'], color='green', linestyle='-', marker='o')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Potencia (W)')
ax.set_title('Potencia a lo largo del Tiempo')
plt.xticks(rotation=45)

# Desplegamos el gráfico
st.pyplot(fig)

st.write("""
## Muestra de datos cargados
""")
# Graficamos una tabla
st.table(df.head())
