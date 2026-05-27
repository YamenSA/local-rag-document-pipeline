import streamlit as st
import os
from src.rag_chain import run_rag_chain

# Konfiguration der Webseite
st.set_page_config(page_title="Local RAG Document Chat", page_icon="🤖", layout="wide")

st.title("🤖 Local RAG Document Chat Assistant")
st.subheader("Stelle Fragen an deine Dokumente – komplett lokal und sicher.")

st.markdown("---")

# Layout aufteilen: Links der Chat, rechts die Quellenanzeige
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat")
    
    # Session State initialisieren, um den Chat-Verlauf zu speichern
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Bisherige Nachrichten anzeigen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Benutzereingabe
    if user_query := st.chat_input("Frage etwas über das Dokument..."):
        # 1. Benutzer-Nachricht im Chat anzeigen und speichern
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # 2. RAG-Pipeline aufrufen und Antwort generieren
        with st.chat_message("assistant"):
            with st.spinner("Die KI durchsucht das Dokument und generiert eine Antwort..."):
                try:
                    answer, sources = run_rag_chain(user_query)
                    st.markdown(answer)
                    
                    # Antwort im Verlauf speichern
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Quellen für die rechte Spalte zwischenspeichern
                    st.session_state.latest_sources = sources
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {e}")

with col2:
    st.header("📋 Genutzte Quellen")
    st.write("Hier siehst du, auf welche Text-Abschnitte sich die KI bei der letzten Antwort bezogen hat:")
    
    if "latest_sources" in st.session_state and st.session_state.latest_sources:
        for i, doc in enumerate(st.session_state.latest_sources):
            with st.expander(f"Quelle [{i+1}]", expanded=True):
                st.write(doc.page_content)
    else:
        st.info("Noch keine Abfrage gestartet. Stelle eine Frage im Chat, um die genutzten Abschnitte zu sehen.")