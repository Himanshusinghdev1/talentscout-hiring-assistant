# app.py

import streamlit as st
from prompts import get_greeting_prompt_multilingual, get_question_prompt
from utils import ask_gemini, analyze_sentiment
from data_handler import save_candidate

# --- Streamlit Page Setup ---
st.set_page_config(page_title="TalentScout AI Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

# --- Session Initialization ---
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.info = {}
    st.session_state.questions = [
        "Full Name",
        "Email Address",
        "Phone Number",
        "Years of Experience",
        "Desired Position(s)",
        "Current Location",
        "Tech Stack"
    ]
    st.session_state.current_question = 0
    st.session_state.language_selected = False
    st.session_state.language = ""
    st.session_state.conversation = []
    st.session_state.chatbot_initialized = False

exit_keywords = ["exit", "quit", "bye", "stop"]

# --- Language Selection ---
if not st.session_state.language_selected:
    lang_input = st.text_input("🌐 Please enter your preferred language (e.g., English, Hindi, Spanish):")
    if lang_input:
        st.session_state.language = lang_input
        st.session_state.language_selected = True
        st.rerun()
else:
    # --- Initial Greeting (once) ---
    if not st.session_state.chatbot_initialized:
        greeting = ask_gemini(get_greeting_prompt_multilingual(st.session_state.language))
        st.session_state.conversation.append(("Assistant", greeting))
        st.session_state.chatbot_initialized = True

    # --- Chat Display ---
    st.markdown("### 💬 Conversation")
    for role, msg in st.session_state.conversation:
        st.markdown(f"**{role}:** {msg}")

    # --- User Input Field ---
    user_input = st.text_input("You:", key="user_input")

    if user_input:
        # Sentiment analysis
        mood = analyze_sentiment(user_input)
        st.session_state.conversation.append(("Candidate", user_input))
        st.session_state.conversation.append(("Assistant", f"(Mood detected: {mood})"))

        # Exit check
        if user_input.strip().lower() in exit_keywords:
            st.session_state.conversation.append(("Assistant", "Thank you for chatting with TalentScout! We'll be in touch soon. 👋"))
            st.session_state.step = -1
            st.stop()

        # Save answer and move to next question
        if st.session_state.current_question < len(st.session_state.questions):
            field = st.session_state.questions[st.session_state.current_question]
            st.session_state.info[field] = user_input
            st.session_state.current_question += 1

            if st.session_state.current_question < len(st.session_state.questions):
                next_q = st.session_state.questions[st.session_state.current_question]
                st.session_state.conversation.append(("Assistant", f"{next_q}?"))
            else:
                # All info collected → Save data and generate tech questions
                save_candidate(st.session_state.info)
                tech_stack = st.session_state.info.get("Tech Stack", "")
                tech_prompt = get_question_prompt(tech_stack)
                tech_questions = ask_gemini(tech_prompt)

                st.session_state.conversation.append(("Assistant", "Thank you for sharing your details! Based on your tech stack, here are some questions:"))
                st.session_state.conversation.append(("Assistant", tech_questions))

        st.rerun()
