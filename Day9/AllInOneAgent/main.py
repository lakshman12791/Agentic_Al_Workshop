import streamlit as st
import matplotlib.pyplot as plt
import datetime
import os
import re
import json
import google.generativeai as genai
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# ------------------------- Commitment Agent -------------------------
class GeminiRAGAgent:
    def __init__(self, model_name="models/gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def analyze(self, lifestyle, startup_idea):
        prompt = (
            "You are a startup mentor. Analyze the founder's current lifestyle and the scope of their startup idea.\n\n"
            f"**Lifestyle**: {lifestyle}\n"
            f"**Startup Idea**: {startup_idea}\n\n"
            "Give realistic feedback on their commitment ability and timeline feasibility."
        )
        response = self.model.generate_content(prompt)
        return response.text

# ------------------------- Streamlit App -------------------------
st.set_page_config(page_title="Multi-Agent Startup Analyzer", layout="centered")
st.title("🚀 Multi-Agent Startup Toolkit")

# Select Agent
agent_choice = st.selectbox("Choose Agent", [
    "Cumulative Monthly Timeline",
    "Weekly Phase Simulation",
    "Commitment Analyzer"
])

# API Key
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    os.environ["GOOGLE_API_KEY"] = api_key  # for langchain Gemini
else:
    st.info("Please enter your Gemini API key to continue.")

# Common Input
startup_idea = st.text_area("💡 Describe your Startup Idea", height=150) if agent_choice != "Commitment Analyzer" else None

# ------------------------- Agent 1: Cumulative Monthly -------------------------
def get_monthly_timeline(description):
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
    response = chain.invoke({"description": description})

    try:
        json_str = re.search(r"\{.*\}", response.content, re.DOTALL).group()
        durations = json.loads(json_str)
    except Exception as e:
        st.error("❌ JSON Parsing Error")
        st.code(response.content)
        return None, None

    cumulative = {}
    total = 0
    for phase, dur in durations.items():
        total += dur
        cumulative[phase] = total

    return durations, cumulative

def visualize_monthly_timeline(cumulative):
    fig, ax = plt.subplots()
    labels = list(cumulative.keys())
    values = list(cumulative.values())

    bars = ax.bar(labels, values, color="mediumseagreen")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height} mo', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    ax.set_ylabel("Cumulative Time (Months)")
    ax.set_title("Startup Timeline (Cumulative Months)")
    st.pyplot(fig)

# ------------------------- Agent 2: Weekly Simulation -------------------------
def build_weekly_prompt(idea, weeks):
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

def parse_and_plot_weekly(json_data, weeks):
    fig, ax = plt.subplots(figsize=(10, 5))
    today = datetime.date.today()

    for item in json_data:
        phase = item["phase"]
        start = today + datetime.timedelta(weeks=item["start_week"] - 1)
        duration = datetime.timedelta(weeks=item["duration_weeks"])
        ax.barh(phase, duration.days, left=start.toordinal(), height=0.5)

    ax.set_xlabel("Date")
    ax.set_ylabel("Phase")
    ax.set_title(f"Startup Timeline (Next {weeks} Weeks)")
    ax.set_yticks(range(len(json_data)))
    ax.set_yticklabels([item["phase"] for item in json_data])
    ax.set_xlim(today.toordinal(), (today + datetime.timedelta(weeks=weeks)).toordinal())
    ax.set_xticks([today.toordinal() + 7 * i for i in range(weeks)])
    ax.set_xticklabels([(today + datetime.timedelta(weeks=i)).strftime('%b %d') for i in range(weeks)], rotation=45)
    st.pyplot(fig)

# ------------------------- Agent Execution -------------------------
if api_key:
    if agent_choice == "Cumulative Monthly Timeline" and startup_idea.strip():
        if st.button("📅 Estimate Monthly Timeline"):
            with st.spinner("Calling Gemini..."):
                durations, cumulative = get_monthly_timeline(startup_idea)
            if durations and cumulative:
                st.subheader("📄 Phase Durations")
                st.json(durations)
                st.subheader("🕒 Cumulative Timeline")
                st.json(cumulative)
                st.subheader("📈 Visual Timeline")
                visualize_monthly_timeline(cumulative)

    elif agent_choice == "Weekly Phase Simulation" and startup_idea.strip():
        week_range = st.slider("📆 Timeline Range (Weeks)", 12, 24, 16)
        if st.button("🚀 Simulate Weekly Timeline"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = build_weekly_prompt(startup_idea, week_range)
                response = model.generate_content(prompt)
                content = response.text

                json_match = re.search(r"\[.*\]", content, re.DOTALL)
                if json_match:
                    timeline_data = json.loads(json_match.group())
                    st.subheader("📄 Timeline Data")
                    st.json(timeline_data)
                    st.subheader("📊 Visual Timeline")
                    parse_and_plot_weekly(timeline_data, week_range)
                else:
                    st.error("❌ Could not parse JSON timeline")
                    st.code(content)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif agent_choice == "Commitment Analyzer":
        lifestyle = st.text_area("👤 Describe your current lifestyle", height=100)
        startup = st.text_area("🚀 Describe your startup idea", height=100)
        if st.button("🧠 Analyze Feasibility") and lifestyle.strip() and startup.strip():
            with st.spinner("Analyzing feasibility with Gemini..."):
                agent = GeminiRAGAgent()
                result = agent.analyze(lifestyle, startup)
            st.success("📊 Feasibility Analysis")
            st.write(result)
