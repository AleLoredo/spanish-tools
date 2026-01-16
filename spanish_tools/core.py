from __future__ import annotations
import pathlib
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    import pandas as pd

from .normalization import clean_header
from .cleaning import clean_string

def load_data(
    ruta_archivo: str,
    separador: str = ';',
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    Loads a file (CSV or Excel) and normalizes its headers and content encoding.

    1.  Detects file type (.csv, .xls, .xlsx).
    2.  Sets defaults for Spanish formats (CSV: sep=';', decimal=',').
    3.  Fixes mojibake in all text columns automatically.
    4.  Cleans column names to 'snake_case'.

    Args:
        ruta_archivo (str): Path to the file.
        separador (str): Delimiter for CSV (default: ';'). Ignored for Excel.
        **kwargs: Standard pandas arguments passed to read_csv or read_excel.

    Returns:
        pd.DataFrame | None: Loaded DataFrame with clean headers.
    """
    try:
        import pandas as pd
    except ImportError:
        print("❌ Error: Pandas not installed. This function requires pandas.")
        return None

    ruta_path = pathlib.Path(ruta_archivo)
    extension = ruta_path.suffix.lower()
    
    print(f"1. Loading '{ruta_path.name}'...")
    
    try:
        if extension in ['.xls', '.xlsx']:
            # Excel Loader
            df = pd.read_excel(str(ruta_path), **kwargs)
        else:
            # CSV Loader (Default)
            # 1. Regional Configuration
            localizacion_kwargs = {
                'sep': separador,
                'decimal': ',', 
                'thousands': '.',
                'encoding': 'utf8',
            }
            config_final = {**localizacion_kwargs, **kwargs}
            df = pd.read_csv(str(ruta_path), **config_final)
            
    except FileNotFoundError:
        print(f"❌ Error: File not found: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

    # 2. Fix Mojibake in Content (Global Fix)
    # We apply this to all string columns to ensure correct encoding
    # WITHOUT normalizing or changing case in the content.
    from .cleaning import fix_mojibake
    
    for col in df.select_dtypes(include=['object', 'string']):
        df[col] = df[col].apply(fix_mojibake)

    # 3. Header Cleaning
    nombre_columnas_map = {col: clean_header(col) for col in df.columns}
    df.rename(columns=nombre_columnas_map, inplace=True)
    print("✅ Load complete. Mojibake fixed globally. Headers normalized.")
    return df

def clean_text(
    df: pd.DataFrame, 
    fields: List[str] | str,
    remove_accents: bool = True,
    **kwargs
) -> pd.DataFrame:
    """
    Cleans and normalizes text columns in an existing DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to clean.
        fields (List[str] | str): Columns to clean. 
                                  - List of column names (already normalized).
                                  - "all" to clean all columns.
        remove_accents (bool): Removes accents if True.
        **kwargs: Ignored arguments (kept for compatibility/flexibility).

    Returns:
        pd.DataFrame: The same DataFrame with clean text.
    """
    # Lightweight copy to avoid unexpected mutation if user doesn't want it (though we operate in-place mostly)
    
    if fields == "all":
        cols_to_clean = df.columns.tolist()
    elif isinstance(fields, list):
        # Validate existence
        cols_to_clean = [c for c in fields if c in df.columns]
        missing = set(fields) - set(df.columns)
        if missing:
            print(f"⚠️ Columns not found: {missing}")
    else:
        print("❌ Error: 'fields' must be a list or 'all'.")
        return df

    count = 0
    for col in cols_to_clean:
        # Simple type check
        # Apply astype(str) for robustness
        df[col] = df[col].astype(str).apply(
            lambda x: clean_string(x, remove_accents=remove_accents)
        )
        count += 1
    
    print(f"✨ Clean text in {count} columns.")
    return df

