import os
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

DATA_PATH = "data/startup_stories.txt"
VECTOR_PATH = "faiss_index"

def create_retriever(api_key):
    #os.environ["GOOGLE_API_KEY"] = api_key  # Set the API key in environment
    # api_key = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"

    
    # Load and split documents
    loader = TextLoader(DATA_PATH)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(docs)
    
    # Generate embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Create or load FAISS index
    vectorstore = FAISS.from_documents(texts, embeddings)
    # Optional: Save index for reuse
    # vectorstore.save_local(VECTOR_PATH)
    
    return vectorstore.as_retriever()

def ask_question_with_rag(retriever, query, api_key):
    os.environ["GOOGLE_API_KEY"] = api_key  # Set the API key in environment
    
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    
    result = qa_chain.run(query)
    return result

# Example usage:
# api_key = "your-google-api-key"
# retriever = create_retriever(api_key)
# answer = ask_question_with_rag(retriever, "What challenges did the founders face?", api_key)
# print(answer)
