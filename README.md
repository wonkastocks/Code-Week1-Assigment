# AI Assistant Streamlit App

This project is a modern, visually appealing Streamlit web application that allows users to interact with large language models (LLMs) from both OpenAI (GPT-3.5, GPT-4) and locally hosted Ollama models. The app features a user-friendly interface for generating AI-powered responses in various formats.

## Features & UI Elements

- **Sidebar:**
  - **Model Selector**: Choose from available OpenAI or Ollama models (only those installed locally are shown).
  - **API Key Field**: Securely enter your OpenAI API key (only required for OpenAI models).
  - **Temperature Slider**: Adjust the creativity of the model's responses.

- **Main Area:**
  - **Header**: App title, model icon, and currently selected model.
  - **Input Box**: Enter your question or prompt for the AI.
  - **Response Format Selector**: Choose between Full Text, Bullet Points, or Numbered List output.
  - **Generate Response Button**: Triggers the AI to generate and display a response.
  - **Output Box**: Displays the AI's answer in the selected format.
  - **About Section**: Expandable section with app details and usage notes.

## Supported LLM Models

- **OpenAI:**
  - `gpt-3.5-turbo`
  - `gpt-4`
  - (Requires your own OpenAI API key, never stored or uploaded)

- **Ollama (local):**
  - Only the following models are shown if installed locally:
    - dolphin-phi:latest
    - gemma3:1b
    - smollm:135m
    - llama3.1:8b
    - llama2-uncensored:latest
    - phi3.5:latest
    - wizard-vicuna-uncensored:30b
    - dolphin-mistral:latest
    - llama2-uncensored:7b
    - llama3.2:3b
    - llava:latest

## How the Dropdown Works
- The model selector dynamically lists only OpenAI models and the above Ollama models that are actually available on your system.
- This prevents errors from selecting a model that is not installed.

## How to Run
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start Ollama (if using local models):**
   ```bash
   ollama serve
   # and pull any desired models, e.g.:
   ollama pull dolphin-phi:latest
   ```
3. **Run the app:**
   ```bash
   streamlit run app_unified.py
   ```
4. **Open in your browser** as directed by Streamlit.

## App Structure & Logic
- All main logic is in `app_unified.py`.
- The sidebar is used for model selection, API key entry, and temperature control.
- The main area handles input, output, and formatting options.
- The app detects which models are available and adapts the UI accordingly.
- OpenAI requests use your API key securely from the environment or sidebar input.
- Ollama requests are sent to your local server and only for models you have installed.
- Prompt instructions are dynamically modified based on the selected output format.

## Security Notes
- **No API keys or sensitive data are ever stored or uploaded.**
- `.env`, OpenAI key files, and personal notes are excluded from the repository.
- Only public, non-sensitive code and assets are included.

## Credits
- Built with [Streamlit](https://streamlit.io/), [OpenAI](https://openai.com/), and [Ollama](https://ollama.ai/).

---
If you have questions or want to contribute, please open an issue or pull request!
