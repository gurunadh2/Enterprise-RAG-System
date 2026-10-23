# Enterprise RAG System

## Overview

Enterprise RAG System is a multi-user Retrieval-Augmented Generation (RAG) platform built with FastAPI, Streamlit, Qdrant, Ollama, and Hybrid Retrieval.

The system allows users to upload PDF documents, perform semantic and keyword-based search, and interact with an AI assistant that answers questions using document content.

---

## Features

* User Registration and Login
* JWT Authentication
* PDF Upload and Processing
* Document Chunking
* Vector Embeddings
* Qdrant Vector Database
* BM25 Retrieval
* Hybrid Retrieval (RRF)
* Ollama Llama 3 Integration
* Source Citations
* Chat History
* User-Specific Chat History
* User-Specific Document Ownership
* Feedback Collection
* Analytics Dashboard
* Multi-PDF Support

---

## Tech Stack

### Backend

* FastAPI
* Python
* SQLite
* Qdrant

### AI Components

* Ollama
* Llama 3
* Sentence Transformers
* BM25

### Frontend

* Streamlit

---

## Project Structure

app/

* api
* auth
* chat
* feedback
* rag
* database
* evaluation

frontend/

* streamlit_app.py

uploads/

---

## Run the Project

### Start Docker

```bash
docker start qdrant
```

### Start Ollama

```bash
ollama serve
```

### Start Backend

```bash
uvicorn app.main:app --reload
```

### Start Frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

## Future Improvements

* User-specific document listing
* Admin roles
* Conversation memory
* Docker Compose deployment
* Cloud deployment
* Role-based access control

---

## Author

Guru
