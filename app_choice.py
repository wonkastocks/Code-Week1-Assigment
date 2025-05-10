import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (for default OpenAI key, if any)
load_dotenv(override=True)

# ---- Sidebar navigation ----
pages = ["OpenAI Assistant", "Local Ollama Assistant", "About"]
page = st.sidebar.radio("Go to", pages)

# ---- Common UI Elements ----
def output_format_selector():
    return st.radio("Response format:", ["Full text", "Bullet points", "Numbered list"], horizontal=True)

def temperature_slider():
    return st.slider("Temperature", 0.0, 1.0, 0.7, 0.01)

# ---- Page 1: OpenAI Assistant ----
if page == "OpenAI Assistant":
    st.title("OpenAI Assistant")
    st.write("Enter your question, and the OpenAI API will provide an answer.")

    # --- Configuration ---
    with st.sidebar:
        st.subheader("Configuration")
        openai_api_key = st.text_input("Enter your OpenAI API key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        openai_model = st.selectbox("Select OpenAI model", ["gpt-3.5-turbo", "gpt-4"])  # Add more as needed
        temp = temperature_slider()

    user_prompt = st.text_area("Enter your question:")
    fmt = output_format_selector()

    if st.button("Generate Response"):
        if not openai_api_key:
            st.error("Please enter your OpenAI API key.")
        elif not user_prompt.strip():
            st.warning("Please enter a question.")
        else:
            import openai
            openai.api_key = openai_api_key
            with st.spinner("Contacting OpenAI API..."):
                try:
                    # Format prompt for output type
                    prompt = user_prompt
                    if fmt == "Bullet points":
                        prompt += "\n\nRespond in bullet points."
                    elif fmt == "Numbered list":
                        prompt += "\n\nRespond as a numbered list."
                    response = openai.chat.completions.create(
                        model=openai_model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=512,
                        temperature=temp,
                    )
                    output = response.choices[0].message.content.strip()
                    st.success("Response:")
                    st.markdown(output)
                except Exception as e:
                    st.error(f"Error: {e}")

# ---- Page 2: Local Ollama Assistant ----
elif page == "Local Ollama Assistant":
    st.title("Local Ollama Assistant")
    st.write("Interact with your locally running Ollama models.")

    # --- Configuration ---
    with st.sidebar:
        st.subheader("Configuration")
        # You can extend this list as you add more models
        ollama_model = st.selectbox("Select Ollama model", ["dolphin-phi", "llama3", "phi3", "mistral"])
        temp = temperature_slider()

    user_prompt = st.text_area("Enter your question:")
    fmt = output_format_selector()

    if st.button("Generate Response"):
        if not user_prompt.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Contacting Ollama API..."):
                try:
                    # Format prompt for output type
                    prompt = user_prompt
                    if fmt == "Bullet points":
                        prompt += "\n\nRespond in bullet points."
                    elif fmt == "Numbered list":
                        prompt += "\n\nRespond as a numbered list."
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": ollama_model,
                            "prompt": prompt,
                            "stream": False,
                            "options": {"temperature": temp}
                        },
                        timeout=60
                    )
                    response.raise_for_status()
                    result = response.json()
                    output = result.get("response", "[No response returned]").strip()
                    st.success("Response:")
                    st.markdown(output)
                except Exception as e:
                    st.error(f"Error: {e}")

# ---- Page 3: About ----
else:
    st.title("About This App")
    st.write("""
    This app lets you choose between using the OpenAI API (with your own key) or a local Ollama model for AI-powered responses.
    
    - **OpenAI Assistant:** Enter your API key, pick a model, set temperature, and choose the output format.
    - **Local Ollama Assistant:** Pick a local model, set temperature, and choose the output format.
    - **Output Formats:** Full text, bullet points, or numbered lists.
    
    **Security:** Your OpenAI API key is never stored.
    """)
    st.info("Built with Streamlit. For best results, ensure Ollama is running and your models are loaded.")
