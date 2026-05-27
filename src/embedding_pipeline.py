import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from ocr_pipeline import extract_text_from_pdf

def chunk_text(text: str):
    print("✂️ Zerschneide Text in Chunks...")
    # Wir schneiden den Text in Blöcke von 500 Zeichen mit 50 Zeichen Überlappung,
    # damit keine Sätze an den Rändern unvollständig abgeschnitten werden.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    print(f"✅ {len(chunks)} Text-Chunks erfolgreich generiert.")
    return chunks

def generate_embeddings(chunks):
    print("🧬 Initialisiere lokales Embedding-Modell (Hugging Face)...")
    # Dieses kompakte Modell läuft komplett offline auf deiner CPU/GPU
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("⏳ Berechne mathematische Vektoren für alle Chunks...")
    # Wir testen es exemplarisch am ersten Chunk, um zu sehen, wie ein Vektor aussieht
    sample_vector = embeddings_model.embed_query(chunks[0])
    
    print(f"✅ Vektor-Berechnung erfolgreich!")
    print(f"📊 Dimension des Vektorraums: {len(sample_vector)} Dimensionen")
    return embeddings_model

if __name__ == "__main__":
    input_pdf = os.path.join("data", "test.pdf")
    
    if os.path.exists(input_pdf):
        # 1. Text extrahieren (aus deinem ersten Skript)
        raw_text = extract_text_from_pdf(input_pdf)
        
        # 2. Text in Abschnitte schneiden
        text_chunks = chunk_text(raw_text)
        
        # 3. Das Embedding-Modell laden und testen
        model = generate_embeddings(text_chunks)
        
        print("\n--- PORFOLIO-VORSCHAU FÜR ARBEITGEBER ---")
        print(f"Erster Text-Chunk:\n{text_chunks[0]}\n")
        print("Pipeline läuft fehlerfrei!")
        print("-----------------------------------------")
    else:
        print(f"❌ Fehler: {input_pdf} nicht gefunden.")