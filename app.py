import streamlit as st
import requests
import json

# Judul aplikasi
st.title("🤖 Qwen Chatbot")

# Sidebar untuk API key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input("Masukkan HF API Key:", type="password", value="sk-ce46c47e696542268e5f3745d56ef034")

# Fungsi untuk query Qwen
def query_qwen(text, api_key):
    API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    payload = {
        "inputs": text,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Area chat
st.header("Chat dengan Qwen")

# Input pengguna
user_input = st.text_input("Tulis pesan Anda:")

if user_input and api_key:
    try:
        with st.spinner("Qwen sedang berpikir..."):
            result = query_qwen(user_input, api_key)
            
        if isinstance(result, list) and len(result) > 0:
            bot_response = result[0].get('generated_text', 'Maaf, tidak ada respons.')
            st.write("🤖 **Qwen:**", bot_response)
        else:
            st.error("Error: " + str(result))
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        
elif user_input and not api_key:
    st.error("Silakan masukkan Hugging Face API Key terlebih dahulu!")

# Info
st.info("Chatbot menggunakan model Qwen dari Hugging Face")
