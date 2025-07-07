import streamlit as st
import requests

st.title("🤖 Qwen Model Studio Chatbot")

api_key = st.sidebar.text_input("API Key:", type="password", value="sk-ce46c47e696542268e5f3745d56ef034")

def query_qwen(text, api_key):
    url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-SSE": "disable"
    }
    
    data = {
        "model": "qwen-turbo",
        "input": {
            "prompt": text
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

user_input = st.text_input("Pesan:")

if user_input and api_key:
    try:
        result = query_qwen(user_input, api_key)
        st.write("Debug response:", result)  # Untuk lihat response asli
        
        if "output" in result:
            st.write("🤖 Qwen:", result["output"]["text"])
        else:
            st.error(f"Error: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
