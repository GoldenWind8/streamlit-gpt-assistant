import openai
import time
import streamlit as st
import os

def main():
    st.title("Biology Assistant 🦠🧬")

    if 'client' not in st.session_state:
        # Initialize the client
        st.session_state.client = openai.OpenAI()
        st.session_state.assistant = st.session_state.client.beta.assistants.retrieve("asst_n32JDYZZSmvAStLau06hMoJ4")

        # Step 2: Create a Thread
        st.session_state.thread = st.session_state.client.beta.threads.create()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What are the two types of cells?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_response(st, prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)


def get_response(st, prompt):
    # Step 3: Add a Message to a Thread
    message = st.session_state.client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )

    # Step 4: Run the Assistant
    run = st.session_state.client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id
    )

    while True:
        time.sleep(2)
        # Retrieve the run status
        run_status = st.session_state.client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = st.session_state.client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
            )

            lastMsg = messages.data[0].content[0].text.value
            print(lastMsg)
            return lastMsg


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    main()