
# 🧠 Gemini Startup Analyzer

The **Gemini Startup Analyzer** is a Streamlit web application that evaluates the feasibility of a startup idea based on the founder’s current lifestyle and commitment potential. It leverages Google's Gemini AI model for contextual analysis and feedback.

## 🚀 Features

- Accepts user input for:
  - Current lifestyle (e.g., job, studies, family obligations)
  - Startup idea
- Uses Gemini AI to analyze and return realistic insights on:
  - Timeline feasibility
  - Commitment expectations
  - Startup practicality
- Simple UI built with Streamlit
- Modular backend via a custom GeminiRAGAgent

## 🧩 Project Structure

```
.
├── app.py                  # Streamlit frontend for UI interaction
├── agent.py                # GeminiRAGAgent with Google Generative AI integration
```

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gemini-startup-analyzer.git
cd gemini-startup-analyzer
```

### 2. Install Requirements

Make sure you have Python 3.8+ and pip installed.

```bash
pip install streamlit google-generativeai
```

### 3. Run the App

```bash
streamlit run app.py
```

## 🔐 Configuration

On running the app, you will be prompted to input your **Gemini API Key**. This is used to authenticate with Google Generative AI.

You can obtain your key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

## 🧠 Powered By

- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)

## 📄 License

This project is licensed under the MIT License.
