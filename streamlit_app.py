import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import json

st.set_page_config(page_title="EduGenie", page_icon="📚")
st.title("📚 EduGenie - AI Study Assistant")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = st.text_input("Enter Google API Key", type="password")
    if not api_key:
        st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

uploaded = st.file_uploader("Upload PDF", type="pdf")

if uploaded:
    reader = PdfReader(uploaded)
    text = ""
    for p in reader.pages:
        text += p.extract_text() or ""
    st.success(f"PDF loaded! {len(reader.pages)} pages")
    if st.button("Generate Quiz"):
        with st.spinner("Generating..."):
            prompt = f"Create 5 MCQ questions from this text in JSON format: [{{'question':'...', 'options':['A','B','C','D'], 'answer':'A'}}] Text: {text[:8000]}"
            response = model.generate_content(prompt)
            clean = response.text.replace('```json','').replace('```','').strip()
            try:
                quiz = json.loads(clean)
                for i, q in enumerate(quiz, 1):
                    st.write(f"**{i}. {q['question']}**")
                    st.write(q['options'])
                    with st.expander("Answer"):
                        st.write(q['answer'])
            except:
                st.write(response.text)
