import json
import streamlit as st
import os
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from google.generativeai import configure
from langchain.docstore.document import Document

# Constants
DATA_PATH = "data/startup_stories.json"

# Streamlit UI setup
st.set_page_config(page_title="📖 Experience Retriever Agent")
st.title("📖 Experience Retriever Agent")

api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

# --- Optional source filter ---
selected_source = st.selectbox("📰 Filter by Source", ["All", "IndieHackers", "YC", "Blog"])

# Function to create retriever
@st.cache_resource
def create_retriever(api_key):
    configure(api_key=api_key)
    
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Apply source filtering
    if selected_source != "All":
        data = [entry for entry in data if entry.get("source", "Unknown") == selected_source]

    docs = [
        Document(
            page_content=entry["story"],
            metadata={
                "company": entry.get("company", ""),
                "source": entry.get("source", "Unknown"),
                "url": entry.get("url", "")
            }
        )
        for entry in data
    ]

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )

    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Function to answer question using RAG
def ask_question_with_rag(retriever, query, api_key):
    configure(api_key=api_key)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key=api_key
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain(query)
    return result

# Main interaction
query = st.text_area("💬 Ask about startup timelines (e.g., How long to get first 100 users?)")

if st.button("🔍 Retrieve Experience"):
    if query and api_key:
        retriever = create_retriever(api_key)
        result = ask_question_with_rag(retriever, query, api_key)
        st.markdown("### 📌 Answer")
        st.write(result["result"])

        # Display sources (optional)
        with st.expander("🧾 Sources"):
            for doc in result["source_documents"]:
                metadata = doc.metadata
                st.markdown(f"- **{metadata.get('company', 'Unknown')}** ({metadata.get('source', '')})")
                st.markdown(f"  [Read more]({metadata.get('url', '#')})")
    else:
        st.warning("Please enter both a query and an API key.")
