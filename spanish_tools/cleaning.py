"""
Module for cleaning Spanish text.
"""
import unicodedata
import string


def fix_mojibake(text: str) -> str:
    """
    Fixes common UTF-8 encoding errors (mojibake).
    Example: 'Ã±' -> 'ñ', 'Ã¡' -> 'á'
    """
    if not isinstance(text, str):
        return text
        
    try:
        # Generic heuristic: encode latin1, decode utf-8
        # This fixes the most common double-encoding issues in Spanish
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If it fails, it means it's likely already correct or a different issue
        return text

def clean_string(texto: str, remove_accents: bool = True) -> str:
    """
    Cleans and normalizes a text string within a data cell.

    Args:
        texto (str): The text value of the cell to clean.
        remove_accents (bool): If True (default), removes accents, 
                               diereses, and transforms 'ñ'. If False, 
                               only normalizes the text (useful for maintaining 
                               correct spelling).
    
    Returns:
        str: The clean text string, without extra spaces and in lowercase.
    """
    if not isinstance(texto, str):
        # Handling non-string values (e.g., NaN, numbers treated as text)
        return texto 

    # 0. Fix Mojibake (Encoding errors)
    texto = fix_mojibake(texto)
    
    # 1. Unicode Normalization: Ensures accented characters have a consistent representation. (NFC is most common)
    texto_limpio = unicodedata.normalize('NFC', texto)
    
    # 2. Remove accents if required
    if remove_accents:
        # NFD Normalization: Decomposes (e.g., 'á' -> 'a' + accent)
        texto_nfd = unicodedata.normalize('NFD', texto_limpio)
        
        # Filter characters: Ignore non-spacing marks ('Mn')
        texto_sin_acentos = ''.join(
            c for c in texto_nfd if unicodedata.category(c) != 'Mn'
        )
        texto_limpio = texto_sin_acentos

    # 3. Remove punctuation (often noise in cells)
    # Using str.maketrans for efficient removal
    # string.punctuation doesn't include ¿ or ¡, so we add them manually
    puntuacion_extra = '¿¡'
    tabla_puntuacion = str.maketrans('', '', string.punctuation + puntuacion_extra)
    texto_limpio = texto_limpio.translate(tabla_puntuacion)
    
    # 4. Convert to lowercase and standardize spaces
    # This guarantees consistency: "  Madrid " -> "madrid"
    texto_limpio = texto_limpio.lower().strip()
    
    # 5. Standardize multiple spaces to single space
    texto_limpio = ' '.join(texto_limpio.split())
    
    return texto_limpio
