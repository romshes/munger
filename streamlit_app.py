import streamlit as st
import os
import openai
from PIL import Image

st.set_page_config(page_title="Chat with your Financial Report")

# Add a local image at the top of the page
image_path = r"cm3.PNG"
image = Image.open(image_path)

# Resize the image safely
max_width, max_height = 800, 600
image = image.resize((max_width, max_height))

# Display the image
st.image(image, use_column_width=True)

# Explanation text
st.write("""
The GPT-4O foundation model was fine-tuned on 100 'mungerisms', allowing the user to chat with the late Charlie Munger.
A mungerism refers to a mental model or a practical approach to thinking that is associated with Charles Munger, the vice chairman of Berkshire Hathaway and the long-time business partner of Warren Buffett. These 'mungerisms' are practical philosophies that Munger has shared through his speeches, writings, and interviews. They are highly regarded by those interested in investing, business strategy, and critical thinking.
""")

# Function to get OpenAI API key
def get_openai_api_key():
    openai_api = st.text_input('Enter OpenAI API Key:', type='password')
    if openai_api and openai_api.startswith('sk-'):
        st.success('Valid API key entered!', icon="✅")
        return openai_api
    elif openai_api:
        st.error('Please enter a valid OpenAI API Key!', icon="⚠️")
    return None

# Store API key in session state
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = get_openai_api_key()

openai_api = st.session_state['openai_api_key']
if openai_api:
    openai.api_key = openai_api  # Set OpenAI API key

# Sidebar for model and parameters
with st.sidebar:
    st.subheader("Specify your Model and Parameters")
    model_options = {
        'Charlie Munger Jr. Model': 'ft:gpt-4o-2024-08-06:personal::A1OKDWJz',
        'GPT-4 Model': 'gpt-4',
        'GPT-3.5 Turbo Model': 'gpt-3.5-turbo'
    }

    selected_model_name = st.selectbox('Choose an OpenAI model:', list(model_options.keys()))
    selected_model = model_options[selected_model_name]

    temperature = st.slider('Temperature', min_value=0.0, max_value=1.5, value=0.7, step=0.01)
    top_p = st.slider('Top_p', min_value=0.01, max_value=1.0, value=0.95, step=0.01)
    max_tokens = st.slider('Max Tokens', min_value=1, max_value=500, value=200, step=1)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "Charlie Munger jr. is a factual chatbot that shares words of wisdom from seasoned financial advisors."}
    ]

# Display chat history
for message in st.session_state['messages']:
    if message['role'] in {"user", "assistant"}:
        st.write(f"{message['role'].capitalize()}: {message['content']}")

# Clear chat history function
def clear_chat_history():
    st.session_state['messages'] = [
        {"role": "system", "content": "Charlie Munger jr. is a factual chatbot that shares words of wisdom from seasoned financial advisors."}
    ]

st.sidebar.subheader('Manage your chat history')
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function to generate chat history and get response
def chat_history(model, temperature, top_p, max_tokens):
    try:
        # Use OpenAI's new chat completion API
        response = openai.ChatCompletion.create(
            model=model,
            messages=st.session_state['messages'],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# User input for the prompt
if prompt := st.chat_input(disabled=not openai_api):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Generate and display assistant response
    if st.session_state['messages']:
        with st.spinner("Thinking..."):
            response = chat_history(selected_model, temperature, top_p, max_tokens)
            if response:
                st.session_state['messages'].append({"role": "assistant", "content": response})
                st.write(f"Assistant: {response}")






