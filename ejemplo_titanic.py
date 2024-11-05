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

        # Convertir 'I(A)' y 'P(W)' a numéricos
        df['I(A)'] = pd.to_numeric(df['I(A)'], errors='coerce')
        df['P(W)'] = pd.to_numeric(df['P(W)'], errors='coerce')

        # Eliminar filas con valores NaN en 'I(A)' y 'P(W)'
        df = df.dropna(subset=['I(A)', 'P(W)'])

        # Mostrar un título y una descripción en la aplicación Streamlit
        st.write("""
        # Mi primera aplicación interactiva
        ## Gráficos usando la base de datos
        """)

        colores = ["red", "blue", "green", "purple", "yellow", "brown"]

        # Barra lateral interactiva
        with st.sidebar:
            st.sidebar.title("Mi primera barra lateral de Streamlit")
            st.sidebar.header("Configuración de gráficos")

            # Selección de color
            color_seleccionado = st.selectbox('Selecciona el color del gráfico:', colores)
            st.write("Color seleccionado:", color_seleccionado)

            # Tipo de marcador
            marcadores = ['o', 's', '^', 'D', 'v', '*']
            marcador_seleccionado = st.selectbox('Selecciona el tipo de marcador:', marcadores)
            st.write("Marcador seleccionado:", marcador_seleccionado)

            # Tamaño de los puntos
            tamaño_punto = st.slider('Selecciona el tamaño de los puntos:', 1, 20, 5)
            st.write("Tamaño de punto:", tamaño_punto)

            # Título para la sección de opciones en la barra lateral
            st.write("# Opciones")

            # Control deslizante para ajustar la transparencia
            alpha_valor = st.slider('Selecciona la transparencia:', 0.0, 1.0, 0.7)
            st.write("Transparencia seleccionada:", alpha_valor)

        # Gráfico de dispersión interactivo de 'I(A)' vs 'P(W)'
        fig1, ax1 = plt.subplots()
        ax1.scatter(df['I(A)'], df['P(W)'], color=color_seleccionado, alpha=alpha_valor,
                    s=tamaño_punto*10, marker=marcador_seleccionado)
        ax1.set_xlabel('Corriente (A)')
        ax1.set_ylabel('Potencia (W)')
        ax1.set_title('Dispersión de Corriente vs Potencia')
        st.pyplot(fig1)

        # Gráfico de líneas de 'P(W)' a lo largo de las lecturas
        fig2, ax2 = plt.subplots()
        ax2.plot(df.index, df['P(W)'], color=color_seleccionado, linestyle='-',
                 marker=marcador_seleccionado, markersize=tamaño_punto)
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
