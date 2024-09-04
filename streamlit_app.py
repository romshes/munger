import streamlit as st
import openai
from PIL import Image

st.set_page_config(page_title="Chat with your Financial Report")

# Load and display the image
image_path = r"cm3.PNG"
image = Image.open(image_path)
max_width = 800
max_height = 600
image.thumbnail((max_width, max_height))
st.image(image, use_column_width=True)

st.write("""
The GPT-4O foundation model was fine-tuned on 100 'mungerisms', allowing the user to chat with the late Charlie Munger.
""")
st.write("""
A mungerism refers to a mental model or a practical approach to thinking that is associated with Charles Munger, the vice chairman of Berkshire Hathaway and the long-time business partner of Warren Buffett. These 'mungerisms' are practical philosophies that Munger has shared through his speeches, writings, and interviews. They are highly regarded by those interested in investing, business strategy, and critical thinking.
""")

# Sidebar for API key, model, and settings
with st.sidebar:
    st.subheader("Specify your API Key")
    api_key = st.text_input('Enter OpenAI API Key:', type='password')

    if api_key:
        openai.api_key = api_key
        st.success("API Key has been entered.")
    else:
        st.error("Please enter your OpenAI API key to proceed.")

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

    st.markdown(f'Chosen model: {selected_model}, temperature = {temperature}, top_p = {top_p}, max_tokens = {max_tokens}')

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Charlie Munger jr. is a factual chatbot, that shares words of wisdom from seasoned financial advisor."}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] in {"user", "assistant"}:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Clear chat history button
def clear_chat_history():
    st.session_state.messages = [{"role": "system", "content": "Charlie Munger jr. is a factual chatbot, that shares words of wisdom from seasoned financial advisor."}]

st.sidebar.subheader('Manage your chat history')
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Chat input (only enabled if the API key is entered)
if api_key:
    if prompt := st.chat_input("Type your message here:"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Function to generate a response using the OpenAI API
        def chat_history(model, temperature, top_p, max_tokens):
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )
                return response['choices'][0]['message']['content']
            except Exception as e:
                return f"Error: {str(e)}"

        # Generate a response if there is a user message
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_history(selected_model, temperature, top_p, max_tokens)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})




