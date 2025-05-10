import streamlit as st
import requests

st.set_page_config(page_title="Dolphin AI Local Demo", layout="centered")
st.markdown("""
    <h1 style='text-align: center; font-size: 2.8em;'>🐬 Dolphin AI Local Demo</h1>
""", unsafe_allow_html=True)
st.write("Enter a prompt and get a response from your locally running Dolphin-phi model via Ollama. Make sure Ollama is running and the model is loaded.")

user_prompt = st.text_area("Enter your prompt", placeholder="e.g. Tell me a joke about AI.")

if st.button("Submit"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Contacting Ollama API..."):
            try:
                # Ollama's default API endpoint for chat/completion
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "dolphin-phi",
                        "prompt": user_prompt,
                        "stream": False
                    },
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
                output = result.get("response", "[No response returned]").strip()
                st.success("Response:")
                st.markdown(f"> {output}")
            except Exception as e:
                st.error(f"Error: {e}")
