import streamlit as st
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_process_urls(urls, api_key):
    try:
        loader = WebBaseLoader(urls)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store.as_retriever(search_kwargs={"k": 5}, search_type="mmr")
    except Exception as e:
        st.error(f"Error processing URLs: {str(e)}")
        return None


def get_answer(retriever, question, api_key):
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4o", openai_api_key=api_key)
    relevant_docs = retriever.get_relevant_documents(question)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a RAG Extractor AI. Answer the question using the provided documents.

        Question: {question}
        Context: {context}

        Answer strictly from the context. If you don't know, say so.
        """
    )

    chain = create_stuff_documents_chain(llm, prompt)
    res = chain.invoke({"context": relevant_docs, "question": question})
    return res


# Streamlit UI
st.set_page_config(page_title="Web Data Extractor", layout="centered")
st.title("🌐 Web Data Extractor with OpenAI")

# Initialize session state
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Set API Key
st.session_state.api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")

# if st.session_state.api_key:
urls = st.text_area("🌍 Enter URLs (one per line):").split("\n")
if st.button("🔄 Process URLs") and urls:
    with st.spinner("Processing URLs..."):
        st.session_state.retriever = load_and_process_urls(urls, st.session_state.api_key)
    if st.session_state.retriever:
        st.success("✅ URLs processed successfully!")

if st.session_state.retriever:
    question = st.text_input("❓ Enter your question:")
    if st.button("🤖 Get Answer") and question:
            with st.spinner("Generating answer..."):
                answer = get_answer(st.session_state.retriever, question, st.session_state.api_key)
            st.write("### 📌 Answer:")
            st.success(answer)
