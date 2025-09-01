import fitz  # PyMuPDF
import os

def extract_text_and_images(pdf_path, output_folder="output"):
    # Crear carpeta si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    all_text = []  # acumulador de texto

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
            
            with open(os.path.join(output_folder, f"page_{page_num}_img_{img_index}.{image_ext}"), "wb") as f:
                f.write(image_bytes)

    # Guardar todo el texto en un solo archivo
    with open(os.path.join(output_folder, "all_text.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_text))

    doc.close()
    print(f"Extraction completed! Files saved in {output_folder}")

# Ejemplo de uso
extract_text_and_images("example.pdf")
