import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_process_urls(urls):
    try:
        loader = WebBaseLoader(urls)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(chunks, embeddings)
        retr = vector_store.as_retriever(search_kwargs={"k": 5}, search_type="mmr")
        return retr
    except Exception as e:
        print(f"Error processing URLs: {str(e)}")  # Print the error
        return None

def get_answer(retr ,question):
    # retriever = vector_store.as_retriever(search_kwargs={"k": 5}, search_type="mmr")
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4o",api_key="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")
    relevent_docs = retr.get_relevant_documents(question)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a RAG Extractor AI. You have been given a question and a set of documents to find the answer from.
        
        Help me answer: 
        {question}
        Based on the provided Context : 
          {context}
          
        Make Sure to answer only from relevant context and be thorough but concise. If you don't know the answer, say so.  
          """
    )
    chain = create_stuff_documents_chain(llm , prompt)
    res = chain.invoke({"context": relevent_docs, "question": question})
    return res


def main():
    os.environ["OPENAI_API_KEY"] = "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"
    vs = load_and_process_urls(["https://en.wikipedia.org/wiki/Rain","https://aisensy.com/"])
    question = "What does AI Sensy do"
    res = get_answer(vs, question)
    print(res)

if __name__=="__main__":
    main()

