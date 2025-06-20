from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from base_agent import BaseAgent

def generate_blueprint(input_features_list: list) -> list:


    class BlueprintOutput(BaseModel):
        features: list = Field(description="List of MVP features")
        architecture: str = Field(description="Technical architecture overview")
        kpis: dict = Field(description="Key metrics per feature")
        resource_allocation: dict = Field(description="Team roles and responsibilities")
        risks: list = Field(description="Implementation risks and mitigation")
        excluded_features: list = Field(description="Features not included with reasons")

    class BlueprintAgent(BaseAgent):
        SYSTEM_PROMPT = """You're a Technical Architect. Generate MVP blueprint with:
        1. Feature Specifications: Clear acceptance criteria
        2. Tech Stack: {tech_stack} with justification for any additions
        3. Architecture Diagram: Mermaid.js syntax for visualization
        4. KPIs: Business and technical metrics per feature
        5. Resource Plan: Roles needed (FE, BE, QA, etc.)
        6. Risk Register: Technical and operational risks
        7. Trade-off Log: Why features were excluded
        
        Current System Context:
        {system_context}"""

        def __init__(self, llm):
            super().__init__(llm, self.SYSTEM_PROMPT, BlueprintOutput)
            
        def run(self, prioritized_features: list, context: dict):
            mvp_features = "\n".join([f"- {f['feature']}" for f in prioritized_features['mvp_features']])
            
            input_str = f"MVP Features:\n{mvp_features}\n\nContext:\n{context}"
            return super().run(input_str)