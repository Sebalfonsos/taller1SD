import fitz  # PyMuPDF
import os

def extraer_pdf(ruta_pdf, carpeta_salida="salida_pdf"):
    # Abrir el PDF
    doc = fitz.open(ruta_pdf)

    # Crear carpeta de salida si no existe
    os.makedirs(carpeta_salida, exist_ok=True)

    for num_pagina in range(len(doc)):
        pagina = doc[num_pagina]
        
        # ---- EXTRAER TEXTO ----
        texto = pagina.get_text()
        with open(os.path.join(carpeta_salida, f"pagina_{num_pagina+1}.txt"), "w", encoding="utf-8") as f:
            f.write(texto)

        # ---- EXTRAER IMÁGENES ----
        for i, img in enumerate(pagina.get_images(full=True)):
            xref = img[0]  # referencia a la imagen
            pix = doc.extract_image(xref)
            imagen_bytes = pix["image"]
            ext = pix["ext"]  # extensión (png, jpg, etc.)

            with open(os.path.join(carpeta_salida, f"pagina_{num_pagina+1}_img_{i+1}.{ext}"), "wb") as f:
                f.write(imagen_bytes)

    print(f"✅ Texto e imágenes extraídos en: {carpeta_salida}")


