from __future__ import annotations
import pathlib
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    import pandas as pd

from .normalization import limpiar_cabeceras_string
from .cleaning import limpiar_celda_texto

def read_csv(
    ruta_archivo: str,
    separador: str = ';',
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    Carga un archivo CSV con configuración regional española y normaliza sus cabeceras.

    Es un wrapper "vitaminado" de pandas.read_csv que:
    1.  Configura decimales (',') y separadores (';') por defecto para España/Latam.
    2.  Limpia automáticamente los nombres de las columnas a 'snake_case'.

    Args:
        ruta_archivo (str): Ruta al archivo CSV.
        separador (str): Delimitador (default: ';').
        **kwargs: Argumentos estándar de pandas.read_csv (encoding, dtype, etc.).

    Returns:
        pd.DataFrame | None: DataFrame cargado con cabeceras limpias.
    """
    try:
        import pandas as pd
    except ImportError:
        print("❌ Error: Pandas no está instalado. Esta función requiere pandas.")
        return None

    # 1. Configuración Regional
    localizacion_kwargs = {
        'sep': separador,
        'decimal': ',', 
        'thousands': '.',
        'encoding': 'utf8',
    }
    config_final = {**localizacion_kwargs, **kwargs}
    
    ruta_path = pathlib.Path(ruta_archivo)
    print(f"1. Cargando '{ruta_path.name}'...")
    
    try:
        df = pd.read_csv(str(ruta_path), **config_final)
    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"❌ Error al cargar: {e}")
        return None

    # 2. Limpieza de Cabeceras
    nombre_columnas_map = {col: limpiar_cabeceras_string(col) for col in df.columns}
    df.rename(columns=nombre_columnas_map, inplace=True)
    print("✅ Carga completa. Cabeceras normalizadas.")
    return df

def clean_text(
    df: pd.DataFrame, 
    fields: List[str] | str,
    quitar_acentos: bool = True
) -> pd.DataFrame:
    """
    Limpia y normaliza columnas de texto en un DataFrame existente.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        fields (List[str] | str): Columnas a limpiar. 
                                  - Lista de nombres de columnas (ya normalizadas).
                                  - "all" para limpiar todas las columnas.
        quitar_acentos (bool): Elimina tildes si es True.

    Returns:
        pd.DataFrame: El mismo DataFrame con los textos limpios.
    """
    # Copia ligera para no mutar el original inesperadamente si el usuario no quiere
    # Aunque en pandas es común mutar, es más seguro retornar una referencia o copia.
    # Por eficiencia en dataframes grandes, operaremos in-place pero retornamos 'df' para chaining.
    # Decisión: Operar sobre el objeto pasado para eficiencia, data science style.
    
    if fields == "all":
        cols_to_clean = df.columns.tolist()
    elif isinstance(fields, list):
        # Validar que existan
        cols_to_clean = [c for c in fields if c in df.columns]
        missing = set(fields) - set(df.columns)
        if missing:
            print(f"⚠️ Columnas no encontradas: {missing}")
    else:
        print("❌ Error: 'fields' debe ser una lista o 'all'.")
        return df

    count = 0
    for col in cols_to_clean:
        # Check simple de tipo
        # Aplicamos astype(str) para robustez
        df[col] = df[col].astype(str).apply(
            lambda x: limpiar_celda_texto(x, quitar_acentos=quitar_acentos)
        )
        count += 1
    
    print(f"✨ Texto limpio en {count} columnas.")
    return df

