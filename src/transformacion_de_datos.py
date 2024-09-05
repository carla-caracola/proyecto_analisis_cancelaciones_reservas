# %%

# Imports 📥
#-----------------------------------------------------------------------

# >> Packages
import pandas as pd
import numpy as np
import re
import calendar

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# >> Settings
pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames


# >> Functions

def reemplazar_fechas_erroneas(fecha):
    """
    Dada una fecha, esta función verifica si el formato de la misma coincide con 'AAAA-MM-DD' y de ser así devuelve un valor nulo.   
    Si el formato no coincide o si no es cadena de texto devuelve la misma fecha.

    Args:
        fecha (string): fecha cuyo formato se quiere verificar.

    Returns: 
        np.null: si el formato coincide.
        El mismo argumento que se le ingresó si el formato no coincide o si no es cadena de texto. 
    """
    # Verificar si el valor es una cadena de texto
    if isinstance(fecha, str):
        # Expresión regular para identificar fechas en formato 'AAAA-MM-DD'
        patron = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(patron, fecha):
            return np.nan
    # Si no es una cadena de texto o no coincide con el patrón, devolver el valor original
    return fecha
# %%

def quick_check(df, column_name):
        """ This function is for testing purposes, to quicky check data type and unique values of a column"""
        print (f"\nColumn name: {column_name}")
        print (f"\nData type: {df[column_name].dtype}")
        print (f"\nNot null count: {df[column_name].notnull().sum()}")
        print (f"\nNull count: {df[column_name].isnull().sum()}, {round(df[column_name].isnull().sum()/df.shape[0]*100)}%")
        print (f"\nDuplicated values: {df[column_name].duplicated().sum()}")
        print (f"\nUnique values: \n{df[column_name].unique()}")
        print (f"\nValue counts: \n{df[column_name].value_counts()}") 


# Función para transformar fechas con formato 'AAAA-MM-DD 00:00:00' en 'AAAA-MM-DD'
def quitar_horas (fecha):
    """ 
    A partir de una fecha, esta función divide los componentes de la misma por espacios y retorna el primer elemento.  
    """
    # Verificar si el valor es una cadena de texto
    if isinstance(fecha, str):
        fecha = fecha.split()[0]
        return fecha
    # Si no es una cadena de texto, devolver el valor original
    return fecha
# %%
# →  Estandarizar para que en todos los casos sean números y cambiar el datatype de la columna a número entero.

def cambiar_formato_mes(df):
    # Diccionario de mapeo de meses y valores numéricos
    dic_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 
        'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
        'November': 11, 'December': 12, 
        1: 1, 2: 2, 3: 3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 'nan': np.nan}
    
    # Asegurarse de que los valores en la columna sean de tipo string para mapear correctamente
    df['arrival_date_month'] = df['arrival_date_month'].astype(str).map(dic_map).astype('Int64')

    return df


def rellenar_fecha_llegada(df):  

    print(f'Nulos antes de hacer la operación:')
    print(f'- arrival_date_year: {df["arrival_date_year"].isna().sum()}')
    print(f'- arrival_date_month: {df["arrival_date_month"].isna().sum()}')
    print(f'- arrival_date_day_of_month: {df["arrival_date_day_of_month"].isna().sum()}')

    # Asegúrate de que las columnas de fecha estén en formato datetime
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

    # Crear una columna para el total de la estancia
    df['total_stays'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

    # Inicializar la columna de fecha de llegada estimada con valores NaT (Not a Time)
    df['estimated_arrival_date'] = pd.NaT

    # Crear filtro para cuando el estado de la reserva es "Checkout"
    filtro_checkout = df['reservation_status'] == 'Checkout'

    # Calcular fecha de llegada estimada para "Checkout"
    df.loc[filtro_checkout, 'estimated_arrival_date'] = df.loc[filtro_checkout, 'reservation_status_date'] - pd.to_timedelta(df.loc[filtro_checkout, 'total_stays'], unit='D')

    # Para los que no son "Checkout", asumir que la llegada fue la fecha del estado de la reserva
    df.loc[~filtro_checkout, 'estimated_arrival_date'] = df.loc[~filtro_checkout, 'reservation_status_date']

    # Extraer el año, mes y día de la fecha de llegada estimada
    df['estimated_arrival_year'] = df['estimated_arrival_date'].dt.year
    df['estimated_arrival_month'] = df['estimated_arrival_date'].dt.month
    df['estimated_arrival_day'] = df['estimated_arrival_date'].dt.day

    # Rellenar los valores nulos en arrival_date_year, arrival_date_month y arrival_date_day_of_month con los valores estimados
    df['arrival_date_year'] = df['arrival_date_year'].fillna(df['estimated_arrival_year'])
    df['arrival_date_month'] = df['arrival_date_month'].fillna(df['estimated_arrival_month'])
    df['arrival_date_day_of_month'] = df['arrival_date_day_of_month'].fillna(df['estimated_arrival_day'])


    print(f'Nulos después de hacer la operación:')
    print(f'- arrival_date_year: {df["arrival_date_year"].isna().sum()}')
    print(f'- arrival_date_month: {df["arrival_date_month"].isna().sum()}')
    print(f'- arrival_date_day_of_month: {df["arrival_date_day_of_month"].isna().sum()}')

    # borramos las columnas creadas para hacer los cálculos
    columnas_a_borrar = ['estimated_arrival_date', 'estimated_arrival_year', 'estimated_arrival_month', 'estimated_arrival_day']
    df = df.drop(columns=columnas_a_borrar)


def imputar_knn_fechas(df, n_neighbors=5):
    # Seleccionar las columnas relevantes para la imputación
    cols_fecha = ['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month']
    
    # Filtrar el DataFrame para las columnas de fechas y convertirlas a float para KNNImputer
    df_fechas = df[cols_fecha].astype(float)
    
    # Imputar los valores nulos usando KNN
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_imputado = imputer.fit_transform(df_fechas)
    
    # Convertir el resultado de vuelta a un DataFrame con las mismas columnas
    df_imputado = pd.DataFrame(df_imputado, columns=cols_fecha)
    
    # Asegurarse de que los valores imputados sean enteros
    df_imputado = df_imputado.round().astype(int)
    
    # Verificar y ajustar los días para que no excedan los máximos permitidos por mes
    for index, row in df_imputado.iterrows():
        year = row['arrival_date_year']
        month = row['arrival_date_month']
        day = row['arrival_date_day_of_month']
        
        # Obtener el último día del mes específico
        last_day_of_month = calendar.monthrange(year, month)[1]
        
        # Ajustar si el día excede el máximo
        if day > last_day_of_month:
            df_imputado.at[index, 'arrival_date_day_of_month'] = last_day_of_month
    
    # Reemplazar las columnas originales en el DataFrame con los valores imputados y ajustados
    df[cols_fecha] = df_imputado
    
    # Imprimir los nulos restantes en las columnas relevantes
    print(f'Nulos después de la operación:')
    print(f'- arrival_date_year: {df["arrival_date_year"].isna().sum()}')
    print(f'- arrival_date_month: {df["arrival_date_month"].isna().sum()}')
    print(f'- arrival_date_day_of_month: {df["arrival_date_day_of_month"].isna().sum()}')

def crear_columna_arrival_date(df):
# Crear la columna de fecha combinada inicialmente
    df['arrival_date'] = pd.to_datetime(
        df[['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month']].astype(str).agg('-'.join, axis=1), 
        format='%Y-%m-%d', 
        errors='coerce' ) # Esto convertirá fechas inválidas a NaT

def calcular_fecha_reserva(df):
    # Asegurar de que 'arrival_date' está en formato datetime
    df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')
    
    # Calcular 'reservation_date' restando 'lead_time' de 'arrival_date'
    df['reservation_date'] = df['arrival_date'] - pd.to_timedelta(df['lead_time'], unit='d')
# %%

def convertir_a_boleano(df, columnas):
    """
    Convierte las columnas especificadas de un DataFrame a tipo booleano.
    Parámetros:
    df (pandas.DataFrame): El DataFrame en el que se encuentran las columnas.
    columnas (list): Lista de nombres de columnas a convertir.
    Retorna:
    pandas.DataFrame: El DataFrame con las columnas convertidas a booleano.
    """
    print(f'El tipo de dato antes del cambio \n {df["is_repeated_guest"].dtype} \n {df["is_canceled"].dtype}')
    for columna in columnas:
        df[columna] = df[columna].astype(bool)
    print(f'El tipo de dato después del cambio \n {df["is_repeated_guest"].dtype} \n {df["is_canceled"].dtype}')
    return df

def eliminar_segundo_digito (df, columnas):
    for columna in columnas:
        print(f"{columna.upper()} --> Valores únicos antes de eliminar: {df[columna].nunique()}")
        df[columna] = df[columna].apply(lambda num: num if num < 10 else num // 10 )
        print(f"{columna.upper()} --> Valores únicos después de eliminar: {df[columna].nunique()}")
    return df

# Función para imputar valores en la columna 'market_segment'
def imputar_market_segment(row):    
    if pd.isnull(row['market_segment']):
        # Reglas para imputar los valores nulos
        if row['distribution_channel'] == 'Corporate':
            return 'Corporate'
        elif row['distribution_channel'] == 'Direct':
            return 'Direct'
        elif row['distribution_channel'] == 'Corporate':
            return 'Corporate'
        elif row['distribution_channel'] == 'Undifined':
            return 'Undifined'        
    else:
        return row['market_segment']

# Función para imputar valores en la columna 'market_segment'
def imputar_distribution_channel(row):
    if pd.isnull(row['distribution_channel']):
        # Reglas para imputar los valores nulos
        if row['market_segment'] == 'Aviation' or 'Corporate':
            return 'Corporate'
        elif row['market_segment'] == 'Complementary':
            return 'Direct'        
        elif row['market_segment'] == 'Direct':
            return 'Direct'
        elif row['market_segment'] == 'Groups' or 'Offline TA/TO' or 'Online TA':
            return 'TA/TO' 
        elif row['market_segment'] == 'Undifined':
            return 'Undifined'    
    else:
        return row['distribution_channel'] 


def imputar_nulos_iterative (df, columns):
    """
    Dada una lista de columnas y un DataFrame, esta función completa los nulos de las columnas con el método IterativeImputer.
    Además, redondea los valores imputados a enteros y asegura que no haya valores negativos.
        Parámetros:
    df (pd.DataFrame): El DataFrame a procesar.
    columns (list): Lista de nombres de columnas a imputar.
        Retorna:
    pd.DataFrame: El DataFrame con los valores nulos imputados.
    """
    # Número de Nan y distribución antes de aplicar el método
    for column in columns:
        print(f"Porcentaje de NaN en '{column}': {df[column].isna().sum() / df.shape[0]:.2f}%")
        print(df[column].value_counts() / df.shape[0] * 100)
    # instanciamos las clases
    imputer_iterative = IterativeImputer(max_iter = 20, random_state = 42)  
    # ajustamos y tranformamos los datos
    imputer_iterative_imputado = imputer_iterative.fit_transform(df[columns])
    # Redondeamos los valores imputados a enteros
    imputer_iterative_imputado = np.round(imputer_iterative_imputado).astype(int)
    # Nos aseguramos de que no haya valores negativos
    imputer_iterative_imputado[imputer_iterative_imputado < 0] = 0
    # Asignamos los valores imputados de vuelta al DataFrame
    df[columns] = imputer_iterative_imputado
    # Número de Nan y distribución después de aplicar el método
    for column in columns:
        print(f"Porcentaje de NaN en '{column}': {df[column].isna().sum() / df.shape[0]:.2f}%")
        print(df[column].value_counts() / df.shape[0] * 100)
    return df
