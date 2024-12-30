import streamlit as st
import random
import time
import requests
import os
from utilities import calculate_embeddings

QUERY_MANAGER_API = os.getenv("QUERY_MANAGER_API")


def get_response(query: str):
    try:
        payload = {"query": query}
        response = requests.post(
            f"{QUERY_MANAGER_API}/answer",
            json=payload,
        )
        response.raise_for_status()
        answer = response.json()["response"]
        return answer
    except Exception as e:
        raise e


def get_response_stream(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Streamed response emulator: for testing purposes
# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)


st.title("🤖 RAG system")

if "hide_fileUploader" not in st.session_state:
    st.session_state.hide_fileUploader = False

hide_fileUploader = st.session_state.get("hide_fileUploader")
with st.container():
    if hide_fileUploader:
        st.empty()
    else:
        uploaded_files = st.file_uploader("Select files...", accept_multiple_files=True)
        if uploaded_files:
            st.write(f"Uploading {len(uploaded_files)} file(s) to the 'data' folder:")

        if st.button("Submit"):
            st.session_state.display_chat = False
            st.session_state.messages = []
            if uploaded_files:
                with st.spinner(text="In progress..."):
                    calculate_embeddings(uploaded_files)
                st.success("You are good to go!", icon="✅")
                time.sleep(5)
                st.session_state.display_chat = True
                st.session_state.hide_fileUploader = True
                st.rerun()
            else:
                st.warning("No files to process. Please upload files first.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


display_chat = st.session_state.get("display_chat")
if display_chat:
    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Analyzing... Please wait..."):
                response = get_response(query=prompt)
            st.write_stream(get_response_stream(response))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
