# import streamlit as st
# from gemini_rag_agent.agent import GeminiRAGAgent
# import google.generativeai as genai
# import sys

# print(sys.path)

# st.set_page_config(page_title="Gemini RAG Agent", layout="centered")
# st.title("🔍 Gemini RAG Agent")
# st.markdown("Ask your startup-related questions and get realistic, benchmarked answers.")

# # In production, ask for key via UI:
# # GEMINI_API_KEY = st.text_input("🔑 Enter your Gemini API Key", type="password")
# GEMINI_API_KEY = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"

# sample_documents = [
#     "As a solo founder, I worked weekends and evenings. My MVP took 4 months.",
#     "I went full-time and built my MVP in 6 weeks, launched to early adopters soon after.",
#     "Balancing freelancing, it took me 3 months part-time to finish my MVP."
# ]

# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)

#     # ✅ Now this works since the class accepts documents
#     agent = GeminiRAGAgent(documents=sample_documents)

#     question = st.text_input("🧠 Ask a question about startup timelines")

#     if question:
#         with st.spinner("Thinking..."):
#             response = agent.answer(question)  # changed to `.answer()` since that's the method you defined
#         st.success("Response:")
#         st.write(response)
# else:
#     st.info("Please enter your Gemini API Key to start.")


import streamlit as st
from gemini_rag_agent.agent import GeminiRAGAgent
import google.generativeai as genai

# Configure page
st.set_page_config(page_title="Startup Feasibility Analyzer", layout="centered")
st.title("🧠 Gemini Startup Analyzer")
st.markdown("Understand your startup feasibility based on your current lifestyle and idea scope.")

# Get API key
GEMINI_API_KEY = st.text_input("🔑 Enter your Gemini API Key", type="password")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    agent = GeminiRAGAgent()

    # User inputs
    lifestyle = st.text_area("👤 Describe your current lifestyle (job, study, family, etc.)", height=100)
    idea = st.text_area("🚀 Describe your startup idea", height=100)

    if st.button("Analyze Feasibility"):
        if lifestyle.strip() and idea.strip():
            with st.spinner("Analyzing with Gemini..."):
                response = agent.analyze(lifestyle, idea)
            st.success("📊 Analysis Result")
            st.write(response)
        else:
            st.warning("Please fill in both lifestyle and startup idea.")
else:
    st.info("Please enter your Gemini API Key to continue.")
