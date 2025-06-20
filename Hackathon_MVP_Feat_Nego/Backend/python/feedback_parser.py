

from langchain_core.prompts import ChatPromptTemplate

class BaseAgent:
    def __init__(self, llm, system_prompt):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}")
        ])
        self.chain = self.prompt | llm
        
    def run(self, input_data):
        return self.chain.invoke({"input": input_data})
    
class FeedbackParserAgent(BaseAgent):
    SYSTEM_PROMPT = """You're a Feedback Parser Agent. Extract features from input using industry taxonomies.
    Context: {rag_context}
    Output JSON format: {{ "feature": "...", "description": "...", "desirability_score": X/10, "source_feedback": "..." }}"""

    def __init__(self, llm, rag):
        # Update the prompt template to include rag_context
        self.rag = rag
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("user", "{input}")
        ])
        self.chain = self.prompt | llm

    def run(self, feedback: str):
        rag_context = self.rag.retrieve("feature taxonomy standards")
        return self.chain.invoke({
            "input": feedback,
            "rag_context": rag_context
        })