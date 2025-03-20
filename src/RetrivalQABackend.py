from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


def validate_urls(urls):
    for url in urls:
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("www.")):
            return False
    return True

def load_and_process_urls(urls):
    if not validate_urls(urls):
        return None, "Invalid URL format. URLs must start with 'http', 'https', or 'www'."
    else:
        try:

            loader = WebBaseLoader(urls)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = text_splitter.split_documents(documents)

            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_documents(chunks, embeddings)

            return vector_store, None
        except Exception as e:
            return None, f"Error processing URLs: {str(e)}"

def get_answer(vector_store, question):
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4o")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_kwargs={"k": 5},
            search_type="mmr"
        ),
        return_source_documents=True
    )

    result = qa_chain({
        "query": f"""
        Answer the following question based ONLY on the provided context. 
        Be thorough but concise. If you don't know the answer, say so.

        Question: {question}
        """
    })
    return result