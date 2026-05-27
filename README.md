# 🤖 Local RAG Document Chat Assistant

A privacy-focused, fully local **Retrieval-Augmented Generation (RAG)** system that allows users to have an interactive chat with their PDF documents. The application runs entirely offline on your local machine, ensuring complete data privacy with zero API costs.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama"/>
  <img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=flat-square" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/100%25-Local-success?style=flat-square" alt="100% Local"/>
</p>

---

## 📊 System Architecture

This project implements a complete Applied AI pipeline from raw document ingestion to an interactive web interface. GitHub renders the architecture below automatically:

```mermaid
graph TD
    subgraph Ingestion Pipeline
        A[PDF Document] -->|pdf2image| B(Page Images)
        B -->|pytesseract OCR| C(Clean Raw Text)
        C -->|RecursiveTextSplitter| D(Text Chunks)
    end

    subgraph Vector Storage
        D -->|langchain-huggingface| E(all-MiniLM-L6-v2 Embeddings)
        E -->|Store| F[(Local ChromaDB)]
    end

    subgraph UI & Inference
        G[User Query] -->|Semantic Search| F
        F -->|Top-3 Context Chunks| H(Prompt Template)
        G --> H
        H -->|Context + Query| I[Local Llama 3.1 via Ollama]
        I -->|Response| J(Streamlit Web UI)
    end
```

---

## 📸 Application Demo

![Application User Interface](docs/app_demo_localhost.png)

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| **Orchestration** | `LangChain` & `langchain-core` |
| **Frontend UI** | `Streamlit` (Interactive dual-column chat interface) |
| **Vector Database** | `ChromaDB` (via `langchain-chroma`) |
| **Text Embedding** | `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`, 384-dimensional vectors) |
| **Data Ingestion & OCR** | `PyTesseract` (Google OCR Engine) & `pdf2image` |

---

## 🚀 Quick Start Guide

Follow these steps to set up and run the project locally:

### 1. Prerequisites

- Install **Python 3.10+**
- Install **Ollama** and pull the model: `ollama pull llama3.1`
- Install **Tesseract OCR** on your system and ensure it is accessible in your script config.

### 2. Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/YamenSA/local-rag-document-pipeline.git
cd local-rag-document-pipeline
```

Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Usage

**Step 1:** Place your target PDF file inside the `data/` directory and name it `test.pdf`.

**Step 2:** Initialize the database and run the OCR ingestion pipeline:

```bash
python src/vector_store.py
```

**Step 3:** Launch the interactive Streamlit Web App:

```bash
streamlit run app.py
```

---

## 🔒 Privacy & Security Notice

This application requires no external API keys and sends no data over the internet. The PDF text extraction, vector embed generation, database storage, and LLM text generation occur entirely locally on your hardware.
