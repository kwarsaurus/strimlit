import os
import streamlit as st
from openai import OpenAI
from http import HTTPStatus
from dashscope import Application
import dashscope

# --- Configuration ---
DASHSCOPE_API_KEY = "sk-4619351667f34e5f82aa482e0e23ee6e"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
APP_API_URL = "https://dashscope-intl.aliyuncs.com/api/v1"
APP_ID = "1985617e94bb4d9291b1896194455aef"  # Replace with your actual application ID

# Set global API key and URL for DashScope Application
dashscope.api_key = DASHSCOPE_API_KEY
dashscope.base_http_api_url = APP_API_URL

SUPPORTED_MODELS = ["qwen-plus", "qwen-turbo", "qwen-max"]

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Qwen Chatbot", layout="centered")
st.title("🤖 Qwen Chatbot (DashScope)")
st.markdown("Interact with Qwen using either OpenAI-style models or custom AppID API.")

# --- Tabs ---
tab1, tab2 = st.tabs(["🔧 OpenAI-Compatible Models", "🧩 Custom AppID Application"])

# --- Tab 1: OpenAI-Compatible Chat ---
with tab1:
    st.header("🔧 OpenAI-Compatible Model Chat")
    with st.sidebar:
        st.subheader("Settings")
        selected_model = st.selectbox("Choose a model:", SUPPORTED_MODELS)
        st.markdown("""
        - **qwen-plus**: Balanced performance  
        - **qwen-turbo**: Fast and low-cost  
        - **qwen-max**: Best for complex tasks
        """)

    user_input_1 = st.text_input("Your message:", value="Who are you?", key="tab1_input")

    if st.button("Send via OpenAI-Compatible API", key="tab1_send"):
        if not user_input_1.strip():
            st.warning("Please enter a message.")
        else:
            client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=BASE_URL)

            with st.spinner("Thinking..."):
                try:
                    stream = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_input_1}
                        ],
                        stream=True
                    )

                    st.write("### Response:")
                    response_area = st.empty()
                    full_response = ""

                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            response_area.markdown(full_response)

                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")
                    st.info("Refer to: https://help.alibabacloud.com/en/model-studio/developer-reference/error-code")

# --- Tab 2: Application-based Chat ---
with tab2:
    st.header("🧩 DashScope Application-based Chat")

    user_input_2 = st.text_input("Your message (App Call):", value="Who are you?", key="tab2_input")
    custom_app_id = st.text_input("Application ID", value=APP_ID)

    if st.button("Send via Application API", key="tab2_send"):
        if not user_input_2.strip() or not custom_app_id.strip():
            st.warning("Please enter both message and App ID.")
        else:
            with st.spinner("Calling Application API..."):
                try:
                    response = Application.call(
                        api_key=DASHSCOPE_API_KEY,
                        app_id=custom_app_id,
                        prompt=user_input_2
                    )

                    if response.status_code != HTTPStatus.OK:
                        st.error(f"❌ Error {response.status_code}: {response.message}")
                        st.code(f"Request ID: {response.request_id}", language="text")
                        st.markdown("[View error codes](https://www.alibabacloud.com/help/en/model-studio/developer-reference/error-code)")
                    else:
                        st.success("✅ Response:")
                        st.write(response.output.text)

                except Exception as e:
                    st.error(f"Exception: {e}")
