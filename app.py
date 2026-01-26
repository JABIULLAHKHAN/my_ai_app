import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Jabi's AI Assistant", page_icon="🤖")

# 2. CSS for Styling (Ab isme error nahi aayega)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True) # Yahan galti thi, ab sahi kar di hai

st.title("🤖 Jabi's AI Assistant")
st.write("Assalam-o-Alaikum! Main aapka personal AI assistant hun.")

# 3. API Key Setup
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Pehle Streamlit Settings > Secrets mein apni API Key dalein.")

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kuch bhi poochiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
