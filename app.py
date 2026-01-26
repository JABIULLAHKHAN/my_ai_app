import streamlit as st
import google.generativeai as genai

# --- 1. APP CONFIGURATION (Icon aur Browser Tab Name) ---
# Yahan maine ek AI icon ka link dala hai, aap ise apni photo ke link se badal sakte hain
st.set_page_config(
    page_title="Jabi AI",
    page_icon="https://cdn-icons-png.flaticon.com/512/4712/4712139.png", 
    layout="centered"
)

# --- 2. HIDING STREAMLIT BRANDING (Powerd by Streamlit hatane ke liye) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Mobile icon fix aur extra branding removal */
            .viewerBadge_container__1QS13 {display: none;}
            [data-testid="stStatusWidget"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. GOOGLE AI SETUP (Using Secrets) ---
try:
    # Secrets se key uthayega (Jo aapne dashboard mein dali hai)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Aapka pasandeeda model
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("API Key missing! Please add it to Streamlit Secrets.")

# --- 4. SIDEBAR (Aapka Naam aur Profile) ---
with st.sidebar:
    st.title("👨‍💻 Developer")
    st.header("Jabi Khan")
    st.write("Personal AI Assistant")
    st.divider()
    st.info("Ye app Jabi Khan ne banaya hai. Isme Gemini AI ki power use ki gayi hai.")

# --- 5. CHAT INTERFACE ---
st.title("🤖 Jabi AI")
st.caption("Custom AI Assistant - Online")

# Chat history ko store karne ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages display karna
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input aur AI Response
if prompt := st.chat_input("Kuch bhi poochiye..."):
    # User ka message save aur show karna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI ka response generate karna
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            # AI ka message save karna
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Opps! Kuch galti ho gayi: {e}")
