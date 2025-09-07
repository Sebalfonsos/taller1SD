import fitz  # PyMuPDF
import os

def extract_text_and_images(pdf_path, output_folder="output"):
    # Crear carpeta si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    if isinstance(pdf_path, str):
        doc = fitz.open(pdf_path)
    else:  # BytesIO
        doc = fitz.open(stream=pdf_path, filetype="pdf")
    
    all_text = []            # acumulador de texto
    image_paths = []         # acumulador de rutas de imágenes

    # Extraer texto e imágenes página por página
    for page_num, page in enumerate(doc, start=1):
        # ---- Extraer texto ----
        text = page.get_text("text")
        all_text.append(f"\n\n--- Page {page_num} ---\n\n{text}")

        # ---- Extraer imágenes ----
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]  # referencia
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # 'png' o 'jpeg'
            
            img_path = os.path.join(output_folder, f"page_{page_num}_img_{img_index}.{image_ext}")
            with open(img_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(img_path)  # guardar la ruta en el array

    doc.close()
    print(f"Extraction completed! Files saved in {output_folder}")

    # Retornar un dict con texto + rutas de imágenes
    return {
        "texto": "\n".join(all_text),
        "imagenes": image_paths
    }
