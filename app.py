import streamlit as st
import google.generativeai as genai

# 1. Page Configuration (App ka title aur icon)
st.set_page_config(page_title="Jabi's AI Assistant", page_icon="🤖")

# 2. CSS for Styling (App ko sundar banane ke liye)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_index=True)

st.title("🤖 Jabi's AI Assistant")
st.write("Assalam-o-Alaikum! Main aapka personal AI assistant hun. Poochiye kya poochna hai?")

# 3. API Key Setup (Secrets se key uthayega)
try:
    # Yahan humne secrets use kiya hai taaki key leak na ho
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key setup mein galti hai. Please Secrets check karein.")

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Naya sawaal poochna
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
