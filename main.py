import openai
import time
import streamlit as st
import os

def main():

    if 'client' not in st.session_state:
        # Initialize the client
        st.session_state.client = openai.OpenAI()

        # Step 1: Loading an Assistant
        st.session_state.assistant = st.session_state.client.beta.assistants.retrieve("asst_n32JDYZZSmvAStLau06hMoJ4")

        # Step 2: Create a Thread
        st.session_state.thread = st.session_state.client.beta.threads.create()

    user_query = st.text_input("Enter your query:", "Tell me about Dance Monkey")

    if st.button('Submit'):
        # Step 3: Add a Message to a Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_query
        )

        # Step 4: Run the Assistant
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
            instructions="Please address the user as Mervin Praison"
        )

        while True:
            # Wait for 5 seconds
            time.sleep(5)

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

                # Loop through messages and print content based on role
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    st.write(f"{role.capitalize()}: {content}")
                break
            else:
                st.write("Waiting for the Assistant to process...")
                time.sleep(5)

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "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"
    main()