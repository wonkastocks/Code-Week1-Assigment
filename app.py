import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="OpenAI API Demo", layout="centered")
st.title("🤖 OpenAI API Streamlit Demo")
st.write("Enter a prompt and get a response from OpenAI's GPT model.")

user_prompt = st.text_area("Enter your prompt", placeholder="e.g. Tell me a joke about AI.")

if st.button("Submit"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Contacting OpenAI API..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_prompt}],
                    max_tokens=256,
                    temperature=0.7,
                )
                output = response.choices[0].message.content.strip()
                st.success("Response:")
                st.markdown(f"> {output}")
            except Exception as e:
                st.error(f"Error: {e}")
