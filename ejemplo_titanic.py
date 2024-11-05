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
        # Carga el archivo CSV "T-001-S1.csv" en un DataFrame de pandas.
        # Especifica el separador y la codificación si es necesario.
        df = pd.read_csv(ruta_csv, sep=';', encoding='latin1')
        
        # Mostrar un título y una descripción en la aplicación Streamlit.
        st.write("""
        # Mi primera aplicación interactiva
        ## Gráficos usando la base de datos del Titanic
        """)
        
        colores = ["red", "blue", "green", "purple", "yellow", "brown"]
        
        # Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
        with st.sidebar:
            st.sidebar.title("Mi primera barra lateral de Streamlit")
            st.sidebar.header("Hola barra lateral!")
            st.sidebar.write("Esto es una barra lateral")
        
            st.sidebar.image("imagen1.png")
            
            if st.sidebar.button("Haz clic para cambiar el color de los gráficos"):
                st.sidebar.write(colores)
            if st.sidebar.button("Haz clic pero en la barra lateral"):
                st.sidebar.write("Has hecho clic en el botón de la barra lateral")
        
            user_input = st.sidebar.text_input("Escribe algo en la barra")
            st.sidebar.write("Escribiste en la barra:", user_input)
            
            # Título para la sección de opciones en la barra lateral.
            st.sidebar.write("# Opciones")
            
            # Crea un control deslizante (slider) que permite al usuario seleccionar un número de bins
            # en el rango de 0 a 10, con un valor predeterminado de 2.
            div = st.sidebar.slider('Número de bins:', 0, 10, 2)
            
            # Muestra el valor actual del slider en la barra lateral.
            st.sidebar.write("Bins =", div)
        
        i = random.randint(0, 5)
        color1 = colores[i]
        i = random.randint(0, 5)
        color2 = colores[i]
        
        # Desplegamos un gráfico de dispersión con los datos del eje X
        fig1, ax1 = plt.subplots()
        ax1.scatter(df['I(A)   '], df['P(W)   '], color=color1, alpha=0.5)
        ax1.set_xlabel('Corriente (A)')
        ax1.set_ylabel('Potencia (W)')
        ax1.set_title('Dispersión de Corriente vs Potencia')
        st.pyplot(fig1)
        
        # Combinar Fecha y Hora en un timestamp
        try:
            df['Timestamp'] = pd.to_datetime(df['Fecha medida'] + ' ' + df['Hora medida'], format='%d/%m/%y %H:%M:%S')
        except Exception as e:
            st.error(f"Error al combinar Fecha y Hora: {e}")
        
        # Desplegamos el gráfico de líneas de Potencia a lo largo del Tiempo
        fig2, ax2 = plt.subplots()
        ax2.plot(df['Timestamp'], df['P(W)   '], color=color2, linestyle='-', marker='o')
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('Potencia (W)')
        ax2.set_title('Potencia a lo largo del Tiempo')
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        
        st.write("""
        ## Muestra de datos cargados
        """)
        # Graficamos una tabla
        st.table(df.head())
        
    except pd.errors.ParserError as pe:
        st.error(f"Error al parsear el archivo CSV: {pe}")
    except UnicodeDecodeError as ude:
        st.error(f"Error de codificación al leer el archivo CSV: {ude}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
