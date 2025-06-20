import streamlit as st
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from feasibility_score import assess_feasibility
from viability_agent import score_viability
from prioritization_agent import prioritize_features
from blueprint_generator import generate_blueprint
from transition_planner import create_transition_plan
from feedback_parser import parse_feedback
from utils.file_parser import parse_uploaded_file
import google.generativeai as genai
import json
import uvicorn
import threading
import time

# Initialize FastAPI
fastapi_app = FastAPI()

# Initialize Gemini
genai.configure()

@fastapi_app.post("/process-feedback")
async def process_feedback(file: UploadFile = File(...)):
    print(f"file: {file}")

    try:
        
        feedback_data = await parse_uploaded_file(file)
        parsed_features = parse_feedback(feedback_data)
        feasible_features = assess_feasibility(parsed_features)
        viable_features = score_viability(feasible_features)
        prioritized_features = prioritize_features(viable_features)
        mvp_blueprint = generate_blueprint(prioritized_features)
        transition_plan = create_transition_plan(mvp_blueprint)
        
        return JSONResponse(content={
            "features": [f.dict() for f in prioritized_features],
            "blueprint": mvp_blueprint.dict(),
            "transition_plan": transition_plan.dict()
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Streamlit interface
def run_streamlit():
    st.set_page_config(page_title="Feedback Processor", layout="wide")
    st.title("Feedback Processing Application")
    st.write("Upload a feedback file to process features, generate blueprint, and create transition plan.")

    uploaded_file = st.file_uploader("Choose a feedback file", type=['txt', 'csv', 'json'])

    if uploaded_file is not None:
        with st.spinner("Processing feedback running..."):
            try:
                # Send file to FastAPI endpoint
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post("http://localhost:8005/process-feedback", files=files)
                
                if response.status_code == 200:
                    results = response.json()
                    
                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["Prioritized Features", "MVP Blueprint", "Transition Plan"])
                    
                    with tab1:
                        st.subheader("Prioritized Features")
                        st.json(results["features"])
                    
                    with tab2:
                        st.subheader("MVP Blueprint")
                        st.json(results["blueprint"])
                    
                    with tab3:
                        st.subheader("Transition Plan")
                        st.json(results["transition_plan"])
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to process file: {str(e)}")

# Run FastAPI server in a separate thread
def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8005)

if __name__ == "__main__":
    # Start FastAPI server in a thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Give FastAPI some time to start
    time.sleep(2)
    
    # Run Streamlit
    run_streamlit()