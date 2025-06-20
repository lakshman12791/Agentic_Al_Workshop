from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from base_agent import BaseAgent

class TransitionOutput(BaseModel):
    roadmap: list = Field(description="Phased rollout plan")
    feedback_loops: dict = Field(description="User feedback mechanisms")
    success_metrics: dict = Field(description="Post-launch measurement plan")
    iteration_plan: dict = Field(description="v1.1 feature planning")

class TransitionPlanner(BaseAgent):
    SYSTEM_PROMPT = """You're a Product Strategist. Create transition plan with:
    1. Phase-based Roadmap:
        - MVP Launch: T0-T{timeframe}
        - Iteration 1: T{timeframe+1}-T{timeframe+4}
        - Scaling Phase: T{timeframe+5}+
    
    2. Feedback Integration:
        - User analytics tools
        - Feedback collection mechanisms
        - Continuous improvement process
    
    3. Success Metrics:
        - Business metrics: {business_metrics}
        - Technical metrics: {technical_metrics}
    
    4. Post-MVP Evolution:
        - Feature pipeline management
        - Technical debt repayment plan
        - Scaling strategy"""

    def __init__(self, llm):
        super().__init__(llm, self.SYSTEM_PROMPT, TransitionOutput)
        
    def run(self, blueprint: dict, context: dict):
        input_str = (
            f"Blueprint Summary:\n{blueprint['summary']}\n\n"
            f"Business Goals:\n{context['goals']}\n"
            f"Time Constraints:\n{context['timeframe']} weeks"
        )
        return super().run(input_str)