import streamlit as st
import matplotlib.pyplot as plt
import datetime
import google.generativeai as genai
import os

# --- Streamlit UI ---
st.title("🧠 Timeline Simulation Agent")
st.subheader("Plan your MVP, GTM, Fundraising, and PMF over 12–24 weeks")

# Input fields
gemini_api_key = st.text_input("🔑 Enter Gemini API Key", type="password")
business_idea = st.text_area("💡 Describe your business idea", height=200)
week_range = st.slider("📅 Select Timeline Range (weeks)", 12, 24, 16)

# Gemini Setup
def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

# Prompt Template
def build_prompt(idea, weeks):
    return f"""
You are a startup planning agent. Based on the following idea:
\"\"\"{idea}\"\"\"
Generate a realistic startup timeline for the next {weeks} weeks. Include key phases like:
- MVP development
- Go-To-Market (GTM)
- Fundraising
- Product-Market Fit (PMF)

Return the result as JSON like:
[
  {{"phase": "MVP", "start_week": 1, "duration_weeks": 5}},
  {{"phase": "GTM", "start_week": 6, "duration_weeks": 4}},
  ...
]
"""

# Timeline Parser and Plotter
def parse_and_plot_timeline(json_data, weeks):
    fig, ax = plt.subplots(figsize=(10, 5))
    today = datetime.date.today()

    for i, item in enumerate(json_data):
        phase = item["phase"]
        start = today + datetime.timedelta(weeks=item["start_week"] - 1)
        duration = datetime.timedelta(weeks=item["duration_weeks"])
        ax.barh(phase, duration.days, left=start.toordinal(), height=0.5)

    ax.set_xlabel("Date")
    ax.set_ylabel("Phase")
    ax.set_title("Startup Timeline (Next {} Weeks)".format(weeks))
    ax.set_yticks(range(len(json_data)))
    ax.set_yticklabels([item["phase"] for item in json_data])
    ax.set_xlim(today.toordinal(), (today + datetime.timedelta(weeks=weeks)).toordinal())
    ax.set_xticks([today.toordinal() + 7 * i for i in range(weeks)])
    ax.set_xticklabels([(today + datetime.timedelta(weeks=i)).strftime('%b %d') for i in range(weeks)], rotation=45)
    st.pyplot(fig)

# Generate Timeline
if st.button("🚀 Generate Timeline") and gemini_api_key and business_idea:
    try:
        model = init_gemini(gemini_api_key)
        prompt = build_prompt(business_idea, week_range)
        response = model.generate_content(prompt)
        content = response.text

        # Try to extract JSON
        import json, re
        json_str = re.search(r"\[.*\]", content, re.DOTALL)
        if json_str:
            timeline = json.loads(json_str.group())
            parse_and_plot_timeline(timeline, week_range)
        else:
            st.error("Could not parse timeline from Gemini response.")
            st.code(content)
    except Exception as e:
        st.error(f"❌ Error: {e}")
