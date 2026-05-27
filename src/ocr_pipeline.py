import os
from pdf2image import convert_from_path
import pytesseract

# 1. Tesseract den Pfad zuweisen, damit Windows es findet
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path: str) -> str:
    print(f"🔄 Starte Verarbeitung von: {pdf_path}")
    
    # 2. PDF-Seiten in Bilder umwandeln
    print("📸 Wandle PDF-Seiten in Bilder um...")
    pages = convert_from_path(pdf_path, dpi=300)
    
    full_text = []
    
    # 3. Schleife über alle Seiten des Dokuments
    for i, page in enumerate(pages):
        print(f"🔤 Führe OCR auf Seite {i+1}/{len(pages)} aus...")
        # Hier kannst du später lang='ara' oder lang='deu' hinzufügen
        text = pytesseract.image_to_string(page, lang='deu+eng') 
        full_text.append(text)
        
    print("✅ Verarbeitung abgeschlossen!")
    return "\n\n".join(full_text)

if __name__ == "__main__":
    # Pfad zu deiner Test-Datei im data-Ordner
    input_pdf = os.path.join("data", "test.pdf")
    
    if os.path.exists(input_pdf):
        extracted_text = extract_text_from_pdf(input_pdf)
        
        print("\n--- EXTRAHIERTER TEXT VORSCHAU ---")
        # Zeige die ersten 500 Zeichen im Terminal an
        print(extracted_text[:500])
        print("----------------------------------")
    else:
        print(f"❌ Fehler: Die Datei {input_pdf} wurde nicht gefunden!")