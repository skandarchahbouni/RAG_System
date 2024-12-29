import streamlit as st
import random
import time
import requests
import os

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
        for word in answer.split():
            yield word + " "
            time.sleep(0.05)
    except Exception as e:
        raise e


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("🤖 RAG system")

uploaded_files = st.file_uploader("Select files...", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(get_response(query=prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
