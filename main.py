# %%
# Imports
from src import transformacion_de_datos as td
import pandas as pd

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
# %%
# Imputar con KNN las columnas 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month'
#td.imputar_knn_fechas(df) # (aún no lo ejecuté) --> Nos está dando problema. 

#%%
# Transformar fechas con formato 'AAAA-MM-DD 00:00:00' en 'AAAA-MM-DD'
df['reservation_status_date'] = df['reservation_status_date'].apply(td.quitar_horas)

#%%
df = td.cambiar_formato_mes(df)

td.rellenar_fecha_llegada(df)

td.imputar_knn_fechas(df)

td.crear_columna_arrival_date(df)


df['arrival_date_week_number'] = df['arrival_date_week_number'].fillna(df['arrival_date'].dt.isocalendar().week)



# %%
