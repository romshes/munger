import streamlit as st
import os
from openai import OpenAI
from PIL import Image

st.set_page_config(page_title="Chat with your Financial Report")


# Add a local image at the top of the page
# Load the image
image_path = r"cm3.PNG"
image = Image.open(image_path)

# Resize the image
max_width = 800  # You can adjust this value
max_height = 600  # You can adjust this value
image.thumbnail((max_width, max_height))

# Display the image
st.image(image, use_column_width=True)


st.write("""
The GPT-4o foundation model was fine-tuned on 100 'mungerisms', allowing the user to chat with the late Charlie Munger.
""")

st.write("""
A mungerism refers to a mental model or a practical approach to thinking that is associated with Charles Munger, the vice chairman of Berkshire Hathaway and the long-time business partner of Warren Buffett. These 'mungerisms' are practical philosophies that Munger has shared through his speeches, writings, and interviews. They are highly regarded by those interested in investing, business strategy, and critical thinking.
You will need an OpenAI API key to use this app.""")
def get_openai_api_key():
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon="✅")
        openai_api = st.secrets['openai_api_key']
    else:
        openai_api = st.text_input('Enter OpenAI API Key', type='password')
        if not (openai_api.startswith('sk-') and len(openai_api) != 51):
            st.warning('Please enter your key credentials!', icon="⚠️")
        else:
            st.success('Proceed to entering your prompt message!', icon="👍")

    os.environ['OPENAI_API_KEY'] = openai_api
    return openai_api

with st.sidebar:

    st.subheader("Specify your API Key")
    openai_api = get_openai_api_key()

    st.subheader("Specify your Model and Parameters")
    #selected_model = st.selectbox('Choose an OpenAI model:', ['ft:gpt-4o-2024-08-06:personal::A1OKDWJz', 'gpt-4', 'gpt-3.5-turbo'])


    # Mapping of user-friendly names to actual model names
    model_options = {
        'Charlie Munger Jr. Model': 'ft:gpt-4o-2024-08-06:personal::A1OKDWJz',
        'GPT-4 Model': 'gpt-4',
        'GPT-3.5 Turbo Model': 'gpt-3.5-turbo'
    }

    # Create a selectbox with the user-friendly names
    selected_model_name = st.selectbox('Choose an OpenAI model:', list(model_options.keys()))
    selected_model = model_options[selected_model_name]




    temperature = st.slider('Temperature', min_value=0.0, max_value=1.5, value=0.7, step=0.01)
    top_p = st.slider('Top_p', min_value=0.01, max_value=1.0, value=0.95, step=0.01)
    max_tokens = st.slider('Max Tokens', min_value=1, max_value=500, value=200, step=1)

    st.markdown('You have chosen your model and parameters:')
    st.markdown(f'{selected_model}, temperature = {temperature}, top_p = {top_p}, max_tokens = {max_tokens}')

# Initialize chat
# Initialize chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add the system message to the chat context, but don't display it
    st.session_state.messages.append(
        {"role": "system", "content": "Charlie Munger jr. is a factual chatbot, that shares words of wisdom from seasoned financial advisor."}
    )

# Display chat history (excluding system messages)
for message in st.session_state.messages:
    if message["role"] in {"user", "assistant"}:  # Only display user and assistant messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Clear chat messages history
# Clear chat history function
def clear_chat_history():
    st.session_state.messages = []
    # Re-add the system message to the chat context after clearing
    st.session_state.messages.append(
        {"role": "system", "content": "Charlie Munger jr. is a factual chatbot, that shares words of wisdom from seasoned financial advisor."}
    )

st.sidebar.subheader('Manage your chat history')
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if prompt := st.chat_input(disabled=not openai_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Function to generate chat history and get response
def chat_history(model, temperature, top_p, max_tokens):

    openai_api =os.environ.get("openai_api_key")
    client =OpenAI(api_key=openai_api)
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

    # Access the message content correctly
    return response.choices[0].message.content


# Only generate a response if there are messages from the user
# Only generate a response if there are messages from the user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_history(selected_model, temperature, top_p, max_tokens)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})







