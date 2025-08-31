import requests
import os
from datetime import datetime
def descargar_archivo(url, ruta_archivo):
    try:
        # Hacer la petición
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lanza error si hay código 4xx/5xx

       
        # Descargar el archivo
        with open(ruta_archivo, 'wb') as archivo:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    archivo.write(chunk)
        
        print(f"Archivo descargado: {ruta_archivo}")
        print(f"Tamaño: {response.headers.get('Content-Length', 'Desconocido')} bytes")
        print(f"Tipo: {response.headers.get('Content-Type', 'Desconocido')}")
        
        return ruta_archivo
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar: {e}")
        return None    