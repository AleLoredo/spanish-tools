# Spanish Tools

[![PyPI version](https://img.shields.io/pypi/v/spanish-tools?color=blue)](https://pypi.org/project/spanish-tools/)
[![Python Version](https://img.shields.io/pypi/pyversions/spanish-tools)](https://pypi.org/project/spanish-tools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Spanish Tools** es una librería de Python diseñada específicamente para facilitar el análisis y procesamiento de datos en español. Resuelve problemas comunes como la codificación, formatos numéricos regionales (coma decimal), fechas y normalización de texto (tildes, eñes) de manera eficiente.

## 🚀 Instalación

### Instalación estándar (PyPI)
```bash
pip install spanish_tools
```

### Instalación en Google Colab
Para instalar la última versión de desarrollo directamente desde GitHub:
```python
!pip install git+https://github.com/AleLoredo/spanish-tools.git
```
> **Nota:** Si vas a utilizar las funciones de carga de CSV (`spanish_tools.io`), asegúrate de tener `pandas` instalado (incluido por defecto en Colab y Anaconda).

## ⚡ Inicio Rápido

Limpia y carga un dataset español desordenado en un solo paso:

```python
from spanish_tools.io import procesar_csv_es

# Carga un CSV con formato español (separador ';', decimal ',')
# y limpia automáticamente los nombres de las columnas.
df = procesar_csv_es(
    ruta_archivo="ventas_2024.csv", 
    columnas_texto_a_limpiar=["Comentarios", "Ciudad"]
)

# ¡Listo! Las columnas ahora son 'snake_case' (ej. 'Fecha Venta' -> 'fecha_venta')
# y el texto en 'comentarios' y 'ciudad' está normalizado.
print(df.head())
```

## ✨ Características Principales

*   **Carga de Datos Localizada**: Funciones para `pandas` pre-configuradas para formatos regionales de España/Latinoamérica (coma decimal, punto de miles).
*   **Normalización de Texto**: Herramientas robustas para eliminar acentos, manejar la 'ñ' y estandarizar mayúsculas/minúsculas.
*   **Limpieza de Cabeceras**: Convierte nombres de columnas "sucios" (con espacios, tildes, símbolos) a `snake_case` limpio y programable.
*   **Gestión de Archivos**: Utilidades para descargar archivos y asegurar estructuras de directorios.

## 📚 Referencia de la API

### 1. Carga y Procesamiento (`spanish_tools.io`)

#### `procesar_csv_es`
Pipeline "todo en uno" para cargar y limpiar datasets.
```python
def procesar_csv_es(
    ruta_archivo: str, 
    columnas_texto_a_limpiar: List[str] = None, 
    separador: str = ';', 
    quitar_acentos: bool = True, 
    **kwargs
) -> Optional[pd.DataFrame]
```
*   **ruta_archivo**: Ruta al archivo CSV.
*   **columnas_texto_a_limpiar**: Lista de nombres de columnas (originales) cuyo contenido de texto se debe normalizar.
*   **separador**: Delimitador del CSV (default: `;`).
*   **quitar_acentos**: Si es `True`, elimina tildes en el contenido de las columnas especificadas.

#### `cargar_csv_es`
Carga un CSV con configuración regional española (coma decimal).
```python
from spanish_tools.io import cargar_csv_es
df = cargar_csv_es("datos.csv", separador=";")
```

### 2. Normalización (`spanish_tools.normalization`)

#### `limpiar_cabeceras_string`
Convierte texto a formato `snake_case` ideal para nombres de variables o columnas.
```python
from spanish_tools.normalization import limpiar_cabeceras_string

print(limpiar_cabeceras_string("Año de Creación (2024)"))
# Salida: "ano_de_creacion_2024"
```

#### `convertir_a_float_es`
Convierte strings numéricos españoles a `float`.
```python
from spanish_tools.normalization import convertir_a_float_es

print(convertir_a_float_es("1.500,50"))
# Salida: 1500.5
```

#### `convertir_a_fecha_es`
Parsea fechas en formato español (dd/mm/aaaa).
```python
from spanish_tools.normalization import convertir_a_fecha_es

print(convertir_a_fecha_es("31/12/2023"))
# Salida: datetime.datetime(2023, 12, 31, 0, 0)
```

### 3. Limpieza de Texto (`spanish_tools.cleaning`)

#### `limpiar_celda_texto`
Limpieza atómica para una cadena de texto.
```python
from spanish_tools.cleaning import limpiar_celda_texto

texto = "  HOLA   MUNDO! "
print(limpiar_celda_texto(texto))
# Salida: "hola mundo"
```

### 4. Utilidades (`spanish_tools.utils`)

*   `descargar_archivo(url, nombre_archivo, subcarpeta_destino)`: Descarga archivos web fácilmente.
*   `asegurar_directorio(ruta)`: Crea directorios si no existen.
*   `ayuda_spanish_tools()`: Muestra la documentación interactiva en consola.

## 🤝 Contribuir
¡Las contribuciones son bienvenidas! Si encuentras un bug o tienes una idea para una nueva funcionalidad:
1.  Haz un Fork del repositorio.
2.  Crea una rama para tu feature (`git checkout -b feature/nueva-feature`).
3.  Haz Commit de tus cambios (`git commit -m 'Añadir nueva feature'`).
4.  Haz Push a la rama (`git push origin feature/nueva-feature`).
5.  Abre un Pull Request.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
