# server/python/rag_parser.py
import sys
import json
import csv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini model
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo")

# Load industry-standard feature taxonomy
with open('feedback_taxonomy.json', 'r') as f:
    taxonomy = json.load(f)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["feedback", "taxonomy"],
    template="""
    You are a feedback parser extracting user needs, feature requests, and desirability scores.
    Use the provided taxonomy to categorize features accurately.
    For each feedback entry, identify:
    - Feature: The specific feature mentioned (must match taxonomy or be 'Other')
    - Need: The user need or problem described
    - Desirability Score: A score from 0 to 1 based on sentiment (1 = very positive, 0 = very negative)

    Taxonomy: {taxonomy}

    Feedback: {feedback}

    Output in JSON format:
    [
        {
            "feature": "string",
            "need": "string",
            "desirability_score": float
        },
        ...
    ]
    """
)

# Chain setup
chain = prompt_template | llm | StrOutputParser()

def parse_file(input_path):
    feedback_data = []
    
    # Handle different file formats
    if input_path.endswith('.csv'):
        with open(input_path, 'r') as f:
            reader = csv.DictReader(f)
            feedback_data = [row['feedback'] for row in reader if 'feedback' in row]
    elif input_path.endswith('.json'):
        with open(input_path, 'r') as f:
            data = json.load(f)
            feedback_data = [item['feedback'] for item in data if 'feedback' in item]
    else:  # Assume text
        with open(input_path, 'r') as f:
            feedback_data = f.read().splitlines()

    # Process feedback with RAG
    results = []
    for feedback in feedback_data:
        if feedback.strip():
            try:
                output = chain.invoke({
                    "feedback": feedback,
                    "taxonomy": json.dumps(taxonomy)
                })
                parsed = json.loads(output)
                results.extend(parsed)
            except Exception as e:
                print(f"Error processing feedback: {e}")

    return results

def main():
    if len(sys.argv) != 3:
        print("Usage: python rag_parser.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    results = parse_file(input_path)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()