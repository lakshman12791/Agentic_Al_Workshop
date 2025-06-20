import json
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

prompt_template = PromptTemplate.from_template("""
You are a Feasibility Assessment Agent.
Evaluate the following feature for feasibility based on:

1. Technical constraints (e.g., AI usage, DB availability, platform support)
2. Development time (if >30 days, it's a risk)
3. Team availability

Input feature JSON:
{feature}

Output JSON Format:
{{
  "feature_name": "<name>",
  "feasibility_score": <0-100>,
  "risk_flags": ["<risk1>", "<risk2>"],
  "high_risk": <true|false>
}}

Assess at least 70% of relevant constraints and flag high-risk features.
""")

# Initialize LLM and Parser (can be done globally if they are stateless)
parser = JsonOutputParser()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo",
    temperature=0.3,
)

def assess_feasibility(input_features_list: list) -> list:
   
    results = []
    for feature_data in input_features_list:
        try:
            prompt_filled = prompt_template.format(feature=json.dumps(feature_data))
            output = llm.invoke(prompt_filled)
            parsed = parser.invoke(output)
            results.append(parsed)
        except Exception as e:
            print(f"Error assessing feasibility for feature {feature_data.get('feature', 'Unknown')}: {e}")
            # Optionally, append an error object or skip
            results.append({"feature_name": feature_data.get('feature', 'Unknown'), "error": str(e), "feasibility_score": 0, "high_risk": True, "risk_flags": ["Processing Error"]})
    return results

if __name__ == "__main__":
    # Example usage for standalone testing
    sample_features = [
        {"feature": "User Authentication", "description": "Implement OAuth 2.0 for user login.", "user_stories": ["As a user, I want to log in securely."]},
        {"feature": "Dashboard Display", "description": "Show key metrics on the main dashboard.", "complexity": "medium"}
    ]
    feasibility_results = assess_feasibility(sample_features)
    print(json.dumps(feasibility_results, indent=2))