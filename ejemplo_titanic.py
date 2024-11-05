import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import os

# Ruta al archivo CSV
ruta_csv = "T-001-S1.csv"

# Verificar si el archivo existe
if not os.path.exists(ruta_csv):
    st.error(f"El archivo {ruta_csv} no se encontró en el directorio actual.")
else:
    try:
        # Leer el CSV con separador ';' y codificación 'latin1'
        df = pd.read_csv(ruta_csv, sep=';', encoding='latin1', on_bad_lines='skip')
        
        # Limpiar los nombres de las columnas
        df.columns = df.columns.str.strip()

        # Mostrar un título y una descripción en la aplicación Streamlit
        st.write("""
        # Mi primera aplicación interactiva
        ## Gráficos usando la base de datos
        """)

        colores = ["red", "blue", "green", "purple", "yellow", "brown"]

        # Barra lateral interactiva
        with st.sidebar:
            st.sidebar.title("Mi primera barra lateral de Streamlit")
            st.sidebar.header("Hola barra lateral!")
            st.sidebar.write("Esto es una barra lateral")
            
            # Botones interactivos en la barra lateral
            if st.sidebar.button("Haz clic para cambiar el color de los gráficos"):
                st.sidebar.write(colores)
            if st.sidebar.button("Haz clic pero en la barra lateral"):
                st.sidebar.write("Has hecho clic en el botón de la barra lateral")
            
            # Entrada de texto en la barra lateral
            user_input = st.sidebar.text_input("Escribe algo en la barra")
            st.sidebar.write("Escribiste en la barra:", user_input)
            
            # Título para la sección de opciones en la barra lateral
            st.write("# Opciones")
            
            # Control deslizante (slider) para el número de bins
            div = st.slider('Número de bins:', 1, 50, 10)
            st.write("Bins =", div)
        
        # Seleccionar colores aleatorios para los gráficos
        color1 = random.choice(colores)
        color2 = random.choice(colores)
        
        # Gráfico de dispersión de 'I(A)' vs 'P(W)'
        fig1, ax1 = plt.subplots()
        ax1.scatter(df['I(A)'], df['P(W)'], color=color1, alpha=0.5)
        ax1.set_xlabel('Corriente (A)')
        ax1.set_ylabel('Potencia (W)')
        ax1.set_title('Dispersión de Corriente vs Potencia')
        st.pyplot(fig1)
        
        # Gráfico de líneas de 'P(W)' a lo largo de las lecturas
        fig2, ax2 = plt.subplots()
        ax2.plot(df.index, df['P(W)'], color=color2, linestyle='-', marker='o')
        ax2.set_xlabel('Número de Lectura')
        ax2.set_ylabel('Potencia (W)')
        ax2.set_title('Potencia a lo largo de las Lecturas')
        st.pyplot(fig2)
        
        st.write("""
        ## Muestra de datos cargados
        """)
        # Mostrar todo el DataFrame con capacidad de desplazamiento
        st.dataframe(df)
        
    except pd.errors.ParserError as pe:
        st.error(f"Error al parsear el archivo CSV: {pe}")
    except UnicodeDecodeError as ude:
        st.error(f"Error de codificación al leer el archivo CSV: {ude}")
    except KeyError as ke:
        st.error(f"Error de columna: {ke}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
