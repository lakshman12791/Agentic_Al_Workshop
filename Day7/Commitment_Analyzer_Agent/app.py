import streamlit as st
from gemini_rag_agent.agent import GeminiRAGAgent

import sys
print(sys.path)


st.set_page_config(page_title="Gemini RAG Agent", layout="centered")
st.title("🔍 Gemini RAG Agent")
st.markdown("Ask your startup-related questions and get realistic, benchmarked answers.")

GEMINI_API_KEY = st.text_input("🔑 Enter your Gemini API Key", type="password")

sample_documents = [
    "As a solo founder, I worked weekends and evenings. My MVP took 4 months.",
    "I went full-time and built my MVP in 6 weeks, launched to early adopters soon after.",
    "Balancing freelancing, it took me 3 months part-time to finish my MVP."
]

if GEMINI_API_KEY:
    agent = GeminiRAGAgent(api_key=GEMINI_API_KEY, documents=sample_documents)

    question = st.text_input("🧠 Ask a question about startup timelines")

    if question:
        with st.spinner("Thinking..."):
            response = agent.query(question)
        st.success("Response:")
        st.write(response)
else:
    st.info("Please enter your Gemini API Key to start.")
