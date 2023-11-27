import pandas as pd
import matplotlib.pyplot as plt

parquet_result_1v = '/Users/liammacgaw/Desktop/InfoVis/tp/ResultadosElectorales_1v.parquet'
parquet_result_paso = '/Users/liammacgaw/Desktop/InfoVis/tp/ResultadosElectorales_PASO_2023.parquet'

result_1v = pd.read_parquet(parquet_result_1v, engine='pyarrow')
result_paso = pd.read_parquet(parquet_result_paso, engine='pyarrow')


# Votos por provincia para las tres agrupaciones principales en 1er vuelta
agrupaciones_seleccionadas = ["UNION POR LA PATRIA", "JUNTOS POR EL CAMBIO", "LA LIBERTAD AVANZA"]
df_seleccionado = result_1v[
    (result_1v['agrupacion_nombre'].isin(agrupaciones_seleccionadas)) &
    (result_1v['cargo_nombre'] == 'PRESIDENTE Y VICE')
]
df_provincia_votos = df_seleccionado.groupby(['distrito_nombre', 'agrupacion_nombre'])['votos_cantidad'].sum().unstack()
fig, ax = plt.subplots(figsize=(12, 8))
colors = {'UNION POR LA PATRIA': 'blue', 'JUNTOS POR EL CAMBIO': 'yellow', 'LA LIBERTAD AVANZA': 'purple'}
df_provincia_votos.plot(kind='barh', ax=ax, color=[colors[col] for col in df_provincia_votos.columns])
plt.title('Cantidad de votos a cargo "PRESIDENTE Y VICE" por Agrupación y Provincia en 1er Vuelta')
plt.xlabel('Votos')
plt.ylabel('Provincia')
plt.legend(title='Agrupación', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# Top 5 agrupaciones con mas votos en las PASO
resultados_presidente = result_paso[result_paso['cargo_nombre'] == 'PRESIDENTE/A']
votos_por_agrupacion = resultados_presidente.groupby('agrupacion_nombre')['votos_cantidad'].sum()
votos_por_agrupacion = votos_por_agrupacion.sort_values(ascending=False)
top_agrupaciones = votos_por_agrupacion.head(5)
plt.figure(figsize=(10, 6))
top_agrupaciones.plot(kind='barh', color='skyblue')  
plt.title('Top 5 Agrupaciones con Mayor Cantidad de Votos para PRESIDENTE/A en las PASO')
plt.xlabel('Cantidad de Votos')
plt.ylabel('Agrupación')
plt.show()


# Diferencia de Votos Presidencial entre PASO y Primera Vuelta por Agrupación'
agrupaciones_deseadas = ["UNION POR LA PATRIA", "JUNTOS POR EL CAMBIO", "LA LIBERTAD AVANZA", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "HACEMOS POR NUESTRO PAIS"]
result_paso_filtrado = result_paso[result_paso['agrupacion_nombre'].isin(agrupaciones_deseadas)]
result_1v_filtrado = result_1v[result_1v['agrupacion_nombre'].isin(agrupaciones_deseadas)]
result_paso_presidente = result_paso_filtrado[(result_paso_filtrado['cargo_nombre'] == 'PRESIDENTE/A')]
result_1v_presidente_vice = result_1v_filtrado[(result_1v_filtrado['cargo_nombre'] == 'PRESIDENTE Y VICE')]
total_votos_paso = result_paso_presidente.groupby('agrupacion_nombre')['votos_cantidad'].sum()
total_votos_primera_vuelta = result_1v_presidente_vice.groupby('agrupacion_nombre')['votos_cantidad'].sum()
diferencia_votos = total_votos_primera_vuelta - total_votos_paso
plt.figure(figsize=(10, 6))
ax = diferencia_votos.plot(kind='barh', color='skyblue')
ax.axvline(x=0, color='black', linestyle='--')
for i, v in enumerate(diferencia_votos):
    ax.text(v + 5 if v > 0 else v - 25, i, str(v), color='black')
plt.title('Diferencia de Votos Presidencial entre PASO y Primera Vuelta por Agrupación')
plt.xlabel('Diferencia de Votos')
plt.ylabel('Agrupación')
plt.show()


 # Top 5 provincias con mayor cantidad de votos para agrupacion_elegida (comparada con otras agrupaciones) en 1er vuelta
agrupaciones_permitidas = ["UNION POR LA PATRIA", "JUNTOS POR EL CAMBIO", "LA LIBERTAD AVANZA"]
while True:
    agrupacion_elegida = input("Ingrese el nombre de la agrupación (o 'salir' para salir): ")
    if agrupacion_elegida.lower() == 'salir':
        break
    elif agrupacion_elegida not in agrupaciones_permitidas:
        print("Agrupación no válida. Por favor, ingrese una de las siguientes: ")
        print(agrupaciones_permitidas)
    else:
        resultados_presidente = result_1v[result_1v['cargo_nombre'] == 'PRESIDENTE Y VICE']
        df_agrupacion = resultados_presidente[resultados_presidente['agrupacion_nombre'] == agrupacion_elegida]
        df_provincia_votos = df_agrupacion.groupby('distrito_nombre')['votos_cantidad'].sum().nlargest(5)
        otras_agrupaciones = [a for a in agrupaciones_permitidas if a != agrupacion_elegida]
        df_otras_agrupaciones = resultados_presidente[resultados_presidente['agrupacion_nombre'].isin(otras_agrupaciones)]
        df_otras_agrupaciones = df_otras_agrupaciones.groupby(['distrito_nombre', 'agrupacion_nombre'])['votos_cantidad'].sum().unstack()
        df_otras_agrupaciones = df_otras_agrupaciones.loc[df_provincia_votos.index]
        fig, ax = plt.subplots(figsize=(12, 8))
        if agrupacion_elegida == "UNION POR LA PATRIA":
            df_provincia_votos.plot(kind='barh', ax=ax, width=0.4, position=0, color='blue', label=agrupacion_elegida)
            df_otras_agrupaciones.plot(kind='barh', ax=ax, width=0.4, position=1, color=['yellow', 'purple'], label=otras_agrupaciones)
        elif agrupacion_elegida == "JUNTOS POR EL CAMBIO":
            df_provincia_votos.plot(kind='barh', ax=ax, width=0.4, position=0, color='yellow', label=agrupacion_elegida)
            df_otras_agrupaciones.plot(kind='barh', ax=ax, width=0.4, position=1, color=['purple', 'blue'], label=otras_agrupaciones)
        elif agrupacion_elegida == "LA LIBERTAD AVANZA":
            df_provincia_votos.plot(kind='barh', ax=ax, width=0.4, position=0, color='purple', label=agrupacion_elegida)
            df_otras_agrupaciones.plot(kind='barh', ax=ax, width=0.4, position=1, color=['yellow', 'blue'], label=otras_agrupaciones)
        plt.title(f'Top 5 provincias con mayor cantidad de votos para {agrupacion_elegida} en 1er Vuelta (comparada con otras agrupaciones)')
        plt.xlabel('Votos')
        plt.ylabel('Provincia')
        plt.legend(title='Agrupación', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()