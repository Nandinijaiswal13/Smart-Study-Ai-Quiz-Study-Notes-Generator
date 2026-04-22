import streamlit as st
from utils import extract_text_from_pdf, preprocess_text, content_analysis, generate_notes, generate_quiz
from auth import register_user, login_user

st.set_page_config(page_title="Smart Study AI")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "quiz" not in st.session_state:
    st.session_state.quiz = []


# 🔐 LOGIN
def auth_page():
    st.title("🔐 Login")

    choice = st.selectbox("Login / Signup", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Register"):
            success, msg = register_user(username, password)
            st.success(msg) if success else st.error(msg)

    if choice == "Login":
        if st.button("Login"):
            success, msg = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.success("Welcome!")
            else:
                st.error(msg)


# 📚 MAIN
def main_app():
    st.title("📚 Smart-Study Ai Notes & Quiz Generator")

    if st.button("Logout"):
        st.session_state.logged_in = False

    # 🔽 INPUT MODE SELECTION
    mode = st.radio("Choose Input", ["Text", "File"])

    text = ""
    file = None

    # 📝 TEXT INPUT
    if mode == "Text":
        text = st.text_area(
            "Enter your study content",
            height=250,
            placeholder="Paste your notes here..."
        )

    # 📄 FILE INPUT
    elif mode == "File":
        file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if file is not None:
        with st.spinner("Reading file..."):
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")

        st.success("File loaded successfully ")


    # 🚀 PROCESS ONLY IF TEXT EXISTS
    if text:

        text, sentences = preprocess_text(text)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Keyword"):
            st.write(content_analysis(text))

    with col2:
        if st.button("Generate Notes"):
            st.write(generate_notes(text))

    with col3:
        if st.button("Generate Quiz"):
            st.session_state.quiz = generate_quiz(sentences)

    # 📝 DISPLAY QUIZ
    if st.session_state.quiz:
        st.subheader("Quiz")
        for i, q in enumerate(st.session_state.quiz, 1):
            st.write(f"{i}. {q['question']}")

    else:
        st.info("Please enter text or upload a file")



if st.session_state.logged_in:
    main_app()
else:
    auth_page()