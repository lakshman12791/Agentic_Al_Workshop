from langchain.agents import AgentExecutor
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
    {rag_context}
    Output JSON format: { "feature": "...", "description": "...", "desirability_score": X/10, "source_feedback": "..." }"""

    def __init__(self, llm, rag):
        super().__init__(llm, self.SYSTEM_PROMPT)
        self.rag = rag

    def run(self, feedback: str):
        rag_context = self.rag.retrieve("feature taxonomy standards")
        return super().run({
            "input": feedback,
            "rag_context": rag_context
        })