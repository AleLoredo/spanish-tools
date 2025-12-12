# spa_text_utils

A Python library designed to handle the complexities of working with Spanish text data.

## Features

- **Cleaning**: Tools to remove accents, handle special characters, and clean text.
- **Normalization**: Spanish-specific text normalization.
- **Analysis**: Tools for analyzing Spanish text.

## Installation

```bash
pip install spa_text_utils
```

## Instalación en Google Colab

Para instalar la última versión directamente desde GitHub:

```python
!pip install git+https://github.com/tu_usuario/spa-text-utils.git
```

Si vas a utilizar las funciones de CSV (que requieren pandas), asegúrate de tener pandas instalado (Colab ya lo incluye por defecto).


## Usage

```python
import spa_text_utils

# Example usage (coming soon)
```

## Referencia de la API

### Gestión de Archivos y Directorios (`spa_text_utils.utils`)

*   `asegurar_directorio(ruta_destino: str)`
    *   Crea un directorio y sus padres si no existen.
    ```python
    from spa_text_utils.utils import asegurar_directorio
    asegurar_directorio("datos/procesados/2024")
    ```

*   `descargar_archivo(url: str, nombre_archivo: str, subcarpeta_destino: str = 'data') -> str | None`
    *   Descarga un archivo desde una URL a una carpeta local.
    ```python
    from spa_text_utils.utils import descargar_archivo
    ruta = descargar_archivo("https://ejemplo.com/data.csv", "datos.csv")
    ```

### Carga y Procesamiento de Datos (`spa_text_utils.io`)

*   `cargar_csv_es(ruta_archivo: str, separador: str = ';', **kwargs) -> Optional[pd.DataFrame]`
    *   Carga un CSV con configuración regional española (decimal=',', miles='.').
    ```python
    from spa_text_utils.io import cargar_csv_es
    df = cargar_csv_es("ventas_espana.csv")
    ```

*   `procesar_csv_es(ruta_archivo: str, columnas_texto_a_limpiar: List[str] = None, separador: str = ';', quitar_acentos: bool = True, **kwargs) -> Optional[pd.DataFrame]`
    *   Pipeline completo: carga CSV, limpia cabeceras y normaliza columnas de texto.
    ```python
    from spa_text_utils.io import procesar_csv_es
    df = procesar_csv_es("comentarios.csv", columnas_texto_a_limpiar=["Opinion_Cliente"])
    ```

### Normalización (`spa_text_utils.normalization`)

*   `limpiar_cabeceras_string(texto: str) -> str`
    *   Convierte texto a `snake_case` (minúsculas, sin acentos, guiones bajos).
    ```python
    from spa_text_utils.normalization import limpiar_cabeceras_string
    print(limpiar_cabeceras_string("Fecha de Creación")) # "fecha_de_creacion"
    ```

*   `convertir_a_float_es(valor: str | float | int) -> float | None`
    *   Convierte strings numéricos españoles ("1.234,56") a float.
    ```python
    from spa_text_utils.normalization import convertir_a_float_es
    print(convertir_a_float_es("1.500,50")) # 1500.5
    ```

*   `convertir_a_fecha_es(fecha_str: str, formato: str = '%d/%m/%Y') -> datetime | None`
    *   Convierte texto a objeto datetime.
    ```python
    from spa_text_utils.normalization import convertir_a_fecha_es
    print(convertir_a_fecha_es("31/12/2023")) # datetime(2023, 12, 31, 0, 0)
    ```

### Limpieza (`spa_text_utils.cleaning`)

*   `limpiar_celda_texto(texto: str, quitar_acentos: bool = True) -> str`
    *   Normaliza texto de celdas: minúsculas, espacios, puntuación y acentos (opcional).
    ```python
    from spa_text_utils.cleaning import limpiar_celda_texto
    print(limpiar_celda_texto("  HOLA MUNDO!  ")) # "hola mundo"
    ```

*   `remove_accents(text)`
    *   Elimina acentos de un texto.
    ```python
    from spa_text_utils.cleaning import remove_accents
    print(remove_accents("camión")) # "camion"
    ```

*   `clean_text(text)`
    *   Limpieza básica de texto.
    ```python
    from spa_text_utils.cleaning import clean_text
    print(clean_text("Texto sucio..."))
    ```

### Ayuda

*   `ayuda_spa_text_utils()`
    *   Imprime la documentación completa y ejemplos de uso en la consola.
    ```python
    from spa_text_utils.utils import ayuda_spa_text_utils
    ayuda_spa_text_utils()
    ```
