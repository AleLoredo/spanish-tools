import unicodedata

from .cleaning import fix_mojibake

def clean_header(texto: str) -> str:
    """
    Normalizes a text string for use as a column name (header).
    Performs the following transformations:
    1. Fixes Mojibake (Encoding errors).
    2. Removes accents, diereses, and transforms 'ñ' (using NFD Normalization).
    3. Converts everything to lowercase.
    4. Replaces spaces, hyphens, and non-alphanumeric characters with underscores ('_').
    5. Removes duplicate, leading, or trailing underscores.

    Args:
        texto (str): The original header string (e.g., "Año-Región (Sur)").
    
    Returns:
        str: The clean string in snake_case (e.g., "ano_region_sur").
    """
    # 0. Fix Mojibake (Encoding errors)
    texto = fix_mojibake(texto)

    # 1. NFD Normalization: Decomposes accented characters into 
    #    base character + combining character.
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # 2. Remove diacritics (accent marks)
    #    Filter only if the character is not a non-spacing mark ('Mn')
    texto_sin_acentos = ''.join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
    
    # 3. Convert to lowercase
    texto_final = texto_sin_acentos.lower()
    
    # 4. Replace unwanted characters with a temporary placeholder, 
    #    except letters, numbers, and underscores (which we will include).
    
    # Replace problematic characters with '_'
    for char in [' ', '-', '(', ')', '/', '\\', '[', ']', '.', ',', '¿', '?']:
        texto_final = texto_final.replace(char, '_')

    # 5. Remove any character that is not alphanumeric or underscore
    texto_snake = ''.join(
        c if c.isalnum() or c == '_' else '' for c in texto_final
    )
    
    # 6. Remove duplicate underscores (__) and leading/trailing underscores
    while '__' in texto_snake:
        texto_snake = texto_snake.replace('__', '_')
    
    return texto_snake.strip('_') # Removes leading/trailing '_'

