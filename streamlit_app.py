import streamlit as st
import os
import openai
from PIL import Image

# Set page title and layout
st.set_page_config(page_title="Chat with your Financial Report")

# Load and display the image at the top of the page
image_path = r"cm3.PNG"
if os.path.exists(image_path):
    image = Image.open(image_path)
    max_width, max_height = 800, 600
    image.thumbnail((max_width, max_height))
    st.image(image, use_column_width=True)
else:
    st.warning("Image not found. Please check the file path.")

st.write("""
### Chat with Charlie Munger Jr.

The GPT-4O foundation model was fine-tuned on 100 'mungerisms', allowing the user to chat with the late Charlie Munger.
""")

# Get OpenAI API key from user input
def get_openai_api_key():
    openai_api = st.text_input('Enter OpenAI API Key:', type='password')
    if not openai_api.startswith('sk-') or len(openai_api) != 51:
        st.warning('Please enter a valid OpenAI API Key!', icon="⚠️")
        return None
    else:
        st.success('Proceed to entering your prompt message!', icon="✨")
        return openai_api

# Fetch and set the OpenAI API key
openai_api = get_openai_api_key()
if openai_api:
    os.environ['OPENAI_API_KEY'] = openai_api
    openai.api_key = openai_api

# Model selection and parameters
with st.sidebar:
    st.subheader("Model and Parameters")
    model_options = {
        'Charlie Munger Jr. Model': 'ft:gpt-4o-2024-08-06:personal::A1OKDWJz',
        'GPT-4 Model': 'gpt-4',
        'GPT-3.5 Turbo Model': 'gpt-3.5-turbo'
    }
    selected_model_name = st.selectbox('Choose an OpenAI model:', list(model_options.keys()))
    selected_model = model_options[selected_model_name]

    temperature = st.slider('Temperature', 0.0, 1.5, 0.7, step=0.01)
    top_p = st.slider('Top_p', 0.01, 1.0, 0.95, step=0.01)
    max_tokens = st.slider('Max Tokens', 1, 500, 200, step=1)

    st.markdown(f'Selected model: {selected_model}')
    st.markdown(f'Temperature: {temperature}, Top_p: {top_p}, Max Tokens: {max_tokens}')

# Initialize chat
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": "Charlie Munger Jr. is a factual chatbot."})

# Display chat history
for message in st.session_state.messages:
    if message["role"] in {"user", "assistant"}:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Clear chat history button
def clear_chat_history():
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": "Charlie Munger Jr. is a factual chatbot."})

st.sidebar.subheader('Manage Chat History')
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Input from user
if openai_api:
    if prompt := st.chat_input("Ask Charlie Munger Jr. anything"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response from the OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model=selected_model,
                messages=st.session_state.messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
            reply = response['choices'][0]['message']['content']
            st.session_state.messages.append({"role": "assistant", "content": reply})

            with st.chat_message("assistant"):
                st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")






