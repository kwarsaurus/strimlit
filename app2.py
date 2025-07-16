import os
import streamlit as st
from openai import OpenAI
from http import HTTPStatus
from dashscope import Application
import dashscope

# --- Configuration ---
DASHSCOPE_API_KEY = "sk-ce46c47e696542268e5f3745d56ef034"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
APP_API_URL = "https://dashscope-intl.aliyuncs.com/api/v1"
APP_ID = "4e4b442cf70b4264999d54e5c3887afd"

# Set global API key and URL for DashScope Application
dashscope.api_key = DASHSCOPE_API_KEY
dashscope.base_http_api_url = APP_API_URL

SUPPORTED_MODELS = ["qwen-plus", "qwen-turbo", "qwen-max"]

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Qwen Chatbot", layout="centered")
st.title("🤖 Qwen Chatbot")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Mode selection
    chat_mode = st.selectbox(
        "Chat Mode:",
        ["OpenAI-Compatible", "Custom Application"],
        help="Choose how to interact with Qwen"
    )
    
    if chat_mode == "OpenAI-Compatible":
        selected_model = st.selectbox("Model:", SUPPORTED_MODELS)
        st.info(f"Using: **{selected_model}**")
        
        # Model descriptions
        model_info = {
            "qwen-plus": "⚡ Balanced performance",
            "qwen-turbo": "🚀 Fast and cost-effective", 
            "qwen-max": "🧠 Best for complex tasks"
        }
        st.caption(model_info[selected_model])
    else:
        custom_app_id = st.text_input("App ID:", value=APP_ID)
        st.info("Using: **Custom Application**")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# --- Chat Interface ---
st.header("💬 Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            if chat_mode == "OpenAI-Compatible":
                try:
                    client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=BASE_URL)
                    
                    # Prepare messages for API (include chat history)
                    messages = [{"role": "system", "content": "You are a helpful assistant."}]
                    messages.extend(st.session_state.messages)
                    
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=messages,
                        stream=True
                    )
                    
                    # Stream response
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in response:
                        if chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            response_placeholder.markdown(full_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            else:  # Custom Application mode
                try:
                    response = Application.call(
                        api_key=DASHSCOPE_API_KEY,
                        app_id=custom_app_id,
                        prompt=prompt
                    )
                    
                    if response.status_code != HTTPStatus.OK:
                        error_msg = f"Error {response.status_code}: {response.message}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    else:
                        response_text = response.output.text
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                except Exception as e:
                    error_msg = f"Exception: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# --- Footer ---
st.markdown("---")
st.caption("💡 **Tips:** Switch between OpenAI-Compatible and Custom Application modes in the sidebar")
