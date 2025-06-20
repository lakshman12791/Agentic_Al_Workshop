from base_agent import BaseAgent


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