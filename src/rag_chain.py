import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM  # Das ist das neue, stabile Modul
from langchain_core.prompts import PromptTemplate  # Korrekter Importpfad für modernstes LangChain

CHROMA_PATH = "chroma_db"

def run_rag_chain(query_text: str):
    # 1. Verbindung zur existierenden Vektordatenbank herstellen
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings_model)
    
    # 2. Die Top 3 relevantesten Textstücke aus der PDF suchen
    print(f"🔍 Durchsuche Dokumenten-Wissen nach: '{query_text}'...")
    relevant_docs = db.similarity_search(query_text, k=3)
    
    # Die gefundenen Texte zu einem einzigen Kontext-Block zusammenfügen
    context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
    
    # 3. Den prompt (die präzise Arbeitsanweisung) definieren
    # Das ist extrem wichtig, damit das LLM NICHT halluziniert, sondern nur das PDF nutzt!
    template = """
    Du bist ein präziser, wissenschaftlicher Assistent. Beantworte die Frage des Nutzers AUSSCHLIESSLICH basierend auf dem bereitgestellten Kontext. 
    Wenn die Antwort nicht im Kontext zu finden ist, sage höflich, dass das Dokument diese Information nicht beinhaltet. Erfinde keine Fakten.

    BEREITGESTELLTER KONTEXT:
    {context}

    FRAGE:
    {question}

    ANTWORT:
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # 4. Lokales Llama 3.1 Modell über Ollama initialisieren
    print("🧠 Rufe lokales Llama 3.1 Modell auf...")
    llm = OllamaLLM(model="llama3.1", temperature=0.2) # Niedrige Temperature für faktengetreue Antworten
    
    # Prompt mit echten Daten befüllen
    formatted_prompt = prompt.format(context=context, question=query_text)
    
    # Antwort generieren
    response = llm.invoke(formatted_prompt)
    
    return response, relevant_docs

if __name__ == "__main__":
    # Test-Frage an dein Dokument ("test.pdf")
    user_question = "Worüber streiten Klimaforscher laut dem Artikel von Markus Becker?"
    
    if os.path.exists(CHROMA_PATH):
        answer, sources = run_rag_chain(user_question)
        
        print("\n🤖 ANTWORT DER KI:")
        print(answer)
        print("\n📋 QUELLEN-CHUNKS DIE GENUTZT WURDEN:")
        for i, doc in enumerate(sources):
            print(f"[{i+1}] {doc.page_content[:150]}...")
    else:
        print(f"❌ Fehler: Keine Vektordatenbank unter '{CHROMA_PATH}' gefunden. Starte zuerst vector_store.py!")