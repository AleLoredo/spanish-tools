import unicodedata

def limpiar_cabeceras_string(texto: str) -> str:
    """
    Normaliza una cadena de texto para usarla como nombre de columna (cabecera).
    Realiza las siguientes transformaciones:
    1. Elimina tildes, diéresis y transforma la ñ (usando Normalización NFD).
    2. Convierte todo a minúsculas.
    3. Reemplaza espacios, guiones y caracteres no alfanuméricos por guiones bajos ('_').
    4. Elimina guiones bajos duplicados o iniciales/finales.

    Args:
        texto (str): La cadena de texto de la cabecera original (ej. "Año-Región (Sur)").
    
    Returns:
        str: La cadena limpia en snake_case (ej. "ano_region_sur").
    """
    # 1. Normalización NFD: Descompone los caracteres acentuados en 
    #    carácter base + marca de acento.
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # 2. Quitar los diacríticos (marcas de acento)
    #    Se filtra solo si el carácter no es una marca diacrítica ('Mn')
    texto_sin_acentos = ''.join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
    
    # 3. Convertir a minúsculas
    texto_final = texto_sin_acentos.lower()
    
    # 4. Reemplazar caracteres no deseados por un espacio temporal, 
    #    excepto letras, números y guiones bajos (que ya incluiremos).
    #    Aquí se usa un enfoque simple con .replace(), ya que no queremos 
    #    depender de 're' (aunque 're' también es de la PSL).
    
    # Reemplazar caracteres problemáticos por '_'
    for char in [' ', '-', '(', ')', '/', '\\', '[', ']', '.', ',', '¿', '?']:
        texto_final = texto_final.replace(char, '_')

    # 5. Eliminar cualquier carácter que no sea alfanumérico o guion bajo
    texto_snake = ''.join(
        c if c.isalnum() or c == '_' else '' for c in texto_final
    )
    
    # 6. Eliminar guiones bajos duplicados (__) y guiones iniciales/finales
    while '__' in texto_snake:
        texto_snake = texto_snake.replace('__', '_')
    
    return texto_snake.strip('_') # Elimina el '_' inicial/final

def convertir_a_float_es(valor: str | float | int) -> float | None:
    """
    Convierte una cadena de texto con formato numérico español (coma decimal) 
    a un número flotante estándar de Python.

    Args:
        valor (str | float | int): El valor de la celda.
    
    Returns:
        float | None: El número flotante o None si la conversión falla.
    """
    # 1. Manejar entradas que ya son numéricas
    if isinstance(valor, (float, int)):
        return float(valor)
        
    if not isinstance(valor, str):
        # Si no es string ni número (ej. None, NaN), devuelve None
        return None

    # 2. Limpieza inicial del string
    texto_limpio = valor.strip()
    
    # 3. Sustitución de separadores:
    # Primero, eliminar el separador de miles (punto en español)
    texto_sin_miles = texto_limpio.replace('.', '')
    
    # Segundo, reemplazar el separador decimal (coma en español) por punto
    texto_float = texto_sin_miles.replace(',', '.')
    
    # 4. Intentar la conversión
    try:
        return float(texto_float)
    except ValueError:
        # La cadena no era un número válido (ej. tenía texto)
        return None

from datetime import datetime

def convertir_a_fecha_es(fecha_str: str, formato: str = '%d/%m/%Y') -> datetime | None:
    """
    Convierte una cadena de texto a un objeto datetime, asumiendo el formato 
    Día/Mes/Año o un formato explícito.

    Args:
        fecha_str (str): La cadena de texto de la fecha (ej. '15/05/2024').
        formato (str): El formato de fecha esperado, usando códigos strptime 
                       (por defecto '%d/%m/%Y' para D/M/A).
    
    Returns:
        datetime | None: El objeto datetime o None si la conversión falla.
    """
    if not isinstance(fecha_str, str):
        return None
        
    texto_limpio = fecha_str.strip()
    
    try:
        # Usamos strptime para parsear la fecha con el formato específico (D/M/A)
        return datetime.strptime(texto_limpio, formato)
    except ValueError:
        # Si el formato no coincide o la fecha no es válida
        return None
