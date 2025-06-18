import streamlit as st

def get_user_commitment():
    st.subheader("Your Availability")
    commitment = st.radio("How much time can you dedicate to your startup?", 
                          ["Full-time", "Part-time", "Weekend Only"])
    return commitment

def get_project_title():
    st.subheader("Startup Project")
    title = st.text_input("Enter your startup project title or description:")
    return title
