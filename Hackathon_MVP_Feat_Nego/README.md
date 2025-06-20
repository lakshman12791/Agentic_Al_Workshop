
---

## 🔌 Key Components

### 1. **Feedback Upload API**
- Built using Express and Multer.
- Accepts JSON feedback files.
- Forwards data to Python for analysis.

### 2. **Python Analysis Engine**
- Parses uploaded feedback using retrieval-augmented generation (RAG).
- Applies domain-specific taxonomies.
- Returns structured outputs such as feature summaries, desirability scores, and matched taxonomies.

### 3. **LangChain AI Agents**
Each agent specializes in a specific task:

| Agent Name              | Purpose                                               |
|-------------------------|-------------------------------------------------------|
| FeedbackParserAgent     | Extracts features from unstructured feedback          |
| FeasibilityAgent        | Assesses technical implementation risk                |
| ViabilityAgent          | Evaluates business impact and strategic fit           |
| PrioritizationAgent     | Ranks features based on composite scores              |
| BlueprintAgent          | Generates MVP architecture and KPIs                   |
| TransitionPlannerAgent  | Creates phased rollout plans and feedback loops       |


# 🤖 AI Agents Summary – Feedback Intelligence System

This document provides a high-level overview of the core LangChain-based AI agents used in the Feedback Intelligence System. Each agent performs a specific function in the feedback-to-feature-to-roadmap pipeline, supporting product teams in making data-driven decisions.

---

## 🧠 Feedback Parser Agent

- Extracts meaningful features and descriptions from raw, unstructured user feedback.
- Assigns a desirability score (0–10) and includes the original feedback for traceability.
- Utilizes domain-specific taxonomy via RAG (Retrieval-Augmented Generation).

---

## ⚙️ Feasibility Assessment Agent

- Evaluates the technical feasibility of implementing a proposed feature.
- Assesses risks related to tech stack, timeline, and platform compatibility.
- Outputs a feasibility score with detailed risk flags and high-risk indicators.

---

## 📈 Viability Scoring Agent

- Analyzes business viability based on revenue potential, market differentiation, and strategic fit.
- Produces a total score and a breakdown of each scoring category.
- Aligns feature evaluation with overall business objectives and competitive positioning.

---

## 🎯 Feature Prioritization Agent

- Prioritizes features using a composite score of desirability, feasibility, and viability.
- Applies business constraints like team capacity, timeline, and must-have requirements.
- Classifies features into MVP and post-MVP groups with documented trade-offs.

---

## 🏗️ Blueprint Generator Agent

- Generates a full MVP blueprint with architecture diagrams and acceptance criteria.
- Suggests technical stack, KPIs, team roles, and implementation risks.
- Visualizes system architecture using Mermaid.js and outlines strategic exclusions.

---

## 🧭 Transition Planner Agent

- Designs a phased product rollout based on the generated blueprint.
- Defines feedback loops, success metrics, and post-MVP iteration plans.
- Helps product teams manage scaling and continuous improvement efforts.

---

## 📌 API Endpoints

### `POST /upload`
- Uploads a `.json` feedback file.
- Returns extracted features and scoring results.

### `GET /results`
- Returns the current taxonomy structure used by the agents.

---

## 🛠️ Requirements

### Node.js
- Express, Multer, child_process, etc.

### Python
- LangChain, Pydantic, and an LLM connector (OpenAI, Gemini, etc.)

---

## 🧪 How to Use

1. Start the Node.js server.
2. Use Postman or cURL to POST a feedback file.
3. Receive structured analysis in the response.

---

## 📎 Notes

- Only `.json` files are supported (max 10MB).
- All temporary files are deleted post-processing.
- The Python script path is configured in the backend route logic.

---

## 📜 License

This project is licensed under the SNS Innovation Hub License.

---

## ✨ Credits

Built with 💡 by combining best-in-class AI architecture and developer tooling for startup-grade product intelligence.
