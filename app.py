import streamlit as st
import google.generativeai as genai

# Page ki setting
st.set_page_config(page_title="Jabi AI Assistant", page_icon="🤖")
st.title("🤖 Jabi's AI Assistant")

# API Setup
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# Chat History (Mobile app ki tarah purani baten yaad rakhne ke liye)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Kuch bhi poochiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI ka jawab
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
