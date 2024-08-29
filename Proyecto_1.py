import requests                 #Se utiliza para enviar peticiones a servidores web y recibir respuestas, lo que facilita la extracción de datos de páginas web y servicios en línea.
from bs4 import BeautifulSoup   #sta librería es utilizada para analizar y manipular datos HTML y XML. Es especialmente útil para extraer información estructurada de páginas web, como buscar elementos específicos en un documento HTML y extraer su contenido.
import pandas as pd             #proporciona estructuras de datos flexibles y herramientas para manipular y analizar datos. Se utiliza para trabajar con datos tabulares, como hojas de cálculo, y facilita tareas como filtrar, limpiar y transformar datos.
import yfinance as yf           #librería que permite acceder a datos financieros y de mercado de Yahoo Finance. Se utiliza para obtener información sobre precios de acciones, volúmenes de operaciones, datos financieros y más, lo que es útil para análisis financiero y modelado.
import datetime                 #Esta librería proporciona clases para manipular fechas y horas en Python. Se utiliza para trabajar con objetos de fecha y hora, calcular diferencias de tiempo, formatear fechas y horas, y otras operaciones relacionadas con el tiempo y la fecha.

# Paso 1: Hacer una solicitud HTTP a la página de Wikipedia
url = "https://es.wikipedia.org/wiki/Anexo:Compañías_del_S%26P_500" #url de la pagina a extraer la tabla de datos
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
#headers: Esta es una estructura de datos que contiene información adicional que se envía junto con la solicitud HTTP. En este caso, se incluye un encabezado llamado 'User-Agent' que indica al servidor web qué tipo de navegador está realizando la solicitud. Esto puede ser útil para evitar bloqueos o restricciones basadas en el agente de usuario.
#es como una tarjeta de identificación que le dice al servidor web quién está haciendo la solicitud. navegador Chrome en una computadora con Windows. para evitar bots o limitaciones de descarga.
try:
    response = requests.get(url, headers=headers) # Aquí estamos utilizando la librería requests para enviar una solicitud HTTP GET a la URL especificada en la variable url. Además, estamos incluyendo los encabezados definidos en la variable headers en nuestra solicitud. Esto es importante para que el servidor web sepa qué tipo de solicitud estamos haciendo y cómo responder.
    response.raise_for_status()  #este método comprueba si la solicitud fue exitosa (código de estado HTTP 200).
    html = response.content      #aquí estamos guardando el contenido de la respuesta en la variable html. Esto es lo que recibimos del servidor web, que generalmente es el código HTML de la página solicitada.

except requests.exceptions.RequestException as e:  # aqui es si no se realizo el proceso correcto, sale un mesnaje de error.
    print(f"Error al realizar la solicitud HTTP: {e}")
    exit()

# Paso 2: Parsear el HTML y extraer la tabla de empresas
soup = BeautifulSoup(html, 'html.parser')#Aquí, estamos utilizando la librería BeautifulSoup para analizar el código HTML que recibimos como respuesta de la solicitud HTTP. 
#es un analizador de HTML que viene con BeautifulSoup y nos ayuda a estructurar y entender el código HTML
#"Parsear" en términos generales significa analizar o interpretar algo, desglosándolo en partes más pequeñas y comprensibles.
table = soup.find('table', {'class': 'wikitable sortable'})
# Con esta línea, estamos buscando en el código HTML (soup) una etiqueta <table> que tenga la clase 'wikitable sortable'. En Wikipedia, esta clase se usa comúnmente para las tablas que contienen datos. La función find() de BeautifulSoup nos permite buscar y seleccionar elementos específicos del código HTML en función de sus etiquetas y atributos.
if not table:
    print("No se encontró la tabla en la página web.")#este se genera si hay algun error en el proceso 
    exit()

companies = []  #Aquí estamos creando una lista vacía llamada companies. Esta lista se usará para almacenar los datos de las empresas que extraigamos de la tabla.
rows = table.find_all('tr')  # busca todas las etiquetas <tr> (filas) dentro de la tabla (table) que encontramos previamente. Esto nos da una lista de todas las filas de la tabla.
headers = [header.text.strip() for header in rows[0].find_all('th')] #comprensión de lista para obtener los encabezados de la tabla. rows[0] se refiere a la primera fila de la tabla (que generalmente es la fila de encabezados), y rows[0].find_all('th') busca todas las etiquetas <th> (celdas de encabezado) dentro de esa fila.

for row in rows[1:]:   #recorre todas las filas de la tabla, excepto la primera fila que contiene los encabezados. La sintaxis [1:] en rows[1:] significa que estamos empezando desde la segunda fila (índice 1) hasta el final de la lista de filas.
    cells = row.find_all('td') #estamos buscando todas las etiquetas <td> (celdas de datos) dentro de esa fila. Esto nos da una lista de todas las celdas de esa fila.
    company = [cell.text.strip() for cell in cells] #Utilizando una comprensión de lista, estamos obteniendo el texto dentro de cada celda de datos (cell.text.strip()) y eliminando cualquier espacio en blanco adicional alrededor del texto (usando .strip()). Esto nos da una lista de los datos de una empresa específica en esa fila.
    companies.append(company)  #Luego, agregamos la lista company (que contiene los datos de una empresa) a la lista companies. Esto se repite para cada fila de la tabla, por lo que al final, la lista companies contendrá una lista de listas, donde cada lista interna representa los datos de una empresa de la tabla.

# Creamos el DataFrame 
df = pd.DataFrame(companies, columns=headers) #crea un DataFrame de pandas con los datos de las empresas extraídos de la tabla HTML, utilizando los nombres de columna proporcionados en la variable headers. Esto facilita la manipulación y análisis posterior de los datos en un formato estructurado y tabular.

# Paso 3: Limpiar los datos de la lista de empresas
# Eliminar columnas innecesarias
columns_to_keep = ['Símbolo', 'Seguridad']  #elimino las columnas que considero que son innecesarias para su analisis
df = df[columns_to_keep] #esta línea de código se encarga de mantener solo las columnas relevantes en el DataFrame, lo que puede ser útil para reducir la cantidad de datos o enfocarse en características específicas durante el análisis de datos

# Renombrar columnas para mayor claridad
df.rename(columns={'Símbolo': 'Ticker', 'Seguridad': 'Company'}, inplace=True)
#esta línea de código renombra las columnas del DataFrame para hacer que los nombres de las columnas sean más claros y descriptivos, lo que facilita el análisis y la comprensión de los datos.
# Manejar valores faltantes (NaN)
df.dropna(inplace=True) #eliminamos las filas del DataFrame que contienen valores faltantes, lo que puede ser útil para limpiar y preparar los datos antes de realizar análisis o procesamientos adicionales.

# Mostrar el DataFrame limpio
print("Lista de empresas limpias:")
print(df)
# Guardar la lista de empresas transformada en un archivo CSV
df.to_csv('Lista_de_empresas_transformadas.csv', index=False, encoding='utf-8-sig') #estamos guardando el DataFrame df en un archivo CSV con el nombre especificado y utilizando la codificación UTF-8 para garantizar la integridad de los caracteres especiales.

# Paso 4: Obtener precios de cotización de cada empresa desde Yahoo Finance
# Definir el rango de fechas para el último trimestre
end_date = datetime.datetime.today() #Esta línea de código utiliza la librería datetime para obtener la fecha y hora actuales del sistema en el momento en que se ejecuta el código. La función datetime.today() devuelve un objeto datetime que representa la fecha y hora actuales.
start_date = end_date - pd.DateOffset(months=3) #En esta línea, estamos calculando la fecha de inicio restando 3 meses a la fecha de finalización (end_date). Utilizamos pd.DateOffset(months=3) de pandas para restar 3 meses al objeto end_date. Esto nos da una nueva fecha que es 3 meses antes de la fecha actual.

# Lista para guardar datos de cada empresa
price_data = []

# Obtener los precios de cierre para cada empresa
for ticker in df['Ticker']: #itera a través de cada valor en la columna 'Ticker' del DataFrame df. Cada valor representa el símbolo de ticker de una empresa.
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date) #finance (yf) para descargar los datos de precios de acciones para el símbolo de ticker actual (ticker). Los datos se descargan en el rango de fechas especificado por start_date y end_date. Los datos descargados se almacenan en stock_data.
        stock_data['Ticker'] = ticker #tabla de datos llamada stock_data que tiene diferentes columnas como 'Fecha', 'Precio', 'Volumen', etc. La línea de código en cuestión agrega una nueva columna llamada 'Ticker' a esta tabla y le asigna el valor de ticker a cada fila de esa columna. genera etiquetas a cada empresa de la tabla
        price_data.append(stock_data[['Close', 'Ticker']]) #simplemente toma un grupo de datos que tiene el precio de cierre y el símbolo de la empresa, y lo agrega a nuestra lista price_data. Esto se repite para cada grupo de datos de cada empresa, y al final tendremos una lista price_data que contiene todos estos grupos de datos juntos para su análisis posterior.
         
        #mostrar error si algo sale mal
    except Exception as e:
        print(f"Error al descargar datos para {ticker}: {e}")

# Concatenar todos los datos en un solo DataFrame
price_df = pd.concat(price_data) #Esto toma todos esos conjuntos de datos que están en la lista price_data y los une todos juntos en un solo conjunto de datos grande. Es como si estuviéramos combinando todas las hojas de cálculo en un solo archivo enorme.

# Resetear el índice para que sea un índice simple
price_df.reset_index(inplace=True) #tendrá un nuevo índice más ordenado y claro, lo que facilita el trabajo con los datos y su análisis.

# Paso 5: Limpiar los datos de los precios de las empresas
# Seleccionar solo las columnas relevantes (Date, Ticker, Close)
price_df = price_df[['Date', 'Ticker', 'Close']]

# Estandarizar los formatos de datos (e.g., fechas, números)
price_df['Date'] = pd.to_datetime(price_df['Date'])
price_df['Close'] = price_df['Close'].astype(float)

# Mostrar el DataFrame limpio con precios de cotización
print("Datos de precios de cotización limpios:")
print(price_df)

# Guardar los precios de las empresas transformados en un archivo CSV
price_df.to_csv('Precios_de_las_empresas_transformadas.csv', index=False, encoding='utf-8-sig')

