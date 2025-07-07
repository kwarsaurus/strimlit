import streamlit as st
import requests
import json

# Judul aplikasi
st.title("🤖 Qwen Chatbot")
st.write("Powered by DashScope International")

# Sidebar untuk API key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input(
    "API Key:", 
    type="password", 
    value="sk-ce46c47e696542268e5f3745d56ef034"
)

# Pilihan model
model_options = ["qwen-max", "qwen-plus", "qwen-turbo"]
selected_model = st.sidebar.selectbox("Pilih Model:", model_options)

# Parameter
temperature = st.sidebar.slider("Temperature:", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens:", 50, 2000, 500, 50)

# Fungsi untuk chat dengan Qwen
def chat_with_qwen(message, api_key, model, temp, max_tok):
    url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": temp,
        "max_tokens": max_tok
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Area chat
st.header("💬 Chat dengan Qwen")

# Input pengguna
user_input = st.text_area("Tulis pesan Anda:", height=100, placeholder="Ketik pertanyaan atau pesan di sini...")

# Tombol kirim
if st.button("🚀 Kirim", type="primary"):
    if user_input and api_key:
        with st.spinner(f"🤔 {selected_model} sedang berpikir..."):
            response = chat_with_qwen(user_input, api_key, selected_model, temperature, max_tokens)
        
        # Tampilkan response
        st.success("✅ Response dari Qwen:")
        st.write(response)
        
    elif not user_input:
        st.warning("⚠️ Silakan tulis pesan terlebih dahulu!")
    elif not api_key:
        st.error("❌ Silakan masukkan API Key!")

# Info
st.markdown("---")
st.info("💡 **Tips:** Gunakan temperature rendah (0.1-0.3) untuk jawaban konsisten, atau tinggi (0.7-1.0) untuk jawaban kreatif.")

# Footer
st.markdown("---")
st.caption("Dibuat dengan ❤️ menggunakan Streamlit dan Qwen API")
