import pathlib
from urllib import request
from urllib.error import URLError, HTTPError
import os
import os

def asegurar_directorio(ruta_destino: str):
    """
    Comprueba si el directorio de destino existe. Si no existe, lo crea 
    incluyendo los directorios intermedios necesarios.

    Args:
        ruta_destino (str): La ruta completa del directorio que se desea asegurar.
    """
    try:
        # Usa pathlib, parte de la librería estándar de Python
        directorio = pathlib.Path(ruta_destino)
        directorio.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio asegurado: '{ruta_destino}'")
    except Exception as e:
        print(f"❌ Error al intentar crear el directorio '{ruta_destino}': {e}")
        # Si la creación falla por permisos u otra razón crítica, es mejor fallar
        raise

def descargar_archivo(url: str, nombre_archivo: str, subcarpeta_destino: str = 'data') -> str | None:
    """
    Descarga un archivo desde una URL y lo guarda en una subcarpeta 
    dentro del directorio de trabajo actual, utilizando solo librerías estándar.

    Args:
        url (str): La URL del recurso a descargar.
        nombre_archivo (str): El nombre que se desea ponerle al archivo 
                              (incluyendo la extensión, ej: 'datos.csv').
        subcarpeta_destino (str): El nombre de la subcarpeta donde se almacenará 
                                  el archivo ('data' por defecto).
    
    Returns:
        str | None: La ruta completa del archivo descargado, o None si falla.
    """
    # 1. Definir rutas
    ruta_base = pathlib.Path.cwd()
    ruta_directorio = ruta_base / subcarpeta_destino
    ruta_completa_archivo = ruta_directorio / nombre_archivo

    # 2. Asegurar que el directorio exista
    try:
        asegurar_directorio(str(ruta_directorio))
    except Exception:
        # Si asegurar el directorio falla, no podemos continuar.
        return None 
    
    print(f"Iniciando descarga de {url}...")
    
    try:
        # 3. Descarga usando urllib.request.urlretrieve
        # Esto descarga el contenido de la URL y lo guarda directamente en el archivo
        request.urlretrieve(url, str(ruta_completa_archivo))

        print(f"✅ Descarga completada. Archivo guardado en: '{ruta_completa_archivo}'")
        return str(ruta_completa_archivo)
        
    except HTTPError as e:
        # Errores específicos de HTTP (404, 500, etc.)
        print(f"❌ Error HTTP al descargar (Código {e.code}): {e.reason}")
        return None
    except URLError as e:
        # Errores de URL o de red (URL incorrecta, fallo de conexión)
        print(f"❌ Error de URL o red: {e.reason}")
        return None
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado al descargar o guardar: {e}")
        return None





def ayuda_spa_text_utils():
    """
    Muestra la documentación completa de las funciones disponibles en la librería 
    spa_text_utils, incluyendo su definición y ejemplos de uso.
    """
    
    documentacion = """
============================================================
📚 Documentación de spa_text_utils para Análisis en Español
============================================================

Esta librería ofrece herramientas esenciales para la preparación de datos 
en español, centrándose en la gestión de archivos, codificación y 
normalización de texto (tildes, eñes, formatos).

---
### 1. Gestión de Archivos y Directorios
---

### 1.1. asegurar_directorio(ruta_destino: str)
------------------------------------------------------------
> **Definición:** Garantiza que un directorio exista. Si no existe, lo crea 
> recursivamente (crea carpetas intermedias si es necesario). 
> Esta función es la base de 'descargar_archivo'.
> **Dependencias:** Solo módulos estándar (pathlib).

* **Parámetros:**
    * `ruta_destino` (str): La ruta completa del directorio a asegurar.
* **Ejemplo de Uso:**
    
    >>> asegurar_directorio('mis_proyectos/data/raw')
    ✅ Directorio asegurado: 'mis_proyectos/data/raw'

------------------------------------------------------------
### 1.2. descargar_archivo(url: str, nombre_archivo: str, subcarpeta_destino: str = 'data')
------------------------------------------------------------
> **Definición:** Descarga un archivo desde una URL usando la biblioteca estándar 
> de Python (urllib.request) y lo guarda en la ubicación especificada, 
> asegurando primero la existencia de la carpeta destino.
> **Dependencias:** Solo módulos estándar (urllib.request, pathlib).

* **Parámetros:**
    * `url` (str): URL del archivo.
    * `nombre_archivo` (str): Nombre deseado para el archivo guardado (ej. 'datos.csv').
    * `subcarpeta_destino` (str): Carpeta dentro del directorio de trabajo (por defecto 'data').
* **Ejemplo de Uso:**

    >>> url_data = 'https://ejemplo.com/reporte.csv'
    >>> ruta = descargar_archivo(url_data, 'reporte_2024.csv', 'datasets_espanol')
    ✅ Descarga completada. Archivo guardado en: '.../datasets_espanol/reporte_2024.csv'

---
### 2. Normalización de Texto (Tildes, Eñes, Formato)
---

### 2.1. limpiar_cabeceras_string(texto: str)
------------------------------------------------------------
> **Definición:** Normaliza una cadena de texto para convertirla en una cabecera 
> segura para análisis ('snake_case'). Elimina tildes/eñes, convierte a minúsculas, 
> y reemplaza espacios o caracteres especiales por guiones bajos.
> **Dependencias:** Solo módulos estándar (unicodedata).

* **Parámetros:**
    * `texto` (str): La cabecera original (ej. "Año Contratación (Pública)").
* **Ejemplo de Uso:**
    
    >>> cabecera = "Región de Distribución - Nº"
    >>> limpiar_cabeceras_string(cabecera)
    'region_de_distribucion_n'

----------------------------------------------------------------------
### 2.2. convertir_a_float_es(valor: str | float | int)
----------------------------------------------------------------------
> **Definición:** Convierte una cadena con formato numérico español (1.234,56) 
> a un float de Python. Maneja separadores de miles (punto) y decimales (coma).
> **Dependencias:** Ninguna.

* **Parámetros:**
    * `valor` (str | float | int): El valor a convertir.
* **Ejemplo de Uso:**
    
    >>> convertir_a_float_es("1.500,50")
    1500.5

    >>> convertir_a_float_es("1.500,50")
    1500.5

----------------------------------------------------------------------
### 2.3. convertir_a_fecha_es(fecha_str: str, formato: str = '%d/%m/%Y')
----------------------------------------------------------------------
> **Definición:** Convierte una cadena de texto a datetime, asumiendo formato 
> D/M/A por defecto.
> **Dependencias:** datetime.

* **Parámetros:**
    * `fecha_str` (str): Fecha en texto (ej. '15/05/2024').
    * `formato` (str): Formato esperado (default '%d/%m/%Y').
* **Ejemplo de Uso:**
    
    >>> convertir_a_fecha_es("15/05/2024")
    datetime.datetime(2024, 5, 15, 0, 0)

------------------------------------------------------------
### 2.4. limpiar_celda_texto(texto: str, quitar_acentos: bool = True)
------------------------------------------------------------
> **Definición:** Limpia y normaliza los valores de texto dentro de un dataset. 
> Estandariza espacios, convierte a minúsculas y, opcionalmente, elimina tildes/eñes 
> para asegurar la consistencia en el análisis y conteo de valores.
> **Dependencias:** Solo módulos estándar (unicodedata, string).

* **Parámetros:**
    * `texto` (str): Valor de la celda (ej. "  PERÚ ").
    * `quitar_acentos` (bool): `True` para quitar acentos (por defecto); `False` para mantener la ortografía.
* **Ejemplo de Uso:**
    
    >>> texto_con_espacios = " País: MÉXICO "
    >>> limpiar_celda_texto(texto_con_espacios, quitar_acentos=False)
    'país méxico'
    
    >>> limpiar_celda_texto(texto_con_espacios, quitar_acentos=True)
    'pais mexico'

---
### 3. Carga de Datos
---

### 3.1. cargar_csv_es(ruta_archivo: str, separador: str = ';', **kwargs)
------------------------------------------------------------
> **Definición:** Carga un CSV con configuración regional española (coma decimal, 
> punto y coma como separador).
> **Dependencias:** pandas.

* **Parámetros:**
    * `ruta_archivo` (str): Ruta del CSV.
    * `separador` (str): Delimitador (default ';').
    * `**kwargs`: Argumentos extra para pd.read_csv.
* **Ejemplo de Uso:**
    
    >>> df = cargar_csv_es('datos.csv')
    ✅ Archivo 'datos.csv' cargado con éxito. Filas: 100

### 3.2. procesar_csv_es(ruta_archivo: str, columnas_texto_a_limpiar: list[str] = None, separador: str = ';', quitar_acentos: bool = True, **kwargs)
------------------------------------------------------------
> **Definición:** Pipeline integral que carga un CSV, limpia cabeceras (snake_case) 
> y normaliza columnas de texto específicas.
> **Dependencias:** pandas.

* **Parámetros:**
    * `ruta_archivo` (str): Ruta del CSV.
    * `columnas_texto_a_limpiar` (list[str]): Lista de columnas a limpiar.
    * `separador` (str): Delimitador (default ';').
    * `quitar_acentos` (bool): Eliminar acentos en texto (default True).
* **Ejemplo de Uso:**
    
    >>> df = procesar_csv_es('datos.csv', columnas_texto_a_limpiar=['Comentarios'])
    1. Iniciando carga localizada...
    2. Cabeceras limpiadas...
    3. Limpieza de texto aplicada...
    ✅ Proceso integral completado.

============================================================
    """
    
    print(documentacion)

