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
        # Leer el CSV con separador ';', codificación 'latin1' y saltar líneas problemáticas
        df = pd.read_csv(ruta_csv, sep=';', encoding='latin1', on_bad_lines='skip')
        
        # Limpiar los nombres de las columnas (eliminar espacios al inicio y final)
        df.columns = df.columns.str.strip()
        
        # Mostrar las columnas disponibles para depuración
        st.write("**Columnas disponibles en el DataFrame:**")
        st.write(df.columns.tolist())

        # Verificar si las columnas necesarias existen
        columnas_necesarias = ['I(A)', 'P(W)', 'Fecha medida', 'Hora medida']
        columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
        if columnas_faltantes:
            st.error(f"Las siguientes columnas faltan en el archivo CSV: {', '.join(columnas_faltantes)}")
        else:
            # Mostrar un título y una descripción en la aplicación Streamlit.
            st.write("""
            # Mi primera aplicación interactiva
            ## Gráficos usando la base de datos
            """)

            colores = ["red", "blue", "green", "purple", "yellow", "brown"]

            # Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
            with st.sidebar:
                st.sidebar.title("Mi primera barra lateral de Streamlit")
                st.sidebar.header("Hola barra lateral!")
                st.sidebar.write("Esto es una barra lateral")

                # Asegúrate de tener una imagen llamada "imagen1.png" en el directorio correcto
                # Si no la tienes, comenta o elimina la siguiente línea
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

            # Seleccionar colores aleatorios para los gráficos
            color1 = random.choice(colores)
            color2 = random.choice(colores)
            
            # Desplegamos un gráfico de dispersión con los datos del eje X
            fig1, ax1 = plt.subplots()
            ax1.scatter(df['I(A)'], df['P(W)'], color=color1, alpha=0.5)
            ax1.set_xlabel('Corriente (A)')
            ax1.set_ylabel('Potencia (W)')
            ax1.set_title('Dispersión de Corriente vs Potencia')
            st.pyplot(fig1)
            
            # Combinar Fecha y Hora en un timestamp
            try:
                df['Timestamp'] = pd.to_datetime(
                    df['Fecha medida'].astype(str) + ' ' + df['Hora medida'].astype(str),
                    format='%d/%m/%y %H:%M:%S',
                    errors='coerce',
                    dayfirst=True
                )
            except Exception as e:
                st.error(f"Error al combinar Fecha y Hora: {e}")
            
            # Eliminar filas con Timestamps inválidos
            df = df.dropna(subset=['Timestamp'])
            
            # Desplegamos el gráfico de líneas de Potencia a lo largo del Tiempo
            fig2, ax2 = plt.subplots()
            ax2.plot(df['Timestamp'], df['P(W)'], color=color2, linestyle='-', marker='o')
            ax2.set_xlabel('Tiempo')
            ax2.set_ylabel('Potencia (W)')
            ax2.set_title('Potencia a lo largo del Tiempo')
            plt.xticks(rotation=45)
            st.pyplot(fig2)
            
            st.write("""
            ## Muestra de datos cargados
            """)
            # Graficamos una tabla
            st.table(df)
            
    except pd.errors.ParserError as pe:
        st.error(f"Error al parsear el archivo CSV: {pe}")
    except UnicodeDecodeError as ude:
        st.error(f"Error de codificación al leer el archivo CSV: {ude}")
    except KeyError as ke:
        st.error(f"Error de columna: {ke}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
