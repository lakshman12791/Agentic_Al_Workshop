from fastapi import FastAPI, File, UploadFile
from feasibility_score import assess_feasibility
from viability_agent import score_viability
from prioritization_agent import prioritize_features
from blueprint_generator import generate_blueprint
from transition_planner import create_transition_plan
from feedback_parser import parse_feedback
from utils.file_parser import parse_uploaded_file
import json
import google.generativeai as genai

app = FastAPI()

# Initialize Gemini (no API key needed for free version)
genai.configure()

async def process_feedback(file: UploadFile = File(...)):
    
    feedback_data = await parse_uploaded_file(file)
    
    parsed_features = parse_feedback(feedback_data)
    feasible_features = assess_feasibility(parsed_features)
    viable_features = score_viability(feasible_features)
    prioritized_features = prioritize_features(viable_features)
    mvp_blueprint = generate_blueprint(prioritized_features)
    transition_plan = create_transition_plan(mvp_blueprint)
        
    return {
        "features": [f.dict() for f in prioritized_features],
        "blueprint": mvp_blueprint.dict(),
        "transition_plan": transition_plan.dict()
    }