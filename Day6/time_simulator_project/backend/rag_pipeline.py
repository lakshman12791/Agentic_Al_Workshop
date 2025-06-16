from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain.chains import RetrievalQA
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings # type: ignore


# Load environment variables
load_dotenv()
api_key = ("AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo")

# Use Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

def load_vector_store():
    loader = JSONLoader(
        file_path=Path("./founder_stories.json"),
        jq_schema=".[]",
        text_content=False  # Prevent ValueError
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    vector_store = FAISS.from_documents(texts, embeddings)
    return vector_store

# Load FAISS vector store
vector_store = load_vector_store()

# Use Gemini LLM
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key),
    retriever=vector_store.as_retriever()
)

def query_similar_stories(query: str):
    return qa_chain.run(query)
