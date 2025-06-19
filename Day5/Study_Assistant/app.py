
# import streamlit as st
# import PyPDF2
# import openai
# import os

# st.title("Study Material Quiz Generator")

# uploaded_file = st.file_uploader("Upload Course PDF", type=["pdf"])
# openai_api_key = st.text_input("Enter OpenAI API Key", type="password")

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# def generate_summary_and_questions(text):
#     prompt = f"""Summarize the following content into concise points and create 5 multiple choice questions (each with 4 options and the correct answer) based on the summary:\n{text}"""

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{{
#             "role": "user",
#             "content": prompt
#         }}],
#         temperature=0.7
#     )
#     return response['choices'][0]['message']['content']

# if uploaded_file and openai_api_key:
#     with st.spinner("Extracting and analyzing content..."):
#         content = extract_text_from_pdf(uploaded_file)
#         openai.api_key = openai_api_key
#         output = generate_summary_and_questions(content)
#         st.subheader("Generated Summary and Quiz:")
#         st.text_area("Result", value=output, height=400)


import streamlit as st
import PyPDF2
import google.generativeai as genai

st.title("Study Material Quiz Generator (Gemini AI)")

uploaded_file = st.file_uploader("Upload Course PDF", type=["pdf"])
gemini_api_key = st.text_input("Enter Gemini API Key", type="password")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def generate_summary_and_questions_with_gemini(text):
    prompt = f"""
    Summarize the following content into concise points and create 5 multiple-choice questions.
    Each question must include 4 options with one correct answer clearly marked.\n\n{text}
    """

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

if uploaded_file and gemini_api_key:
    with st.spinner("Extracting and analyzing content using Gemini..."):
        content = extract_text_from_pdf(uploaded_file)
        try:
            output = generate_summary_and_questions_with_gemini(content)
            st.subheader("Generated Summary and Quiz:")
            st.text_area("Result", value=output, height=400)
        except Exception as e:
            st.error(f"Error generating content: {e}")
