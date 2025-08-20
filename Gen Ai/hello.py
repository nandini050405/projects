import streamlit as st

import requests
import json

# Streamlit UI
st.set_page_config(page_title="Ollama with Streamlit", page_icon="🤖", layout="centered")

st.title("💬 Chat with Ollama (LLaMA2)")
st.write("Type a question and get a response from Ollama running locally.")

# Input box
prompt = st.text_area("Enter your prompt:")

if st.button("Generate Response"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "gemma3",
        "prompt": prompt
    }

    # Placeholder for streaming response
    response_placeholder = st.empty()
    full_response = ""

    with requests.post(url, json=data, stream=True) as r:
        for line in r.iter_lines():
            if line:
                body = json.loads(line)
                if "response" in body:
                    token = body["response"]
                    full_response += token
                    response_placeholder.markdown(full_response)

    st.success("✅ Response Generated!")