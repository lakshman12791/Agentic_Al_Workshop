# Feedback Processing API

This Node.js/Express application provides an API endpoint for uploading and processing feedback JSON files. It integrates with a Python script to analyze the uploaded data and return structured results.

## Features

- Accepts JSON files via a POST upload
- Validates uploaded file format
- Passes data to a Python script for processing
- Returns structured JSON response
- Retrieves feedback taxonomy metadata
- Temporary file handling and cleanup

---

## Project Structure

```
server/
├── src/
│   └── routes/
│       └── feedback.js        # Express router for file upload and Python execution
├── temp_files/                # Temporary files created during processing
└── python/
    ├── main.py                # Python script for processing feedback
    └── feedback_taxonomy.json# JSON taxonomy used by Python
```

---

## Requirements

### Node.js

- `express`
- `multer`
- `fs/promises`
- `child_process`
- `path`

Install dependencies:

```bash
npm install express multer
```

### Python

Ensure `python3` is available and required packages are installed for `main.py`.

---

## API Endpoints

### `POST /upload`

Uploads a JSON file and processes it using the Python script.

- **Form field:** `feedback` (JSON file only)
- **Content-Type:** `multipart/form-data`
- **Response:**
  ```json
  {
    "success": true,
    "message": "File uploaded and processed successfully",
    "data": {
      "filename": "input.json",
      "size": 2345,
      "pythonResult": { ... }
    }
  }
  ```

### `GET /results`

Returns the `feedback_taxonomy.json` content.

- **Response:**
  ```json
  {
    "category1": {
      "subcategories": [...]
    },
    ...
  }
  ```

---

## Error Handling

- Returns `400` if no file or invalid file type.
- Returns `500` on Python script failure or read errors.
- Logs all Python `stdout` and `stderr` for debugging.

---

## Notes

- Only `.json` files are allowed.
- Maximum file size is 10MB.
- Temporary files are stored in `server/temp_files/` and automatically deleted after processing.
- Python script path is hardcoded; update `pythonScriptPath` in `feedback.js` if needed.

---

## Development Tips

- Run the Node.js server with:
  ```bash
  node server.js
  ```

- Test the upload using Postman or cURL:
  ```bash
  curl -X POST -F "feedback=@sample_feedback.json" http://localhost:3000/upload
  ```

---

## License

MIT


# BaseAgent using Langchain

This project defines a `BaseAgent` class utilizing the [Langchain](https://docs.langchain.com/) framework. The agent is designed to wrap a language model with a customizable system prompt and accept user input for inference.

## 🧠 Overview

`BaseAgent` is a lightweight agent wrapper that:
- Accepts a language model (LLM) instance.
- Accepts a system-level prompt to guide responses.
- Uses Langchain's `ChatPromptTemplate` to format inputs.
- Allows users to invoke the LLM with dynamic input using a simple interface.

## 📦 Dependencies

Install the required dependencies using pip:

```bash
pip install langchain langchain-core
```

> ⚠️ You must also install a compatible LLM integration (e.g., OpenAI, Google Generative AI, etc.).

## 🚀 Usage

```python
from langchain.chat_models import ChatOpenAI
from your_module import BaseAgent  # Adjust import path accordingly

# Initialize your LLM (example with OpenAI)
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Define a system prompt
system_prompt = "You are an expert assistant that helps developers with coding questions."

# Create the agent
agent = BaseAgent(llm, system_prompt)

# Run the agent with user input
response = agent.run("How do I sort a list in Python?")
print(response)


# Feedback Parser Agent

## Overview

The **FeedbackParserAgent** is a LangChain-based agent that processes raw user feedback and extracts structured information using Retrieval-Augmented Generation (RAG). It aligns extracted features with industry-standard taxonomies to ensure consistency and relevance.

## Features

- Extracts features and their descriptions from unstructured feedback.
- Assigns a desirability score out of 10.
- Includes original feedback in the output.
- Uses RAG to reference taxonomy standards for accurate parsing.

## Output Format

The output is a JSON object:
```json
{
  "feature": "string",
  "description": "string",
  "desirability_score": 8,
  "source_feedback": "original feedback text"
}


# 🧠 Feasibility Assessment Agent

This agent evaluates software features for feasibility based on technical constraints, estimated development time, and team availability. It leverages Google's Gemini LLM (via LangChain) to assess risks and assign a feasibility score to each feature.

---

## 📌 Features

- Analyzes technical feasibility of product features
- Flags high-risk elements (e.g., platform mismatch, long dev cycles)
- Outputs structured JSON with:
  - `feature_name`
  - `feasibility_score` (0–100)
  - `risk_flags` (array of strings)
  - `high_risk` (boolean)

---

## 🛠️ Technologies Used

- Python
- [LangChain](https://www.langchain.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- JSON Output Parsing

# Viability Scoring Agent

## Overview

The **Viability Scoring Agent** is a Langchain-based AI agent designed to evaluate the business viability of product features. It scores features based on:

- **Revenue Potential** (40%)
- **Market Differentiation** (30%)
- **Strategic Alignment** (30%)

It provides a breakdown of the scoring and explains how the feature aligns with overall business goals and the competitive landscape.

---

## Features

- Accepts structured input for feature details and business context.
- Produces structured output with a viability score, category-wise breakdown, and strategic fit analysis.
- Customizable scoring weights based on context.

---

## File Structure

- `viability_agent.py`: Contains the `ViabilityInput`, `ViabilityOutput`, and `ViabilityAgent` classes.
- `base_agent.py`: Abstract base class to handle common prompt and LLM invocation logic.

---

## Class Details

### `ViabilityInput`

| Field              | Type   | Description                            |
|-------------------|--------|----------------------------------------|
| `feature`         | str    | Name of the feature                    |
| `description`     | str    | Description of the feature             |
| `business_context`| str    | Context including business goals       |

### `ViabilityOutput`

| Field              | Type   | Description                                        |
|-------------------|--------|----------------------------------------------------|
| `feature`         | str    | Evaluated feature name                            |
| `viability_score` | float  | Score between 0-10                                |
| `breakdown`       | dict   | Detailed scoring breakdown by category            |
| `strategic_fit`   | str    | Analysis of how the feature fits into strategy    |

---

## Usage

```python
from viability_agent import ViabilityAgent

# Initialize agent with LLM (e.g., ChatGoogleGenerativeAI, OpenAI)
agent = ViabilityAgent(llm)

# Define input
feature_data = {
    "feature": "Smart Recommendations",
    "description": "AI-driven suggestions for users based on browsing history"
}

business_context = {
    "goals": "Increase user engagement and time-on-site",
    "competition": "Competitors have basic recommendation systems",
    "weights": {
        "revenue": 50,
        "differentiation": 25,
        "alignment": 25
    }
}

# Run the agent
result = agent.run(feature_data, business_context)

# Output: ViabilityOutput object
print(result)


# 📌 Feature Prioritization Agent

The **Feature Prioritization Agent** is a LangChain-based AI agent that categorizes features into MVP and Post-MVP buckets by evaluating desirability, feasibility, and viability. It uses a modified **RICE** model along with strategic business constraints.

---

## 🚀 Purpose

This agent helps product managers and startup teams prioritize features for development using:
- User desirability
- Technical feasibility
- Business viability
- Strategic constraints like team capacity, deadlines, and must-have requirements

---

## 🧠 How It Works

### 1. Input
- A list of scored features with:
  - `desirability`: how much users want the feature
  - `feasibility`: technical ease/complexity
  - `viability`: business impact and alignment
- Constraints including:
  - `mvp_timeframe`: how many weeks are available for MVP development
  - `team_capacity`: number of person-weeks available
  - `must_have_features`: mandatory features regardless of score

### 2. Logic
The agent applies the following prioritization rules:
- **RICE model**: Reach × Impact × Confidence / Effort (implicitly adapted to DFV scoring)
- Auto-selects features with score > 24/30
- Enforces must-have features even if scores are lower
- Considers technical dependencies
- Balances quick wins vs long-term investment

### 3. Output
Structured JSON response:
```json
{
  "mvp_features": [...],
  "post_mvp_features": [...],
  "tradeoffs": "Explanation of decisions and dependencies"
}


# Blueprint Agent

The **BlueprintAgent** is a LangChain-powered autonomous agent designed to generate a comprehensive MVP blueprint for software projects. It functions as a Technical Architect, processing prioritized features and contextual system data to output a complete development blueprint including architecture, KPIs, resource plan, and risks.

---

## 🔧 Features

- ✅ Generates MVP feature list with acceptance criteria
- 🏗️ Creates technical architecture in **Mermaid.js** syntax
- 📊 Assigns KPIs (business and technical) to each feature
- 👥 Recommends team structure and resource allocation
- ⚠️ Identifies implementation risks with mitigation strategies
- 🔍 Explains excluded features and trade-offs

---

## 🧠 Agent Role

```text
You're a Technical Architect. Generate MVP blueprint with:
1. Feature Specifications: Clear acceptance criteria
2. Tech Stack: <provided> with justification for any additions
3. Architecture Diagram: Mermaid.js syntax for visualization
4. KPIs: Business and technical metrics per feature
5. Resource Plan: Roles needed (FE, BE, QA, etc.)
6. Risk Register: Technical and operational risks
7. Trade-off Log: Why features were excluded


# 🧭 TransitionPlanner Agent

The `TransitionPlanner` is a LangChain-based agent that generates a strategic transition plan for a product based on its blueprint and business context. It helps define a phased rollout roadmap, integrates feedback loops, outlines success metrics, and plans for post-MVP iterations.

## 📌 Features

- **Phase-Based Roadmap:** Plans the MVP launch, initial iterations, and scaling phase.
- **Feedback Integration:** Recommends tools and processes for user feedback collection and improvement.
- **Success Metrics:** Specifies business and technical metrics to track post-launch.
- **Iteration Planning:** Defines a strategy for future feature development and technical evolution.

## 🧱 Dependencies

- `langchain`
- `langchain-core`
- `pydantic_v1`

## 🧩 Class Structure

### `TransitionOutput`

Pydantic model specifying the output schema:
- `roadmap`: List — Phased rollout plan.
- `feedback_loops`: Dict — Feedback collection and improvement process.
- `success_metrics`: Dict — Metrics for business and technical success.
- `iteration_plan`: Dict — Plan for post-MVP feature rollout and evolution.

### `TransitionPlanner`

Inherits from `BaseAgent`.

- **System Prompt:** Instructs the LLM to act as a Product Strategist and generate:
  - Roadmap with time phases
  - Feedback integration plan
  - Success metrics (business + technical)
  - Post-MVP feature planning

- **Constructor**:
  ```python
  def __init__(self, llm):
      super().__init__(llm, self.SYSTEM_PROMPT, TransitionOutput)
