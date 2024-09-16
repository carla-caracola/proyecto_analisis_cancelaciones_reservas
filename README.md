# proyecto_visualizacion_vizlab
🏨 Análisis y Optimización de Cancelaciones de Reservas de Hoteles

📖 Introducción

Este proyecto tiene como objetivo analizar las cancelaciones de reservas en hoteles utilizando un conjunto de datos que contiene información detallada de las reservas realizadas. El análisis pretende identificar patrones y factores clave detrás de las cancelaciones, con el fin de ayudar a los hoteles a reducir esta tasa y mejorar la gestión de reservas.

A lo largo del proyecto, se utilizan herramientas de análisis de datos y visualización para crear un 📊 dashboard interactivo que permita a la gerencia del hotel tomar decisiones informadas basadas en datos.
🛠️ Documentación e Instrucciones de Instalación
Requisitos Previos

Para ejecutar este proyecto, necesitarás tener instaladas las siguientes herramientas:

    🐍 Python 3.x: Descargar Python
    📦 Pandas y NumPy para el análisis de datos.
    📊 Matplotlib y Seaborn para la creación de gráficos.
    📓 Jupyter Notebook para ejecutar y visualizar el análisis.

Instalación

    Clona este repositorio en tu máquina local:


git clone https://github.com/laural87/proyecto_visualizacion_vizlab.git

    Navega al directorio del proyecto:



cd project-da-promo-i-modulo-4-team-vizalab

    Instala las dependencias necesarias ejecutando:



pip install -r requirements.txt

    Inicia Jupyter Notebook:



jupyter notebook

    Abre el archivo hotel-booking-analysis.ipynb para ejecutar el análisis paso a paso.

💻 Instrucciones de Uso

Este proyecto se organiza en varias etapas:

    Limpieza de Datos: 🧹 Se realiza una limpieza exhaustiva del conjunto de datos para eliminar valores nulos, duplicados y otros problemas que puedan afectar el análisis.
    Análisis Exploratorio de Datos (EDA): 🔍 Visualizaciones y análisis estadísticos que identifican patrones de cancelaciones.
    Visualización de Resultados: Los resultados obtenidos se presentan en gráficos interactivos 📊.
    Dashboard Interactivo: Utiliza Tableau o Power BI para visualizar las principales métricas, tendencias y patrones de las cancelaciones.

🔧 Ejemplo de Uso
Cargar el conjunto de datos y ver un resumen:

python

import pandas as pd

# Cargar los datos
df = pd.read_csv('finanzas-hotel-bookings.csv')

# Mostrar las primeras filas
df.head()

Crear un gráfico que muestre la tasa de cancelación por mes:

python

import seaborn as sns
import matplotlib.pyplot as plt

# Crear un gráfico de cancelaciones por mes
sns.countplot(x='arrival_date_month', hue='is_canceled', data=df)
plt.title('Cancelaciones por Mes')
plt.show()

📊 Ejemplo del Dashboard

En nuestro dashboard interactivo podrás:

    🔍 Filtrar por tipo de cliente, fecha de llegada o canal de distribución.
    Ver la tasa de cancelación en función del país 🌍, segmento de mercado y otros factores.
    Explorar cómo la anticipación de la reserva influye en la probabilidad de cancelación ⏳.

🔧 Tecnologías Utilizadas

    🐍 Python: Lenguaje de programación principal.
    📦 Pandas y NumPy: Análisis y manipulación de datos.
    📊 Matplotlib y Seaborn: Visualización de datos.
    📈 Tableau/Power BI: Creación de dashboards interactivos.
    💻 GitHub: Control de versiones y colaboración.

Para más información sobre estas herramientas:

    Pandas
    Matplotlib
    Seaborn
    Tableau
    Power BI

❓ Preguntas Frecuentes (FAQ)

    ¿Qué es un "adr" en los datos?
        ADR significa Average Daily Rate (Tarifa Promedio Diaria) y es una métrica clave utilizada en el sector hotelero para medir el precio medio de una habitación por noche.

    ¿Cómo puedo acceder al dashboard?
        Una vez completado el análisis, el dashboard estará disponible en Tableau o Power BI. Puedes encontrar el archivo hotel-dashboard.twbx en este repositorio para Tableau o un enlace a la versión publicada en la web.

    ¿Puedo usar este conjunto de datos para otro tipo de análisis?
        ¡Por supuesto! Este conjunto de datos tiene potencial para otros análisis, como la predicción de reservas o el análisis de satisfacción del cliente.

📄 Licencia

Este proyecto está licenciado bajo la licencia MIT. Para más detalles, revisa el archivo LICENSE.
📧 Información de Contacto

Equipo de Desarrollo:

    👥 Nombre del equipo: Vizlab
    🚀 Promoción: Promo-I, Adalab
    ✉️ Correo de contacto: team-y@adalab.com

Si tienes alguna pregunta o sugerencia, no dudes en contactarnos a través de nuestro correo.