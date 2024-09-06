# %%
# Imports
from src import transformacion_de_datos as td
import pandas as pd
import datetime

# %%
# Importar datos
df = pd.read_csv("data/finanzas_hotel_bookings.csv", index_col=0)

#%%
# Eliminar filas a partir de la 119390
df = df.iloc[:119390]

# Eliminar columna '0' y sobreescribir los cambios
df.drop("0", axis = 1, inplace = True) 

# %%
# Corregir fechas erroneas de la columna 'reservation_status_date'
df['reservation_status_date'] = df['reservation_status_date'].apply(td.reemplazar_fechas_erroneas)

#%%
# Transformar fechas con formato 'AAAA-MM-DD 00:00:00' en 'AAAA-MM-DD'
df['reservation_status_date'] = df['reservation_status_date'].apply(td.quitar_horas)

#%%
td.cambiar_formato_mes(df)

td.rellenar_fecha_llegada(df)

td.imputar_knn_fechas(df)

td.crear_columna_arrival_date(df)

td.calcular_fecha_reserva(df)

df['arrival_date_week_number'] = df['arrival_date_week_number'].fillna(df['arrival_date'].dt.isocalendar().week)
# Convierte los valores de la columna a positivos
df['adr'] = df['adr'].abs()

td.rellenar_fecha_estado_reserva(df)

# %%
columnas = ["is_repeated_guest", "is_canceled"]
td.convertir_a_boleano(df, columnas)

columnas = ["adults", "children", "babies"]
td.eliminar_segundo_digito(df, columnas)

# Imputar nulos de la columna "distribution_channel" a la categoría "Undefined"
df["distribution_channel"].fillna("Undefined")

# Aplicar la función al DataFrame
df['market_segment'] = df.apply(td.imputar_market_segment, axis=1)

columnas = ["children", "previous_cancellations"]
td.imputar_nulos_iterative(df, columnas )

# Imputar nulos por 'Unknown'
lista_columnas = ['country', 'company', 'agent', "reserved_room_type"]
td.imputar_por_unknown (df, lista_columnas)

# Imputar nulos por la moda
lista_columnas = ["is_repeated_guest","customer_type"]
td.imputar_por_moda (df, lista_columnas)


# %%

df.to_csv(f'data/finanzas_hotel_booking_transformado.csv')



# %%