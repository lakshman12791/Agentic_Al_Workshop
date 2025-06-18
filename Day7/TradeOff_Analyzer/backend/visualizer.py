import streamlit as st
import matplotlib.pyplot as plt

def visualize_tradeoffs(commitment):
    if commitment == "Full-time":
        months = 3
    elif commitment == "Part-time":
        months = 12
    else:
        months = 16

    fig, ax = plt.subplots()
    ax.bar(["MVP Build Time"], [months], color="skyblue")
    ax.set_ylabel("Estimated Duration (Months)")
    ax.set_title(f"Estimated Timeline for {commitment} Commitment")
    st.pyplot(fig)
