import os
import pandas as pd
from PIL import Image
from pillow_heif import register_heif_opener
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# HEIC-Unterstützung aktivieren
register_heif_opener()

def heic_to_jpeg(heic_path):
    image = Image.open(heic_path)
    return image

def images_to_pdf(images, pdf_path):
    if not images:
        return
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    for image in images:
        # Bild skalieren, falls zu groß
        img_width, img_height = image.size
        scale = min(width / img_width, height / img_height)
        new_size = (int(img_width * scale), int(img_height * scale))
        image = image.resize(new_size)

        # Temporär speichern, weil reportlab mit Image-Objekten direkt nicht klarkommt
        temp_jpg = "temp_image.jpg"
        image.save(temp_jpg, format="JPEG", quality=95)

        # Im PDF platzieren
        c.drawImage(temp_jpg, 0, height - new_size[1], width=new_size[0], height=new_size[1])
        c.showPage()
        os.remove(temp_jpg)

    c.save()

def process_excel(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Überordner sicherstellen

    df = pd.read_excel(file_path)
    grouped = df.groupby('Bewerber')['Bild'].apply(list).to_dict()

    for bewerber, paths in grouped.items():
        # PDF direkt im Überordner
        pdf_path = os.path.join(output_dir, f'{bewerber}.pdf')

        if os.path.exists(pdf_path):
            print(f"PDF für {bewerber} existiert bereits - wird überschrieben.")
        
        images = []
        for path in paths:
            if os.path.exists(path) and path.lower().endswith(".heic"):
                try:
                    img = heic_to_jpeg(path)
                    images.append(img)
                except Exception as e:
                    print(f"Fehler beim Laden von {path}: {e}")

        images_to_pdf(images, pdf_path)
        print(f"PDF für {bewerber} wurde erstellt: {os.path.abspath(pdf_path)}")

if __name__ == '__main__':
    excel_path = r"/Users/dominik/Desktop/ExcelBewerber.xlsx"
    output_directory = '/Users/dominik/Desktop/Bewerber_PDFs'
    process_excel(excel_path, output_directory)
