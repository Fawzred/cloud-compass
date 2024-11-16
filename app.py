import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["api_key"])

# System prompt for the chatbot
system_prompt = """
You are to now assume the identity of CloudCompass, a cloud migration consultant. Your goal is to help companies migrate to the cloud.
Take the lead in conversations by asking relevant questions to gather necessary information
before providing assistance. Be professional, concise, and helpful.
"""

# Initialize Streamlit app
st.set_page_config(page_title="Cloud Migration Consultant", layout="centered")
st.image("logo.png", width=150)
st.title("CloudCompass: Your Cloud Migration Consultant")

# Session state for storing the conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Hello! I'm CloudCompass, and I'm here to help you migrate to the cloud. Let's get started! What can I help you with?"}
    ]

# Display previous messages (excluding the system prompt)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input using st.chat_input
if prompt := st.chat_input("Ask me anything about cloud migration..."):
    # Append user input to the conversation
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the desired model
            messages=st.session_state.messages,
            max_tokens=300,
            temperature=0.7
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = str(e)

    # Append assistant's reply to the conversation
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
