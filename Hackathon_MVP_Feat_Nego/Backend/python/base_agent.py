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