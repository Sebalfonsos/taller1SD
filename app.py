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
max_procesos = config["num_procesos"]

app = Flask(__name__)

contador = mp.Value('i', 0)  # entero compartido
lock = mp.Lock()
elementos = []
procesos = []
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

def lanzar_procesos(elementos, contador, lock):
    procesos = []
    for elemento in elementos:
        if len(procesos) >= max_procesos:
            procesos[0].join()  # esperar que al menos uno termine
            procesos.pop(0)

        p = mp.Process(target=procesar_entrada, args=(elemento, contador, lock))
        p.start()
        procesos.append(p)

    # esperar a que todos terminen
    for p in procesos:
        p.join()


@app.route('/enviar', methods=['POST'])
def recibir_datos():
    try:
        texto = request.form.get('texto_input')
        if not texto:
            return jsonify({"status": "error", "message": "No se recibió texto"}), 400

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

        # Parsear XML
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        elementos = []
        for entry in root.findall('atom:entry', ns):
            titulo = entry.find('atom:title', ns).text.strip()
            fecha = entry.find('atom:published', ns).text.strip()
            resumen = entry.find('atom:summary', ns).text.strip()
            autores = [a.find('atom:name', ns).text.strip() for a in entry.findall('atom:author', ns)]
            categorias = [c.attrib['term'] for c in entry.findall('atom:category', ns)]

            pdf_url = None
            for link in entry.findall('atom:link', ns):
                if link.attrib.get('title') == 'pdf':
                    pdf_url = link.attrib['href']
                    break

            elementos.append({
                "rutacarpeta": carpeta_destino,
                "titulo": titulo,
                "autores": autores,
                "fecha_publicacion": fecha,
                "categorias": categorias,
                "resumen": resumen,
                "pdf_url": pdf_url
            })

        with contador.get_lock():
            contador.value = 0

        cantidadTotalEntradas = len(elementos)
        print(f"Cantidad de entradas: {cantidadTotalEntradas}")

        # 👉 Lanzar el procesamiento en segundo plano
        mp.Process(target=lanzar_procesos, args=(elementos, contador, lock)).start()

        # 👉 Responder inmediatamente
        return jsonify({
            'status': 'success',
            'message': 'Procesamiento iniciado',
            'texto': cantidadTotalEntradas
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error del servidor: {str(e)}'
        }), 500


    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)