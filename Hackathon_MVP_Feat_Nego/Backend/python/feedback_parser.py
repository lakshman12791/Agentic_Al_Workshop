# import json
# import os
# import re
# from tqdm import tqdm
# from dotenv import load_dotenv
# from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import CharacterTextSplitter

# # Load environment variables (or hardcoded key)
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo"
# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY not found.")

# # Load taxonomy
# with open("feedback_taxonomy.json", "r") as f:
#     taxonomy = json.load(f)

# # Load feedback lines
# with open("feedback_details.txt", "r") as f:
#     feedback_entries = [line.strip() for line in f if line.strip()]

# # Build taxonomy text for embedding
# taxonomy_text = "\n".join([f"{item['feature']} ({item['need']})" for item in taxonomy])

# # Create document chunks
# text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
# docs = text_splitter.create_documents([taxonomy_text])

# # Embed and setup retriever
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
# db = FAISS.from_documents(docs, embeddings)
# retriever = db.as_retriever()

# # Setup Gemini LLM with RAG
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=GOOGLE_API_KEY)
# rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)

# # Process and store structured outputs
# structured_outputs = []
# print("🔍 Processing feedback entries...")

# for feedback in tqdm(feedback_entries):
#     prompt = f"""You are extracting structured data for product analysis from feedback.
# Feedback: "{feedback}"

# Using the reference taxonomy, extract structured information in JSON:
# [
#   {{
#     "feature": "string",
#     "need": "string",
#     "desirability_score": int (1 to 10)
#   }}
# ]
# If no relevant match, return an empty list.
# """
#     try:
#         response = rag_chain.run(prompt)
#         match = re.search(r"\[.*?\]", response, re.DOTALL)
#         if match:
#             json_output = json.loads(match.group(0))
#             if isinstance(json_output, list):
#                 structured_outputs.extend(json_output)
#         else:
#             print("⚠️ No JSON found:", response)

#     except Exception as e:
#         print("❌ Error for:", feedback)
#         print("   ➤", str(e))

# # Save structured output
# output_path = "structured_results.json"
# os.makedirs(os.path.dirname(output_path), exist_ok=True)
# with open(output_path, "w") as f:
#     json.dump(structured_outputs, f, indent=2)

# print(f"✅ Extracted {len(structured_outputs)} items. Saved to: {output_path}")


import json
import os
import re
from typing import List, Dict
from tqdm import tqdm
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS  # Changed import
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import CharacterTextSplitter
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_env_vars() -> str:
    """Load and validate Google API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or "YOUR_DEFAULT_API_KEY"
    if not api_key or api_key == "YOUR_DEFAULT_API_KEY":
        raise ValueError("GOOGLE_API_KEY is required. Set it in .env or environment variables.")
    return api_key

def load_taxonomy(file_path: str) -> List[Dict]:
    """Load and validate taxonomy JSON file."""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            taxonomy = json.load(f)
        if not isinstance(taxonomy, list):
            raise ValueError("Taxonomy must be a list of dictionaries")
        return taxonomy
    except FileNotFoundError:
        logger.error(f"Taxonomy file not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in taxonomy file: {file_path}")
        raise

def load_feedback(file_path: str) -> List[str]:
    """Load and clean feedback entries from text file."""
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"Feedback file not found: {file_path}")
        raise

def setup_rag_chain(api_key: str) -> RetrievalQA:
    """Setup RAG chain with embeddings and retriever."""
    try:
        # Create document chunks
        text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        docs = text_splitter.create_documents([taxonomy_text])
        
        # Setup embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        db = FAISS.from_documents(docs, embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 3})
        
        # Setup LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=api_key
        )
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False
        )
    except Exception as e:
        logger.error(f"Failed to setup RAG chain: {str(e)}")
        raise

def process_feedback(feedback: str, rag_chain: RetrievalQA) -> List[Dict]:
    """Process a single feedback entry and return structured output."""
    prompt = f"""Extract structured data for product analysis from feedback.
Feedback: "{feedback}"

Using the reference taxonomy, return JSON:
[
  {{
    "feature": "string",
    "need": "string",
    "desirability_score": int (1 to 10)
  }}
]
Return an empty list if no relevant match is found.
Ensure the output is valid JSON.
"""
    try:
        response = rag_chain.invoke({"query": prompt})["result"]
        # Extract JSON from response
        match = re.search(r'\[.*?\]', response, re.DOTALL)
        if match:
            json_output = json.loads(match.group(0))
            if isinstance(json_output, list):
                # Validate each item in the output
                for item in json_output:
                    if not all(key in item for key in ["feature", "need", "desirability_score"]):
                        logger.warning(f"Invalid structure in JSON output: {item}")
                        return []
                    if not isinstance(item["desirability_score"], int) or not 1 <= item["desirability_score"] <= 10:
                        logger.warning(f"Invalid desirability score: {item}")
                        return []
                return json_output
        return []
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON in response for feedback: {feedback}")
        return []
    except Exception as e:
        logger.error(f"Error processing feedback: {feedback}\n{str(e)}")
        return []

def main():
    """Main function to process feedback and generate structured output."""
    try:
        # Load configurations
        api_key = load_env_vars()
        taxonomy = load_taxonomy("feedback_taxonomy.json")
        feedback_entries = load_feedback("feedback_details.txt")
        
        # Build taxonomy text for embedding
        global taxonomy_text
        taxonomy_text = "\n".join([f"{item['feature']} ({item['need']})" for item in taxonomy])
        
        # Setup RAG chain
        rag_chain = setup_rag_chain(api_key)
        
        # Process feedback entries
        structured_outputs = []
        logger.info("Processing feedback entries...")
        
        for feedback in tqdm(feedback_entries, desc="Processing feedback"):
            result = process_feedback(feedback, rag_chain)
            structured_outputs.extend(result)
        
        # Save results
        output_path = "structured_results.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(structured_outputs, f, indent=2)
        
        logger.info(f"Extracted {len(structured_outputs)} items. Saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()