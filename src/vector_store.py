import os
from langchain_chroma import Chroma
from embedding_pipeline import extract_text_from_pdf, chunk_text, HuggingFaceEmbeddings

# Pfad, an dem die Datenbank lokal gespeichert wird
CHROMA_PATH = "chroma_db"

def create_vector_store(pdf_path: str):
    # 1. Daten über die bestehende Pipeline holen
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw_text)
    
    # 2. Das Embedding-Modell laden
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print(f"📦 Initialisiere ChromaDB im Ordner '{CHROMA_PATH}'...")
    
    # 3. Vektordatenbank erstellen und Chunks speichern
    db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_PATH
    )
    
    print("✅ Alle Chunks wurden erfolgreich in der Vektordatenbank gespeichert!")
    return db

def query_vector_store(query_text: str):
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Datenbank aus dem Verzeichnis laden
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings_model)
    
    print(f"\n🔍 Suche in der Datenbank nach: '{query_text}'")
    # Suche die Top 2 relevantesten Abschnitte
    results = db.similarity_search_with_relevance_scores(query_text, k=2)
    
    return results

if __name__ == "__main__":
    input_pdf = os.path.join("data", "test.pdf")
    
    if os.path.exists(input_pdf):
        # Datenbank erstellen
        vector_db = create_vector_store(input_pdf)
        
        # Test-Abfrage starten (basierend auf deiner Bibliografie zu "The Day After Tomorrow")
        # Wir suchen nach dem Begriff 'Klimaforscher', um zu sehen, ob er den richtigen Absatz findet
        query = "Klimaforscher"
        search_results = query_vector_store(query)
        
        print("\n--- INHALTLICHE SUCHERGEBNISSE (RETRIEVAL) ---")
        for doc, score in search_results:
            print(f"📄 [Score: {score:.4f}]")
            print(f"Inhalt: {doc.page_content}\n")
        print("----------------------------------------------")
        
    else:
        print(f"❌ Fehler: {input_pdf} nicht gefunden.")