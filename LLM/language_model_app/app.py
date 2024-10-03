import streamlit as st
import ollama

SYSTEM_PROMPT = "You are a helpful AI assistant."
SYSTEM_MESSAGE = [{"role": "system","content": SYSTEM_PROMPT}]
models = ollama.list()

def format_func(option: dict) -> str:
    return f"{option['name']} ({round(option['size'] / 10**9, 1)} Gb)"

model_dict = st.selectbox(label="Select a Model", options=models["models"], format_func=format_func)
model = model_dict["name"]

def stream_response(model: str, messages: list):
    try:
        messages = SYSTEM_MESSAGE + messages
        stream = ollama.chat(model=model, messages=messages, stream=True)
    except Exception as e:
        stream = f"LLM ERROR: {e}"
    return stream

def stream_wrapper(stream):
    print(stream)
    for chunk in stream:
        print(chunk)
        yield chunk['message']['content']

st.title(f"Chat with _{model}_")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("New Chat"):
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your message"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    stream = stream_wrapper(stream_response(model, st.session_state.messages))
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # st.markdown(response)
        # for chunk in stream:
        #     st.write(chunk['message']['content'])
        msg = st.write_stream(stream)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": msg})



# import ollama

# stream = ollama.chat(
#     model='llama3.1',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)

# with st.chat_message(“assistant”):
# msg = st.write_stream(response)