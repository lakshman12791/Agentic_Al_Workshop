import streamlit as st
from feasibility_score import assess_feasibility
from viability_agent import score_viability
from prioritization_agent import prioritize_features
from blueprint_generator import generate_blueprint
from transition_planner import create_transition_plan
from feedback_parser import parse_feedback
from utils.file_parser import parse_uploaded_file
import google.generativeai as genai
import os
import tempfile

# Initialize Gemini
genai.configure()

def process_feedback(file_path: str):
    # Step 1: Parse uploaded file
    feedback_data = parse_uploaded_file(file_path)
    if feedback_data is None:
        raise ValueError("parse_uploaded_file returned None")
    if not isinstance(feedback_data, (list, dict)):
        raise ValueError(f"parse_uploaded_file returned non-iterable type: {type(feedback_data)}")

    # Step 2: Parse feedback
    parsed_features = parse_feedback(feedback_data)
    print("parsed_features:", parsed_features)  

    if parsed_features is None:
        st.warning("parse_feedback returned None; returning empty list to continue processing.")
        parsed_features = []  # Fallback to empty list
    if not isinstance(parsed_features, (list, dict)):
        raise ValueError(f"parse_feedback returned non-iterable type: {type(parsed_features)}")

    # Step 3: Assess feasibility
    feasible_features = assess_feasibility(parsed_features)
    print("feasible_features:", feasible_features)  

    if feasible_features is None:
        raise ValueError("assess_feasibility returned None")
    if not isinstance(feasible_features, (list, dict)):
        raise ValueError(f"assess_feasibility returned non-iterable type: {type(feasible_features)}")

    # Step 4: Score viability
    viable_features = score_viability(feasible_features)
    print("viable_features:", viable_features)  

    if viable_features is None:
        st.warning("score_viability returned None; returning empty list to continue processing.")
        viable_features = []  # Fallback to empty list
    if not isinstance(viable_features, (list, dict)):
        raise ValueError(f"score_viability returned non-iterable type: {type(viable_features)}")

    # Step 5: Prioritize features
    prioritized_features = prioritize_features(viable_features)
    print("prioritized_features:", prioritized_features)  

    if prioritized_features is None:
        raise ValueError("prioritize_features returned None")
    if not isinstance(prioritized_features, (list, dict)):
        raise ValueError(f"prioritize_features returned non-iterable type: {type(prioritized_features)}")

    # Step 6: Generate blueprint
    mvp_blueprint = generate_blueprint(prioritized_features)
    if mvp_blueprint is None:
        raise ValueError("generate_blueprint returned None")

    # Step 7: Create transition plan
    transition_plan = create_transition_plan(mvp_blueprint)
    if transition_plan is None:
        raise ValueError("create_transition_plan returned None")
    
    

    return {
        "features": [f.dictt() for f in prioritized_features],
        "blueprint": mvp_blueprint.dict(),
        "transition_plan": transition_plan.dict()
    }

# Streamlit interface
def main():
    st.set_page_config(page_title="Feedback Processor", layout="wide")
    st.title("Feedback Processing Application")
    st.write("Upload a feedback file to process features, generate blueprint, and create transition plan.")

    uploaded_file = st.file_uploader("Choose a feedback file", type=['txt', 'csv', 'json'])

    if uploaded_file is not None:
        with st.spinner("Processing feedback..."):
            try:
                # Create a temporary file to store the uploaded content
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                # Run the process_feedback function
                results = process_feedback(tmp_file_path)
                
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
            except Exception as e:
                st.error(f"Failed to process file: {str(e)}")
            finally:
                # Clean up the temporary file
                if 'tmp_file_path' in locals():
                    os.unlink(tmp_file_path)

if __name__ == "__main__":
    main()