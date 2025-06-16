import streamlit as st
import requests

st.title("Startup Time Investment Simulator")

idea = st.text_input("Describe your startup idea")
hours = st.slider("Weekly Time Commitment (hrs)", 1, 60, 10)
exp = st.selectbox("Experience Level", ["Novice", "Intermediate", "Expert"])

if st.button("Simulate"):
    res = requests.post("http://localhost:8000/simulate", json={
        "idea": idea,
        "hours_per_week": hours,
        "experience": exp
    }).json()
    st.success(res['message'])

if st.button("Get Inspiration"):
    res = requests.post("http://localhost:8000/inspiration", json={
        "query": f"{idea}, solo founder, {hours} hrs/week"
    }).json()
    st.markdown("### Similar Stories")
    st.write(res["result"])