import streamlit as st
import requests
import json

# Judul aplikasi
st.title("🤖 Qwen Model Studio Chatbot")

# Sidebar untuk API key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input("Masukkan Qwen API Key:", type="password", value="sk-ce46c47e696542268e5f3745d56ef034")

# Fungsi untuk query Qwen
def query_qwen(text, api_key):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "user", "content": text}
            ]
        },
        "parameters": {
            "max_tokens": 500,
            "temperature": 0.7
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Area chat
st.header("Chat dengan Qwen")

# Input pengguna
user_input = st.text_input("Tulis pesan Anda:")

if user_input and api_key:
    try:
        with st.spinner("Qwen sedang berpikir..."):
            result = query_qwen(user_input, api_key)
            
        if "output" in result and "text" in result["output"]:
            bot_response = result["output"]["text"]
            st.write("🤖 **Qwen:**", bot_response)
        else:
            st.error("Error: " + str(result))
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
elif user_input and not api_key:
    st.error("Silakan masukkan Qwen API Key!")

st.info("Chatbot menggunakan Qwen dari Alibaba Cloud Model Studio")
