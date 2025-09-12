# Taller1SD  

## 📌 Descripción  
- Consultar artículos en **ArXiv** mediante su API.  
- Descargar archivos PDF de los artículos encontrados.  
- Extraer texto e imágenes de los PDFs.  
- Generar **palabras clave (keywords)** usando un modelo de Inteligencia Artificial.  
- Almacenar la información procesada en **MongoDB** para su consulta posterior.  
- Ofrecer una interfaz para visualizar los resultados.  

---

## 👥 Integrantes del grupo  
- **Chaira Mileth Zapa Caraballo**  
- **Lucia Carolina Arroyo Figueroa**  
- **Sebastián Alfonso Sierra Torres**  

---

## ⚙️ Tecnologías utilizadas  
- **Python 3**  
- **Flask** – Framework para el servidor web  
- **MongoDB** – Base de datos NoSQL para almacenar artículos  
- **PyMuPDF (fitz)** – Extracción de texto e imágenes de PDFs  
- **Requests** – Descarga de archivos desde URLs  
- **Multiprocessing / concurrent.futures** – Procesamiento paralelo  
- **Ollama (Gemma3:1b)** – Generación de keywords con IA  
- **tqdm** – Barra de progreso en la consola  

---

## 📂 Estructura del proyecto  

```
Taller1SD/
│── app.py                  # Servidor Flask y lógica principal
│── config.json             # Configuración (número de procesos)
│── dbmongo.py              # Conexión y operaciones con MongoDB
│── descargar.py            # Función para descargar archivos
│── diagramadeclases.png    # Diagrama de clases del proyecto
│── inteligenciaArtificial.py # Generación de keywords con IA
│── pdfextractor.py         # Extracción de texto e imágenes de PDFs
│── procesos.py             # Ejemplo de procesos paralelos
│── readpdf.py              # Extracción de PDFs en carpetas
│── sanitizar.py            # Limpieza de nombres de archivo
│── downloads/              # Carpeta donde se guardan PDFs y resultados
│── templates/              # Vistas HTML (index, resultados, artículo)
```
---
## 🚀 Funcionamiento  

1. El usuario envía un término de búsqueda desde la interfaz web.  
2. El sistema consulta la API de **ArXiv** y obtiene un conjunto de artículos relacionados.  
3. Se descargan los PDFs asociados y se extraen texto e imágenes.  
4. Se generan **keywords** relevantes mediante el módulo de IA.  
5. Toda la información se guarda en **MongoDB**.  
6. El usuario puede consultar los resultados en la página web y ver cada artículo procesado.  
---
## ▶️ Ejecución  

1. Instalar dependencias necesarias:  
   ```bash
   pip install flask pymongo requests pymupdf tqdm ollama
   ```

2. Asegurarse de que **MongoDB** esté en ejecución en `localhost:27017`.  

3. Ejecutar el servidor:  
   ```bash
   python app.py
   ```

4. Abrir en el navegador:  
   ```
   http://localhost:5000
   ```
