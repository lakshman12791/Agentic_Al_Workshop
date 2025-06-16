from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import query_similar_stories
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

class SimInput(BaseModel):
    idea: str
    hours_per_week: int
    experience: str

@app.post("/simulate")
def simulate(input: SimInput):
    estimated_weeks = int(300 / input.hours_per_week)
    return {
        "estimate": f"{estimated_weeks} weeks",
        "message": f"At {input.hours_per_week} hrs/week, MVP ETA = {estimated_weeks} weeks."
    }

class RAGInput(BaseModel):
    query: str

@app.post("/inspiration")
def inspiration(input: RAGInput):
    response = query_similar_stories(input.query)
    return {"result": response}
