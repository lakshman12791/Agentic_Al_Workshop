
# 🧠 Timeline Simulation Agent

This project uses **Gemini AI** and **Streamlit** to simulate a realistic startup timeline over a 12–24 week horizon. It assists founders in planning key phases such as MVP development, Go-To-Market (GTM), Fundraising, and achieving Product-Market Fit (PMF).

## 🚀 Features

- Gemini-powered timeline generation based on your business idea.
- Dynamic range for weekly planning (12–24 weeks).
- Visualized timeline using `matplotlib` in Streamlit.
- Easy-to-use UI for non-technical users.

## 📦 Requirements

- Python 3.8+
- Streamlit
- matplotlib
- google-generativeai

## 🛠️ Installation

```bash
pip install streamlit matplotlib google-generativeai
```

## ▶️ How to Run

1. Clone this repository:
```bash
git clone https://github.com/your-repo/timeline-agent.git
cd timeline-agent
```

2. Run the app:
```bash
streamlit run app.py
```

3. Enter your Gemini API Key and describe your business idea to generate the timeline.

## 🧠 Powered By

- [Google Gemini](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)

## 📌 Sample Prompt

```
Describe your business idea: "An AI platform to automate hiring and onboarding for tech startups."
```

## 🖼️ Example Output

The app will return a horizontal bar graph showing phase durations and expected start times for each startup milestone.

---

© 2025 Timeline Simulation Agent
