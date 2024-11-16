import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='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')

# System prompt for the chatbot
system_prompt = """
You are to now assume the identity of CloudCompass, a cloud migration consultant. Your goal is to help companies migrate to the cloud.
Take the lead in conversations by asking relevant questions to gather necessary information
before providing assistance. Be professional, concise, and helpful.
"""

# Initialize Streamlit app
st.set_page_config(page_title="Cloud Migration Consultant", layout="centered")
st.title("CloudCompass: Your Cloud Migration Consultant")

# Session state for storing the conversation
if "conversation" not in st.session_state:
    st.session_state["conversation"] = [{"role": "system", "content": system_prompt}]
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat interface
st.chat_message("assistant").write("Hello! I'm CloudCompass, how can i help you today?")

# User input box
user_input = st.text_input("Type your message:", key="user_input", placeholder="Ask me anything about cloud migration...")

if user_input:
    # Append user input to the conversation
    st.session_state["conversation"].append({"role": "user", "content": user_input})
    
    # Generate response from OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state["conversation"],
            max_tokens=300,
            temperature=0.7
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = "I'm sorry, I couldn't process your request at the moment. Please try again later."
    
    # Append response to the conversation
    st.session_state["conversation"].append({"role": "assistant", "content": assistant_reply})
    
    # Update chat history
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    st.session_state["chat_history"].append({"role": "assistant", "content": assistant_reply})

# Display chat history
for message in st.session_state["chat_history"]:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").write(message["content"])