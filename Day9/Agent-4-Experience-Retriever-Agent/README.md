
# 📖 Experience Retriever Agent

This project is a Streamlit-based application that leverages Google's Gemini API and LangChain's RAG (Retrieval-Augmented Generation) capabilities to answer startup-related queries using real founder stories from IndieHackers, Y Combinator blogs, and other sources.

---

## 🚀 Features

- Ask natural language questions about startup timelines and milestones.
- Dynamically filters sources like IndieHackers, YC, and Blog.
- Uses vector search (FAISS) and Google Gemini LLM for accurate results.
- Includes example startup stories for semantic retrieval.

---

## 🧱 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── retriever.py           # Optional separate retriever logic
├── startup_stories.json   # Dataset of startup journey summaries
```

---

## 🔧 Requirements

- Python 3.8+
- Streamlit
- LangChain
- Google Generative AI
- FAISS

Install all dependencies:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:
```text
streamlit
langchain
faiss-cpu
google-generativeai
```

---

## 🔑 Setup

1. Get your **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/).
2. Place it in the app UI when prompted.
3. Ensure the `startup_stories.json` file is in the `data/` folder.

Directory should look like:

```
.
├── app.py
├── retriever.py
├── data/
│   └── startup_stories.json
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Once the app launches:

1. Paste your **Gemini API Key**.
2. Choose a **source filter**.
3. Ask a question like:

```
How long did it take Airbnb to get into YC?
What were the challenges faced by Flipkart?
When did Apple launch their first product?
```

---

## 📦 Notes

- `retriever.py` includes a modular version of retriever logic using `.txt` format. The `app.py` uses `json` input directly.
- The app uses `langchain.vectorstores.FAISS` and `GoogleGenerativeAIEmbeddings` for vector search.
- You can extend the dataset by adding more entries to `startup_stories.json`.

---

## 📄 License

MIT License — Free to use and modify.
