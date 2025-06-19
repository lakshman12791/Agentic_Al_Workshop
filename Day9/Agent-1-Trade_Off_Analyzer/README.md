# 🚀 Startup Timeline Agent

A **Streamlit** web app that uses **Gemini (Google Generative AI)** to generate a realistic timeline for startup development phases like **MVP**, **Launch**, and **PMF** based on a given project description. The tool visualizes the output in both JSON and bar chart format.

---

## ✨ Features

- Accepts a detailed startup idea as input.
- Calls **Gemini 1.5 Flash** model to compute realistic time estimates for each startup phase.
- Parses and displays JSON data showing individual and cumulative timelines.
- Visualizes cumulative timeline using **Matplotlib** bar charts.

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- Matplotlib

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/startup-timeline-agent.git
   cd startup-timeline-agent
   ```

2. **Install Dependencies**

   It's recommended to use a virtual environment.

   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt`** (you can create this file):

   ```txt
   streamlit
   matplotlib
   langchain
   langchain-google-genai
   ```

3. **Set the Google API Key**

   Replace the placeholder API key in the code or set it via environment variable:

   ```bash
   export GOOGLE_API_KEY=your_actual_key_here
   ```

   Or modify the code in `main.py`:

   ```python
   os.environ["GOOGLE_API_KEY"] = "your_actual_key_here"
   ```

4. **Run the App**

   ```bash
   streamlit run main.py
   ```

---

## 🖼️ UI Preview

- 📝 Enter a project idea
- 🔮 Get estimated phase durations via Gemini
- 📈 View cumulative phase timelines visually

---

## 🔒 Important Note

- Make sure **not to expose your API Key** in production code.
- Consider loading it via `.env` file and using `python-dotenv`.

---

## 📜 License

MIT License

---

## 🙋‍♂️ Author

Lakshman — Full Stack Developer | AI Explorer  
[LinkedIn](https://www.linkedin.com/) | [GitHub](https://github.com/)
