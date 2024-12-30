import streamlit as st
import random
import time
import requests
import os
from utilities import calculate_embeddings

QUERY_MANAGER_API = os.getenv("QUERY_MANAGER_API")
DATA_PATH = os.getenv("DATA_PATH")


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


if uploaded_files:
    st.write(f"Uploading {len(uploaded_files)} file(s) to the 'data' folder:")

if st.button("Submit"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(DATA_PATH, uploaded_file.name)
            with open(file_path, "wb") as f:
                bytes_data = uploaded_file.read()
                f.write(bytes_data)
        st.write("Please wait...")
        calculate_embeddings()
        st.success("You are good to go!")

    else:
        st.warning("No files to process. Please upload files first.")

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
