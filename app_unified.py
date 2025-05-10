import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (for default OpenAI key, if any)
load_dotenv(override=True)

# ---- Sidebar: Configuration ----
st.sidebar.markdown("""
    <div style='text-align:center; font-weight:700; font-size:1.5em; color:#184c7d;'>Model</div>
""", unsafe_allow_html=True)

# Use external CSS for styling
with open("app_unified.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Model options
import subprocess

def get_ollama_models():
    """
    Returns a list of allowed Ollama models that are currently available on the local system.
    Filters the list to only include models specified in `allowed_models` and present in `ollama list`.
    """
    allowed_models = [
        "dolphin-phi:latest",
        "gemma3:1b",
        "smollm:135m",
        "llama3.1:8b",
        "llama2-uncensored:latest",
        "phi3.5:latest",
        "wizard-vicuna-uncensored:30b",
        "dolphin-mistral:latest",
        "llama2-uncensored:7b",
        "llama3.2:3b",
        "llava:latest"
    ]
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        available = set()
        for line in lines[1:]:
            name = line.split()[0]
            if name in allowed_models:
                available.add(name)
        return list(available)
    except Exception:
        return []

def get_model_options():
    """
    Returns a combined list of OpenAI and available Ollama models for the dropdown selector.
    """
    openai_models = ["gpt-3.5-turbo", "gpt-4"]
    ollama_models = get_ollama_models()
    return openai_models + ollama_models

model_options = get_model_options()
selected_model = st.sidebar.selectbox(
    "Model",  # Non-empty label for accessibility
    model_options,
    label_visibility="collapsed"  # Hide label visually
)

# Only show API key input for OpenAI models
def show_api_key_input():
    """
    Returns True if the selected model is an OpenAI GPT model (requires API key input).
    """
    return selected_model.startswith("gpt-")

openai_api_key = ""
if show_api_key_input():
    openai_api_key = st.sidebar.text_input(
        "Enter your OpenAI API key", type="password", value=os.getenv("OPENAI_API_KEY", "")
    )

# Temperature slider
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.01)

# ---- Main Area ----
# Determine logo and model display
logo = "🤖"
if selected_model == "dolphin-phi":
    logo = "🐬"
elif selected_model == "llama3":
    logo = "🦙"
elif selected_model == "phi3":
    logo = "🦉"
elif selected_model == "mistral":
    logo = "🐺"

# Unified blue theme, reduced space, all centered, modern look
st.markdown("""
    <style>
    body {
        background: #ede6fa;
    }
    .main-area {
        background: #cfe6ff;
        border-radius: 18px;
        box-shadow: 0 2px 16px rgba(80, 140, 255, 0.10);
        padding: 1.1em 1.2em 1.2em 1.2em;
        margin: 0em auto 0.7em auto;
        max-width: 540px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    header, .st-emotion-cache-18ni7ap {
        background: #f5f6fa !important;
    }
    .model-card {
        background: #eaf4ff;
        border-radius: 14px;
        padding: 0.7em 1.3em 0.7em 1.3em;
        margin-bottom: 0.6em;
        margin-top: 0.2em;
        box-shadow: 0 1px 8px rgba(80, 140, 255, 0.07);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .prompt-box textarea {
        background: #e7f2ff !important;
        border-radius: 10px !important;
        border: 1.3px solid #b6d6ff !important;
        font-size: 1.09em !important;
        color: #1e355b !important;
        margin-top: 0.2em !important;
        margin-bottom: 0.3em !important;
    }
    .stButton button {
        background: #e53935 !important;
        color: #fff !important;
        border-radius: 8px !important;
        padding: 0.6em 1.5em !important;
        font-weight: 600;
        font-size: 1.1em;
        border: 1.5px solid #b6d6ff !important;
        margin-top: 0.5em;
        margin-bottom: 1em;
        box-shadow: 0 2px 8px rgba(80, 140, 255, 0.07);
    }
    .stButton button:hover {
        background: #eaf4ff !important;
        color: #2a3c5a !important;
        border: 1.5px solid #6ec1e4 !important;
    }
    .stRadio > div {
        justify-content: center;
    }
    .response-label {
        font-weight: 600;
        color: #184c7d;
        font-size: 1.09em;
        margin-bottom: 0.3em;
        text-align: center;
    }
    .response-box {
        background: #eaf4ff;
        border-radius: 8px;
        padding: 0.8em 1em;
        color: #1e355b;
        margin-top: 0.5em;
        margin-bottom: 0.7em;
        font-size: 1.09em;
        text-align: center;
        box-shadow: 0 1px 8px rgba(80, 140, 255, 0.07);
    }
    .stAlert, .stAlert-success {
        border-radius: 8px !important;
        background: #eaf4ff !important;
        color: #1e355b !important;
        border: 1.5px solid #b6d6ff !important;
        text-align: center !important;
    }
        .stApp, .block-container {
            background: #ede6fa !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class='main-area'>
        <div style='display: flex; align-items: center; justify-content: center; gap: 1.1em; margin-bottom: 0.35em;'>
        <span style='font-size: 2.1em; font-weight: 700; color: #184c7d;'>AI Assistant</span>
        <span style='display: flex; align-items: center; font-size: 1.1em;'>
            <span style='font-size: 1.7em; margin-right: 0.3em;'>{logo}</span>
            <span style='font-weight: 600; color: #184c7d;'>{selected_model}</span>
        </span>
    </div>
    <div style='margin-bottom: 0.8em; text-align:center; color:#184c7d; font-size:1.08em;'>Enter your Question Below</div>
        <div class='prompt-box' style='width:100%;'>
""", unsafe_allow_html=True)

user_prompt = st.text_area(
    "Your question",  # non-empty label for accessibility
    value="",
    placeholder="Type your question here...",
    label_visibility="collapsed"  # hides the label visually
)

st.markdown("</div>", unsafe_allow_html=True)

# Centered response format and button
# Button and radio group on one centered line
import streamlit as st
from streamlit import columns

# Group Generate Response and radio buttons together in a single row
# Centered custom Generate Response button above a single radio group
import streamlit_js_eval

st.markdown("<div style='text-align:center; font-weight:600; color:#2a3c5a; margin-bottom:0.3em;'>Response format</div>", unsafe_allow_html=True)
output_format = st.radio(
    "Response format:",  # Non-empty label for accessibility
    ["Full text", "Bullet points", "Numbered list"],
    horizontal=True,
    key="response_format_radio",
    label_visibility="collapsed"
)

# Center the Generate Response button below the radio using Streamlit columns
col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    generate_clicked = st.button("Generate Response", key="generate_response_btn")

if generate_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a question.")
    elif show_api_key_input() and not openai_api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner("Generating response..."):
            prompt = user_prompt
            if output_format == "Bullet points":
                prompt += "\n\nRespond in bullet points."
            elif output_format == "Numbered list":
                prompt += "\n\nRespond as a numbered list."
            else:
                prompt += "\n\nRespond in a single paragraph of natural language, not as a list."
            try:
                if show_api_key_input():
                    import openai
                    openai.api_key = openai_api_key
                    try:
                        response = openai.chat.completions.create(
                            model=selected_model,
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=512,
                            temperature=temperature,
                        )
                        output = response.choices[0].message.content.strip()
                        st.success("Response:")
                        st.markdown(output)
                    except Exception as e:
                        err_msg = str(e)
                        if "Incorrect API key" in err_msg or "401" in err_msg:
                            st.error("Wrong API Key. Please check your key and try again, or choose a local model.")
                        else:
                            st.error(f"OpenAI Error: {err_msg}")
                else:
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": selected_model,
                            "prompt": prompt,
                            "stream": False,
                            "options": {"temperature": temperature}
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
    # Always clear the input after button press
    
# ---- About section at the bottom ----
with st.expander("About this app"):
    st.write("""
    This app lets you choose between OpenAI's API (with your key) or a local Ollama model for AI-powered responses. 
    - Select your model and temperature in the sidebar.
    - Choose your output format.
    - Your OpenAI API key is never stored.
    """)
