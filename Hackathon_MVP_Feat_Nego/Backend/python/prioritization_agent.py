from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from base_agent import BaseAgent

def prioritize_features(input_features_list: list) -> list:


    class FeatureScore(BaseModel):
        feature: str = Field(description="Feature name")
        desirability: float = Field(description="User desirability score")
        feasibility: float = Field(description="Technical feasibility score")
        viability: float = Field(description="Business viability score")
        total_score: float = Field(description="Calculated total score")

    class PrioritizationOutput(BaseModel):
        mvp_features: List[FeatureScore] = Field(description="Features for MVP phase")
        post_mvp_features: List[FeatureScore] = Field(description="Features for future phases")
        tradeoffs: str = Field(description="Prioritization rationale and tradeoffs")

    class PrioritizationAgent(BaseAgent):
        SYSTEM_PROMPT = """You're a Product Prioritization Expert. Apply the RICE scoring model:
        Reach * Impact * Confidence / Effort
        
        Constraints:
        - MVP timeframe: {mvp_timeframe} weeks
        - Team capacity: {team_capacity} person-weeks
        - Must-have features: {must_have_features}
        
        Prioritization Rules:
        1. Features scoring >24/30 automatically qualify for MVP
        2. Must-have features override scoring if strategically critical
        3. Consider technical dependencies between features
        4. Balance quick wins vs strategic investments
        
        Output clear MVP vs Post-MVP categorization with justification."""

        def __init__(self, llm):
            super().__init__(llm, self.SYSTEM_PROMPT, PrioritizationOutput)
            
        def run(self, scored_features: list, constraints: dict):
            features_str = "\n".join([
                f"- {f['feature']}: D={f['desirability']}, F={f['feasibility']}, V={f['viability']}"
                for f in scored_features
            ])
            
            input_str = f"Scored Features:\n{features_str}\n\nConstraints:\n{constraints}"
            return super().run(input_str)