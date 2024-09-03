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