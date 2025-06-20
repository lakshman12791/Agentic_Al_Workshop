import json
import os
from tqdm import tqdm
from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()
GOOGLE_API_KEY = "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"

# Load and prepare industry taxonomy
with open("feedback_taxonomy.json") as f:
    taxonomy = json.load(f)

# Load feedback entries
with open("feedback_details.txt") as f:
    feedback_entries = [line.strip() for line in f if line.strip()]

# Prepare feature reference text
taxonomy_text = ""
for category, data in taxonomy.items():
    for feature in data["subcategories"]:
        taxonomy_text += f"{feature} ({category})\n"

# Create embeddings from taxonomy for reference
text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
docs = text_splitter.create_documents([taxonomy_text])

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
db = FAISS.from_documents(docs, embeddings)
retriever = db.as_retriever()

# Gemini for RAG
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GOOGLE_API_KEY)
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)

structured_outputs = []

print("Processing feedback entries...")
for feedback in tqdm(feedback_entries):
    prompt = f"""You are extracting structured data for product analysis from feedback.
Feedback: "{feedback}"

Using the reference taxonomy, extract structured information in JSON:
[
  {{
    "feature": "string",
    "need": "string",
    "desirability_score": int (1 to 10)
  }}
]
If no relevant match, return an empty list.
"""
    try:
        response = rag_chain.run(prompt)
        json_output = json.loads(response)
        if isinstance(json_output, list):
            structured_outputs.extend(json_output)
    except Exception as e:
        print("Error parsing:", feedback, e)

# Save results
with open("structured_results.json", "w") as f:
    json.dump(structured_outputs, f, indent=2)

print(f"✅ Extracted {len(structured_outputs)} structured features. Saved to structured_results.json")
