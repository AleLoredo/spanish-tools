"""
Module for cleaning Spanish text.
"""
import unicodedata
import string

def remove_accents(text):
    """
    Placeholder for removing accents from text.
    """
    pass

def clean_text(text):
    """
    Placeholder for general text cleaning.
    """
    pass

def limpiar_celda_texto(texto: str, quitar_acentos: bool = True) -> str:
    """
    Limpia y normaliza una cadena de texto dentro de una celda de datos.

    Args:
        texto (str): El valor de texto de la celda a limpiar.
        quitar_acentos (bool): Si es True (por defecto), elimina tildes, 
                               diéresis y transforma la ñ. Si es False, 
                               solo normaliza el texto (útil para mantener 
                               la ortografía correcta).
    
    Returns:
        str: La cadena de texto limpia, sin espacios extra y en minúsculas.
    """
    if not isinstance(texto, str):
        # Manejo de valores no string (ej. NaN, números que se tratan como texto)
        return texto 

    # 1. Normalización Unicode: Asegura que los caracteres acentuados 
    #    tengan una representación consistente. (NFC es la forma más común)
    texto_limpio = unicodedata.normalize('NFC', texto)
    
    # 2. Quitar acentos si se requiere
    if quitar_acentos:
        # Normalización NFD: Descompone (ej. 'á' -> 'a' + acento)
        texto_nfd = unicodedata.normalize('NFD', texto_limpio)
        
        # Filtrar caracteres: Ignora las marcas diacríticas ('Mn')
        texto_sin_acentos = ''.join(
            c for c in texto_nfd if unicodedata.category(c) != 'Mn'
        )
        texto_limpio = texto_sin_acentos

    # 3. Eliminar puntuación (a menudo es ruido en las celdas)
    # Se usa el método str.maketrans para una eliminación eficiente
    # string.punctuation no incluye ¿ ni ¡, así que los añadimos manualmente
    puntuacion_extra = '¿¡'
    tabla_puntuacion = str.maketrans('', '', string.punctuation + puntuacion_extra)
    texto_limpio = texto_limpio.translate(tabla_puntuacion)
    
    # 4. Convertir a minúsculas y estandarizar espacios
    # Esto garantiza consistencia: "  Madrid " -> "madrid"
    texto_limpio = texto_limpio.lower().strip()
    
    # 5. Estandarizar espacios múltiples a uno solo (si quedaron)
    texto_limpio = ' '.join(texto_limpio.split())
    
    return texto_limpio
