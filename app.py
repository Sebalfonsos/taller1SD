from flask import Flask, render_template, request, jsonify
from datetime import datetime
from descargar import descargar_archivo
import os
import xml.etree.ElementTree as ET
from queue import Queue
import multiprocessing as mp
import json
from sanitizar import sanitizar_nombre_archivo


with open("config.json", "r") as f:
    config = json.load(f)
numero_procesos = config["num_procesos"]

app = Flask(__name__)

contador = mp.Value('i', 0)  # entero compartido
lock = mp.Lock()

# Función que procesará cada elemento de la cola
def procesar_entrada(item, contador, lock):
    """Función que será ejecutada por cada proceso para procesar una entrada"""
    pid = os.getpid()
    
    # Sanitizar el nombre del archivo antes de usarlo
    nombre_archivo_sanitizado = sanitizar_nombre_archivo(item['titulo'])
    ruta_destino = os.path.join(item['rutacarpeta'], nombre_archivo_sanitizado)
    
    print(f"[PID: {pid}] Ruta: {ruta_destino}")
    
    # Pasar tanto la URL como el nombre del archivo a la función de descarga
    descargar_archivo(item['pdf_url'], ruta_destino)
    with lock:  # evitar condiciones de carrera
        contador.value += 1
    return True

@app.route('/progreso')
def obtener_progreso():
    return jsonify({"total_procesados": contador.value})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def recibir_datos():
    try:
        # Obtener el texto del formulario
        texto = request.form.get('texto_input')
        
        if texto:
            print(f"Texto recibido: {texto}")
            
            url = f"https://export.arxiv.org/api/query?search_query=all:{texto}&start=300&max_results=300"
            ahora = datetime.now()
            fecha_str = ahora.strftime("%Y%m%d_%H%M%S")
            nombreArchivo = f"busqueda_{texto}_{fecha_str}.xml"

            carpeta_base = "downloads"
            fecha_hora = datetime.now().strftime(f"{texto}-%Y-%m-%d_%H-%M-%S")
            carpeta_destino = os.path.join(carpeta_base, fecha_hora)
            os.makedirs(carpeta_destino, exist_ok=True)
            ruta_archivo = os.path.join(carpeta_destino, nombreArchivo)
            descargar_archivo(url, ruta_archivo)

            # Parsear el XML
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            # El XML usa namespaces, hay que definirlos
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            # Crear una cola
            cola = Queue()

            for entry in root.findall('atom:entry', ns):
                titulo = entry.find('atom:title', ns).text.strip()
                fecha = entry.find('atom:published', ns).text.strip()
                resumen = entry.find('atom:summary', ns).text.strip()
                
                # Autores
                autores = [a.find('atom:name', ns).text.strip() 
                        for a in entry.findall('atom:author', ns)]
                
                # Categorías (puede haber varias)
                categorias = [c.attrib['term'] for c in entry.findall('atom:category', ns)]
                
                # URL del PDF
                pdf_url = None
                for link in entry.findall('atom:link', ns):
                    if link.attrib.get('title') == 'pdf':
                        pdf_url = link.attrib['href']
                        break
                
                # Guardar todo en la cola como un diccionario
                cola.put({
                    "rutacarpeta": carpeta_destino,
                    "titulo": titulo,
                    "autores": autores,
                    "fecha_publicacion": fecha,
                    "categorias": categorias,
                    "resumen": resumen,
                    "pdf_url": pdf_url
                })

            with contador.get_lock():
                contador.value = 0  # Reiniciar contador
            # Contar cuántas entradas hay
            cantidadTotalEntradas = cola.qsize()
            print(f"Cantidad de entradas en la cola: {cantidadTotalEntradas}")

            # Procesar la cola con multiprocessing (máximo 3 procesos simultáneos)
            procesos = []
            max_procesos = numero_procesos
            
            # Extraer todos los elementos de la cola para procesarlos
            elementos = []
            while not cola.empty():
                elementos.append(cola.get())
            
            # Crear y ejecutar procesos
            for i, elemento in enumerate(elementos):
                if len(procesos) >= max_procesos:
                    # Esperar a que al menos un proceso termine antes de iniciar más
                    for p in procesos:
                        p.join()
                    procesos = []  # Reiniciar la lista de procesos
                
                # Crear y empezar un nuevo proceso
                p = mp.Process(target=procesar_entrada, args=(elemento, contador, lock))
                p.start()
                procesos.append(p)
            
            # Esperar a que todos los procesos terminen
            for p in procesos:
                p.join()
            
            return jsonify({
                'status': 'success',
                'message': 'Perfect',
                'texto': cantidadTotalEntradas
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'No se recibió texto'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error del servidor: {str(e)}'
        }), 500
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)