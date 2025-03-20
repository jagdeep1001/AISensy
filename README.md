# Web Data Extractor with OpenAI

## Overview
This Streamlit-based application allows users to:
- Securely enter their OpenAI API key.
- Input multiple URLs to fetch and process web data.
- Ask questions based on the extracted data.
- Receive AI-generated answers from relevant context using OpenAI’s GPT-4o.

## Tech Stack
- **Streamlit**: UI framework for building interactive web apps in Python.
- **LangChain**: Framework for working with LLMs, including document processing and retrieval.
- **FAISS**: Facebook AI Similarity Search for efficient vector-based document retrieval.
- **OpenAI API**: GPT-4o model for generating answers from retrieved context.

## Features
✅ **Session State**: Stores API key and retriever object for a seamless experience.  
✅ **Secure Input Handling**: API key is hidden using password-type input.  
✅ **Efficient Text Processing**: Uses **RecursiveCharacterTextSplitter** for optimal chunking.  
✅ **Vector Search with FAISS**: Enables **fast** and **accurate** retrieval of relevant context.  
✅ **RAG-based Answering**: Ensures answers come **only from extracted documents**.  
✅ **Minimal Yet Professional UI**: Uses emojis, spinners, and success messages for a clean experience.  

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Setup
1. Clone the repository:
2. Create and activate virtual Env:
   ```
   python3 -m venv venv1
       source venv1/bin/activate
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```sh
   streamlit run src/single_page.py
   ```

## Usage
1. Enter your OpenAI API key in the provided input field.
2. Paste URLs (one per line) in the text area and click **Process URLs**.
3. Once processed, enter a question related to the extracted data.
4. Click **Get Answer** to receive an AI-generated response based on retrieved context.

## Code Overview
### **1. Load and Process URLs**
- Fetches content using `WebBaseLoader`.
- Splits text into chunks using `RecursiveCharacterTextSplitter`.
- Embeds and stores text in FAISS for efficient retrieval.

### **2. Retrieve Relevant Context**
- Uses FAISS with **Maximum Marginal Relevance (MMR)** to fetch the most relevant content for a given question.

### **3. Generate Answers**
- Uses `ChatOpenAI` (GPT-4o) to generate responses.
- Implements a **Retrieval-Augmented Generation (RAG)** approach to ensure answers are based on the extracted documents.
