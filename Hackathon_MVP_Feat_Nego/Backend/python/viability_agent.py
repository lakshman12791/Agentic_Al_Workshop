from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from base_agent import BaseAgent

def score_viability(input_features_list: list) -> list:


    class ViabilityInput(BaseModel):
        feature: str = Field(description="Feature name to evaluate")
        description: str = Field(description="Feature description")
        business_context: str = Field(description="Business goals and context")

    class ViabilityOutput(BaseModel):
        feature: str = Field(description="Evaluated feature name")
        viability_score: float = Field(description="Score from 0-10")
        breakdown: dict = Field(description="Score breakdown by category")
        strategic_fit: str = Field(description="Alignment with business strategy")

    class ViabilityAgent(BaseAgent):
        SYSTEM_PROMPT = """You're a Business Viability Analyst. Evaluate features based on:
        - Revenue Potential (40% weight): {revenue_weight}%
        - Market Differentiation (30% weight): {differentiation_weight}%
        - Strategic Alignment (30% weight): {alignment_weight}%
        
        Business Goals:
        {business_goals}
        
        Competitive Landscape:
        {competitive_landscape}
        
        Output must include detailed breakdown and strategic fit analysis."""

        def __init__(self, llm):
            super().__init__(llm, self.SYSTEM_PROMPT, ViabilityOutput)
            
        def run(self, feature_data: dict, business_context: dict):
            # Configure weights from context or use defaults
            weights = business_context.get("weights", {
                "revenue": 40,
                "differentiation": 30,
                "alignment": 30
            })
            
            prompt = PromptTemplate.from_template(
                "Feature: {feature}\nDescription: {description}\n\nBusiness Context:\n{context}"
            )
            input_str = prompt.format(
                feature=feature_data["feature"],
                description=feature_data["description"],
                context=business_context
            )
            
            # Format system prompt with weights
            system_prompt = self.SYSTEM_PROMPT.format(
                revenue_weight=weights["revenue"],
                differentiation_weight=weights["differentiation"],
                alignment_weight=weights["alignment"],
                business_goals=business_context.get("goals", ""),
                competitive_landscape=business_context.get("competition", "")
            )
            
            return super().run(input_str, system_prompt=system_prompt)
        

        