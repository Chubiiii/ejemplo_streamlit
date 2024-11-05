import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import os
from datetime import datetime

# Título de la Aplicación
st.title("Aplicación Interactiva de Datos")
st.write("## Visualización de Datos con Streamlit")

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
        st.sidebar.header("Configuración de Datos")
        st.sidebar.write("**Columnas disponibles:**")
        st.sidebar.write(df.columns.tolist())
        
        # Verificar si las columnas necesarias existen
        columnas_necesarias = ['I(A)', 'P(W)', 'Fecha medida', 'Hora medida']
        columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
        if columnas_faltantes:
            st.error(f"Las siguientes columnas faltan en el archivo CSV: {', '.join(columnas_faltantes)}")
        else:
            # Selección de columnas para los gráficos
            opciones_columnas = {
                'Eje X': ['I(A)', 'P(W)', 'Fecha medida', 'Hora medida'],
                'Eje Y': ['I(A)', 'P(W)', 'Fecha medida', 'Hora medida']
            }
            eje_x = st.sidebar.selectbox("Selecciona la columna para el Eje X:", opciones_columnas['Eje X'], index=0)
            eje_y = st.sidebar.selectbox("Selecciona la columna para el Eje Y:", opciones_columnas['Eje Y'], index=1)
            
            # Selección de rango de fechas
            df['Fecha'] = pd.to_datetime(df['Fecha medida'], dayfirst=True, errors='coerce')
            fecha_min = df['Fecha'].min()
            fecha_max = df['Fecha'].max()
            rango_fechas = st.sidebar.date_input("Selecciona el rango de fechas:", [fecha_min, fecha_max])
            
            if len(rango_fechas) != 2:
                st.error("Por favor, selecciona un rango válido de fechas.")
            else:
                # Filtrar el DataFrame por el rango de fechas seleccionado
                inicio, fin = rango_fechas
                mask = (df['Fecha'] >= pd.to_datetime(inicio)) & (df['Fecha'] <= pd.to_datetime(fin))
                df_filtrado = df.loc[mask]
                
                st.write(f"### Datos filtrados desde {inicio} hasta {fin}")
                st.write(f"Total de registros: {df_filtrado.shape[0]}")
                
                # Selección de colores para los gráficos
                colores = ["red", "blue", "green", "purple", "yellow", "brown"]
                color_x = st.sidebar.selectbox("Selecciona el color para el Eje X:", colores, index=1)
                color_y = st.sidebar.selectbox("Selecciona el color para el Eje Y:", colores, index=2)
                
                # Opciones para mostrar gráficos
                mostrar_scatter = st.sidebar.checkbox("Mostrar Gráfico de Dispersión", value=True)
                mostrar_line = st.sidebar.checkbox("Mostrar Gráfico de Líneas", value=True)
                
                # Crear Timestamp combinando Fecha y Hora
                df_filtrado['Hora'] = pd.to_datetime(df_filtrado['Hora medida'], format='%H:%M:%S', errors='coerce').dt.time
                df_filtrado['Timestamp'] = df_filtrado.apply(
                    lambda row: datetime.combine(row['Fecha'], row['Hora']) if pd.notnull(row['Hora']) else pd.NaT,
                    axis=1
                )
                df_filtrado = df_filtrado.dropna(subset=['Timestamp'])
                
                # Gráfico de Dispersión
                if mostrar_scatter:
                    fig1, ax1 = plt.subplots()
                    ax1.scatter(df_filtrado[eje_x], df_filtrado[eje_y], color=color_x, alpha=0.5)
                    ax1.set_xlabel(eje_x)
                    ax1.set_ylabel(eje_y)
                    ax1.set_title(f'Dispersión de {eje_x} vs {eje_y}')
                    st.pyplot(fig1)
                
                # Gráfico de Líneas
                if mostrar_line:
                    fig2, ax2 = plt.subplots()
                    ax2.plot(df_filtrado['Timestamp'], df_filtrado[eje_y], color=color_y, linestyle='-', marker='o')
                    ax2.set_xlabel('Tiempo')
                    ax2.set_ylabel(eje_y)
                    ax2.set_title(f'{eje_y} a lo largo del Tiempo')
                    plt.xticks(rotation=45)
                    st.pyplot(fig2)
                
                # Mostrar una muestra de los datos cargados
                st.write("## Muestra de Datos Cargados")
                st.table(df_filtrado.head())
                
                # Opcional: Descargar datos filtrados
                csv = df_filtrado.to_csv(index=False)
                st.download_button(
                    label="Descargar Datos Filtrados",
                    data=csv,
                    file_name='datos_filtrados.csv',
                    mime='text/csv',
                )
                
    except pd.errors.ParserError as pe:
        st.error(f"Error al parsear el archivo CSV: {pe}")
    except UnicodeDecodeError as ude:
        st.error(f"Error de codificación al leer el archivo CSV: {ude}")
    except KeyError as ke:
        st.error(f"Error de columna: {ke}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
