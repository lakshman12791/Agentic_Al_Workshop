import json
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

# 1. Load input JSON
with open("input_features.json", "r") as f:
    input_data = json.load(f)

features = input_data.get("features", [])

# 2. Define prompt template
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

# 3. Output parser
parser = JsonOutputParser()

# 4. Load LLM (Google Gemini, replace with OpenAI if needed)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyCp8H9Ihvgujw76b56eIVQOAK8Jr92YBpo",
    temperature=0.3,
)

# 5. Run for each feature
results = []
for feature in features:
    prompt = prompt_template.format(feature=json.dumps(feature))
    output = llm.invoke(prompt)
    parsed = parser.invoke(output)
    results.append(parsed)

# 6. Output result
with open("feasibility_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
