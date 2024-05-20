import os  # To interact with the operating system and environment variables.
import streamlit as st  # To create and run interactive web applications directly through Python scripts.
from pathlib import Path  # To provide object-oriented filesystem paths, enhancing compatibility across different operating systems.
from dotenv import load_dotenv  # To load environment variables from a .env file into the system's environment for secure and easy access.
from groq import Groq  # To interact with Groq's API for executing machine learning models and handling data operations.

# Load environment variables from .env at the project root
project_root = Path(__file__).resolve().parent
load_dotenv(project_root / ".env")

# Dictionary of available LLM models
llm_models = {
    "LLaMA3 8b": "llama3-8b-8192",
    "LLaMA3 70b": "llama3-70b-8192",
    "MixtraL 8x7b": "mixtral-8x7b-32768",
    "GEMMA 7b": "gemma-7b-it"
}
# System prompt for the LLM model
systems = {
    "PHP": "You are a PHP 8 expert. Please generate responses in PHP to all user inputs and add CSS code if needed.",
    "Laravel": "You are a Laravel version 11 professional. Please generate responses in Laravel to all user inputs.",
    "Python": "You are a Python and CSS professional. Please generate responses in Python and CSS code to all user inputs and explain the code.",
    "JavaScript": "You are a JavaScript professional. Please generate responses in JavaScript code to all user inputs and explain the code.",
    "CSS and SASS": "You are a CSS, SASS professional. Please generate responses in CSS and SASS to all user inputs.",
}

languages = {
    "English": "English",
    "Dutch": "Dutch",
    "French": "French",
    "German": "German",
}

class GroqAPI:
    """Handles API operations with Groq to generate chat responses."""
    def __init__(self, model_name: str, system_prompt: str, language: str):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.language = language

# Internal method to fetch responses from the Groq API
    def _response(self, message):
        # st.write(self.model_name)
        # st.write(self.system_prompt)
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            stream=True,
            stop=None,
        )

    # Generator to stream responses from the API
    def response_stream(self, message):
        for chunk in self._response(message):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class Message:
    """Manages chat messages within the Streamlit UI."""
    system_prompt = "You are a professional AI. Please generate responses in English to all user inputs."

# Initialize chat history if it doesn't exist in session state
    def __init__(self, system_prompt: str, language: str):
        self.system_prompt = f"{system_prompt}. Always respond in {language}."
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": self.system_prompt}]

# Add a new message to the session state
    def add(self, role: str, content: str):
        # st.write('IM IN ADD*******')
        st.write(f'system prompt ${self.system_prompt}')
        st.session_state.messages[0] = {"role": "system", "content": self.system_prompt}
        st.session_state.messages.append({"role": role, "content": content})
        # st.write(st.session_state.messages)
        # st.write(st.session_state.messages)

# Display all past messages in the UI, skipping system messages
    def display_chat_history(self):
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Stream API responses to the Streamlit chat message UI
    def display_stream(self, generater):
        with st.chat_message("assistant"):
            return st.write_stream(generater)

# Entry point for the Streamlit app
def main():
    user_input = st.chat_input("Enter message to AI models...")

    # Display model selection in a sidebar with a title
    with st.sidebar:
        st.sidebar.title("Chat With Groq")
        selected_model_name = st.selectbox("Select a model:", list(llm_models.keys()))
        selected_model = llm_models[selected_model_name]
        selected_system_name = st.selectbox("Select a system prompt:", list(systems.keys()))
        selected_system = systems[selected_system_name]
        selected_language_name = st.selectbox("Select a language:", list(languages.keys()))
        selected_language = languages[selected_language_name]
        message = Message(selected_system, selected_language)

    # If there's user input, process it through the selected model
    if user_input:
        # st.write('new input')
        llm = GroqAPI(selected_model, selected_system, selected_language)
        message.add("user", user_input)
        message.display_chat_history()
        response = message.display_stream(llm.response_stream(st.session_state.messages))
        message.add("assistant", response)


if __name__ == "__main__":
    main()
