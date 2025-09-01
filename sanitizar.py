import re
import unicodedata

def sanitizar_nombre_archivo(nombre):
    """
    Sanitiza un nombre de archivo para que sea válido en Windows/Linux
    Remueve caracteres inválidos, normaliza y asegura extensión .pdf
    """
    # Normalizar caracteres Unicode (remover acentos, etc.)
    nombre = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('ASCII')
    
    # Remover caracteres inválidos para sistemas de archivos
    caracteres_invalidos = r'[<>:"/\\|?*\n\r\t]'
    nombre = re.sub(caracteres_invalidos, '_', nombre)
    
    # Remover caracteres de control
    nombre = re.sub(r'[\x00-\x1f\x7f-\x9f]', '_', nombre)
    
    # Reemplazar múltiples espacios y guiones bajos
    nombre = re.sub(r'[\s_]+', '_', nombre)
    
    # Remover puntos múltiples y puntos al inicio/final (excepto extensión)
    nombre = re.sub(r'\.+', '.', nombre)
    nombre = nombre.strip('._')
    
    # Limitar longitud (máximo 100 caracteres para el nombre)
    if len(nombre) > 100:
        # Mantener las primeras 95 caracteres y añadir hash
        import hashlib
        hash_suffix = hashlib.md5(nombre.encode()).hexdigest()[:8]
        nombre = nombre[:95] + '_' + hash_suffix
    
    
    return nombre