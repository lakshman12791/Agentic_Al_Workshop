# import streamlit as st
# from backend.visualizer import visualize_tradeoffs
# from backend.utils import get_user_commitment, get_project_title
# from backend.rag_query import query_project_timeline

# st.set_page_config(page_title="Tradeoff Visualizer Agent", layout="centered")
# st.title("📈 Tradeoff Visualizer Agent")

# title = get_project_title()
# if title:
#     st.info(f"Analyzing timeline for: **{title}**")
#     rag_result = query_project_timeline(title)
#     st.write("**RAG Timeline Benchmark:**")
#     st.write(rag_result)

# commitment = get_user_commitment()
# if commitment:
#     visualize_tradeoffs(commitment)


# import streamlit as st
# import matplotlib.pyplot as plt

# # Placeholder: Replace this with actual Gemini + LangChain RAG logic
# def query_with_rag(prompt):
#     # Simulate a timeline response from Gemini + RAG system
#     # This would normally use vector DB like FAISS and embeddings from Gemini or OpenAI
#     if "ecommerce" in prompt.lower():
#         return {
#             "milestones": {
#                 "MVP": 4,
#                 "Launch": 6,
#                 "First 100 users": 8
#             },
#             "summary": "E-commerce projects typically take 4 months to MVP, 6 months to launch, and 8 months to first traction (100 users)."
#         }
#     elif "ai tool" in prompt.lower():
#         return {
#             "milestones": {
#                 "MVP": 5,
#                 "Beta Launch": 7,
#                 "Product-Market Fit": 12
#             },
#             "summary": "AI tool startups often take 5 months for MVP, 7 for Beta, and 12 months to reach PMF."
#         }
#     else:
#         return {
#             "milestones": {
#                 "MVP": 6,
#                 "Launch": 9,
#                 "PMF": 14
#             },
#             "summary": "General tech startups take 6 months to MVP, 9 to launch, and 14 months to reach product-market fit."
#         }

# def visualize_timeline_chart(milestones, commitment_label):
#     fig, ax = plt.subplots()
#     names = list(milestones.keys())
#     durations = list(milestones.values())
#     bars = ax.bar(names, durations, color="mediumseagreen")

#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{height} mo', xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

#     ax.set_ylabel("Estimated Duration (Months)")
#     ax.set_title(f"Startup Timeline ({commitment_label})")
#     st.pyplot(fig)

# def main():
#     st.set_page_config(page_title="Tradeoff Visualizer Agent", layout="centered")
#     st.title("📈 Tradeoff Visualizer Agent")

#     st.subheader("Startup Project Input")
#     project_title = st.text_input("Enter your startup idea or project title:")
    
#     if project_title:
#         st.success("Sending to Gemini + RAG system...")
#         with st.spinner("Analyzing timelines..."):
#             rag_result = query_with_rag(project_title)
        
#         st.subheader("📋 Timeline Insight")
#         st.markdown(rag_result["summary"])

#         st.subheader("🧠 Your Availability")
#         commitment = st.radio("How much time can you dedicate?", ["Full-time", "Part-time", "Weekend Only"])
        
#         if commitment:
#             st.subheader("📊 Visualized Timeline")
#             visualize_timeline_chart(rag_result["milestones"], commitment)

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import matplotlib.pyplot as plt
# import os
# from langchain.vectorstores import FAISS
# from langchain_google_genai import ( # type: ignore
#     GoogleGenerativeAIEmbeddings,
#     ChatGoogleGenerativeAI
# )
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import TextLoader # type: ignore

# # --- Set API Key (avoid dotenv in this version) ---
# os.environ["GOOGLE_API_KEY"] = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"

# # --- Load Vector DB (RAG) ---
# def load_vector_store():
#     embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     return FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# # --- Query Gemini + RAG ---
# def get_timeline_with_rag(user_description):
#     # Step 1: Query Gemini directly
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
#     prompt = PromptTemplate.from_template("""
#     You are a startup planning agent. Based on this idea:
#     "{description}"
#     Generate a realistic timeline with 3 phases like MVP, Launch, PMF, and estimate time in months for each.
#     Reply in JSON like:
#     {{ "MVP": 4, "Launch": 7, "PMF": 12 }}
#     """)
#     chain = prompt | llm
#     gemini_response = chain.invoke({"description": user_description})

#     # Step 2: Retrieve from vector store using same input
#     vectorstore = load_vector_store()
#     retriever = vectorstore.as_retriever(search_type="similarity", k=3)
#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
#     rag_result = qa.run(user_description)

#     return gemini_response.content, rag_result

# # --- Parse Gemini JSON Output ---
# def parse_gemini_json(response):
#     try:
#         import json
#         return json.loads(response)
#     except Exception:
#         return {"MVP": 6, "Launch": 9, "PMF": 14}  # fallback

# # --- Plot Chart ---
# def visualize_timeline_chart(milestones, title="Startup Timeline"):
#     fig, ax = plt.subplots()
#     labels = list(milestones.keys())
#     durations = list(milestones.values())
#     bars = ax.bar(labels, durations, color="cornflowerblue")
    
#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{height} mo', xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

#     ax.set_ylabel("Estimated Duration (Months)")
#     ax.set_title(title)
#     st.pyplot(fig)

# # --- Streamlit UI ---
# def main():
#     st.set_page_config(page_title="Startup Timeline Agent", layout="centered")
#     st.title("📊 Tradeoff Visualizer Agent")

#     st.markdown("Enter a detailed description of your startup idea:")
#     user_description = st.text_area("Project Description")

#     if st.button("Estimate Timeline") and user_description.strip():
#         with st.spinner("Generating timeline from Gemini and retrieving RAG data..."):
#             gemini_json_str, rag_summary = get_timeline_with_rag(user_description)
#             timeline_data = parse_gemini_json(gemini_json_str)

#         st.subheader("📄 Gemini Estimated Timeline")
#         st.code(gemini_json_str, language="json")

#         st.subheader("📚 RAG-Sourced Timeline Insight")
#         st.write(rag_summary)

#         st.subheader("📈 Visual Timeline")
#         visualize_timeline_chart(timeline_data)

# if __name__ == "__main__":
#     main()



# import streamlit as st
# import matplotlib.pyplot as plt
# import os
# import json
# import re
# from langchain.vectorstores import FAISS
# from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
# from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import TextLoader
# from pathlib import Path

# # --- Set API Key ---
# os.environ["GOOGLE_API_KEY"] = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"  # <-- Replace with your actual key

# # --- Load Vector DB (RAG) ---
# def load_vector_store():
#     embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     index_path = Path("faiss_index/index.faiss")
#     if not index_path.exists():
#         raise FileNotFoundError("FAISS index not found. Please generate it first.")
#     return FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
#     # return FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
#     # return FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# # --- Query Gemini + RAG ---
# def get_timeline_with_rag(user_description):
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
#     prompt = PromptTemplate.from_template("""
#     You are a startup planning agent. Based on this idea:
#     "{description}"
#     Generate a realistic timeline with 3 phases like MVP, Launch, PMF, and estimate time in months for each.
#     Reply in JSON like:
#     {{ "MVP": 4, "Launch": 7, "PMF": 12 }}
#     """)
#     chain = prompt | llm
#     gemini_response = chain.invoke({"description": user_description})

#     vectorstore = load_vector_store()
#     retriever = vectorstore.as_retriever(search_type="similarity", k=3)
#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
#     rag_result = qa.run(user_description)

#     return gemini_response.content, rag_result

# # --- Parse Gemini JSON Output ---
# def parse_gemini_json(response):
#     try:
#         json_str = re.search(r"\{.*\}", response, re.DOTALL).group()
#         return json.loads(json_str)
#     except Exception as e:
#         print("Parsing error:", e)
#         return {"MVP": 6, "Launch": 9, "PMF": 14}

# # --- Plot Chart ---
# def visualize_timeline_chart(milestones, title="Startup Timeline"):
#     fig, ax = plt.subplots()
#     labels = list(milestones.keys())
#     durations = list(milestones.values())
#     bars = ax.bar(labels, durations, color="cornflowerblue")

#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{height} mo', xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

#     ax.set_ylabel("Estimated Duration (Months)")
#     ax.set_title(title)
#     st.pyplot(fig)

# # --- Streamlit UI ---
# def main():
#     st.set_page_config(page_title="Startup Timeline Agent", layout="centered")
#     st.title("📊 Tradeoff Visualizer Agent")

#     st.markdown("Enter a detailed description of your startup idea:")
#     user_description = st.text_area("Project Description")

#     if st.button("Estimate Timeline") and user_description.strip():
#         with st.spinner("Generating timeline from Gemini and retrieving RAG data..."):
#             gemini_json_str, rag_summary = get_timeline_with_rag(user_description)
#             timeline_data = parse_gemini_json(gemini_json_str)

#         st.subheader("📄 Gemini Estimated Timeline")
#         st.code(gemini_json_str, language="json")

#         st.subheader("📚 RAG-Sourced Timeline Insight")
#         st.write(rag_summary)

#         st.subheader("📈 Visual Timeline")
#         visualize_timeline_chart(timeline_data)

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import matplotlib.pyplot as plt
# import os
# import json
# import re
# from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate

# # --- Set API Key ---
# os.environ["GOOGLE_API_KEY"] = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"  # Replace with your actual key

# # --- Query Gemini only (no RAG) ---
# def get_timeline_from_gemini(user_description):
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
#     prompt = PromptTemplate.from_template("""
#     You are a startup planning agent. Based on this idea:
#     "{description}"
#     Generate a realistic timeline with 3 phases like MVP, Launch, PMF, and estimate time in months for each.
#     Reply in JSON like:
#     {{ "MVP": 4, "Launch": 7, "PMF": 12 }}
#     """)
#     chain = prompt | llm
#     response = chain.invoke({"description": user_description})
#     return response.content

# # --- Parse Gemini JSON Output ---
# def parse_gemini_json(response):
#     try:
#         json_str = re.search(r"\{.*\}", response, re.DOTALL).group()
#         return json.loads(json_str)
#     except Exception as e:
#         print("Parsing error:", e)
#         return {"MVP": 6, "Launch": 9, "PMF": 14}

# # --- Plot Chart ---
# def visualize_timeline_chart(milestones, title="Startup Timeline"):
#     fig, ax = plt.subplots()
#     labels = list(milestones.keys())
#     durations = list(milestones.values())
#     bars = ax.bar(labels, durations, color="cornflowerblue")

#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{height} mo', xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

#     ax.set_ylabel("Estimated Duration (Months)")
#     ax.set_title(title)
#     st.pyplot(fig)

# # --- Streamlit UI ---
# def main():
#     st.set_page_config(page_title="Startup Timeline Agent", layout="centered")
#     st.title("📊 Tradeoff Visualizer Agent")

#     st.markdown("Enter a detailed description of your startup idea:")
#     user_description = st.text_area("Project Description")

#     if st.button("Estimate Timeline") and user_description.strip():
#         with st.spinner("Generating timeline from Gemini..."):
#             gemini_json_str = get_timeline_from_gemini(user_description)
#             timeline_data = parse_gemini_json(gemini_json_str)

#         st.subheader("📄 Gemini Estimated Timeline")
#         st.code(gemini_json_str, language="json")

#         st.subheader("📈 Visual Timeline")
#         visualize_timeline_chart(timeline_data)

# if __name__ == "__main__":
#     main()


import streamlit as st
import matplotlib.pyplot as plt
import os
import json
import re
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# --- Set API Key ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"  # Replace with your actual key

# --- Call Gemini and compute timeline ---
def get_timeline_from_gemini(user_description):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate.from_template("""
    You are a startup planning agent. Based on this idea:
    "{description}"
    Generate a realistic timeline with 3 phases like MVP, Launch, PMF.
    Estimate time in months for each **phase individually** (not cumulative).
    Reply in valid JSON format only like:
    {{ "MVP": 3, "Launch": 6, "PMF": 8 }}
    """)
    chain = prompt | llm
    response = chain.invoke({"description": user_description})
    
    # --- Extract JSON ---
    try:
        json_str = re.search(r"\{.*\}", response.content, re.DOTALL).group()
        phase_durations = json.loads(json_str)
    except Exception as e:
        print("Parsing error:", e)
        return {}, {}, response.content  # fallback if error

    # --- Compute cumulative milestones ---
    cumulative = {}
    total = 0
    for phase, duration in phase_durations.items():
        total += duration
        cumulative[phase] = total

    return phase_durations, cumulative, json_str

# --- Plot Timeline Chart ---
def visualize_timeline_chart(milestones, title="Startup Timeline (Cumulative Months)"):
    fig, ax = plt.subplots()
    labels = list(milestones.keys())
    times = list(milestones.values())
    bars = ax.bar(labels, times, color="mediumseagreen")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height} mo', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    ax.set_ylabel("Cumulative Time (Months)")
    ax.set_title(title)
    st.pyplot(fig)

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="Startup Timeline Agent", layout="centered")
    st.title("📊 Startup Timeline Generator")

    st.markdown("Enter a detailed description of your startup idea:")
    user_description = st.text_area("Project Description")

    if st.button("Estimate Timeline") and user_description.strip():
        with st.spinner("Generating timeline from Gemini..."):
            durations, cumulative, raw_json = get_timeline_from_gemini(user_description)

        st.subheader("📄 Gemini Estimated Durations")
        st.json(durations)

        st.subheader("🕒 Cumulative Timeline (in months)")
        st.json(cumulative)

        st.subheader("📈 Visual Timeline")
        visualize_timeline_chart(cumulative)

if __name__ == "__main__":
    main()
