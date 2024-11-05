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

# Gráfico de líneas de 'P(W)' a lo largo de las lecturas (índice del DataFrame)
fig2, ax2 = plt.subplots()
ax2.plot(df.index, df['P(W)'], color=color2, linestyle='-', marker='o')
ax2.set_xlabel('Número de Lectura')
ax2.set_ylabel('Potencia (W)')
ax2.set_title('Potencia a lo largo de las Lecturas')
st.pyplot(fig2)
