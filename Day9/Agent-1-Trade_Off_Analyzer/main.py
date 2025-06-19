

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
    st.title("Tradeoff Visualizer Agent")

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
