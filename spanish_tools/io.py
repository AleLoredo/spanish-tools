from __future__ import annotations
import pathlib
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    import pandas as pd

from .normalization import limpiar_cabeceras_string
from .cleaning import limpiar_celda_texto

def procesar_csv_es(
    ruta_archivo: str, 
    columnas_texto_a_limpiar: List[str] = None, 
    separador: str = ';', 
    quitar_acentos: bool = True, 
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    Función integral que automatiza la carga y limpieza de un dataset CSV 
    con localización en español.

    Realiza la carga localizada, la limpieza de cabeceras, y la normalización 
    de texto en las columnas especificadas.

    Args:
        ruta_archivo (str): La ruta completa del archivo CSV.
        columnas_texto_a_limpiar (list[str]): Nombres de las columnas de texto 
                                              a las que se aplicará limpiar_celda_texto. 
                                              Se usan los nombres originales de las columnas.
                                              Por defecto es None (no se limpian cuerpos de texto).
        separador (str): El delimitador de campos (por defecto ';').
        quitar_acentos (bool): Si es True, elimina tildes/eñes en los cuerpos de texto 
                               (True por defecto).
        **kwargs: Argumentos adicionales que se pasan directamente a pd.read_csv.
    
    Returns:
        pd.DataFrame | None: El DataFrame limpio y procesado, o None si hay error.
    """
    try:
        import pandas as pd
    except ImportError:
        print("❌ Error: Pandas no está instalado. Esta función requiere pandas.")
        return None
    
    # 1. CARGA LOCALIZADA
    # Configuración por defecto para CSVs españoles
    localizacion_kwargs = {
        'sep': separador,
        'decimal': ',', 
        'thousands': '.',
        'encoding': 'utf8',
    }
    # Combinar con kwargs del usuario (usuario manda)
    config_final = {**localizacion_kwargs, **kwargs}
    
    ruta_path = pathlib.Path(ruta_archivo)
    print(f"1. Iniciando carga localizada de '{ruta_path.name}'...")
    
    try:
        df = pd.read_csv(str(ruta_path), **config_final)
    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return None

    # 2. LIMPIEZA DE CABECERAS
    # Crear el mapeo de nombres (Original -> Limpio)
    nombre_columnas_map = {col: limpiar_cabeceras_string(col) for col in df.columns}
    df.rename(columns=nombre_columnas_map, inplace=True)
    print("2. Cabeceras limpiadas y convertidas a snake_case.")
    
    # 3. LIMPIEZA DE CUERPOS DE TEXTO
    if columnas_texto_a_limpiar:
        # Obtener los nombres limpios que coinciden con las columnas a limpiar
        nombres_limpios_a_limpiar = [
            nombre_columnas_map.get(col_original) 
            for col_original in columnas_texto_a_limpiar 
            if col_original in nombre_columnas_map # Asegura que la columna original exista
        ]
        
        if not nombres_limpios_a_limpiar:
             print("⚠️ Advertencia: Ninguna de las columnas especificadas para limpieza de texto fue encontrada.")
        
        for col_limpia in nombres_limpios_a_limpiar:
            # Aplicamos la función atómica de limpieza de texto
            # Usar .astype(str) asegura que manejamos NaNs como 'nan' o fallos silent
            df[col_limpia] = df[col_limpia].astype(str).apply(
                lambda x: limpiar_celda_texto(x, quitar_acentos=quitar_acentos)
            )
        print(f"3. Limpieza de texto aplicada a {len(nombres_limpios_a_limpiar)} columna(s).")
    
    print("✅ Proceso integral completado.")
    return df

