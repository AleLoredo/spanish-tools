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

