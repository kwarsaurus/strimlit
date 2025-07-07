import streamlit as st
import requests

# Judul aplikasi
st.title("🤖 Qwen Chatbot")

# Sidebar untuk API key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input(
    "API Key:", 
    type="password", 
    value="sk-ce46c47e696542268e5f3745d56ef034"
)

# Pilihan model
model_type = st.sidebar.radio(
    "Jenis Model:",
    ["Model Standar", "Model Custom"]
)

if model_type == "Model Standar":
    model_options = ["qwen-max", "qwen-plus", "qwen-turbo"]
    selected_model = st.sidebar.selectbox("Pilih Model:", model_options)
else:
    # Input untuk custom model ID
    selected_model = st.sidebar.text_input(
        "Custom Model ID:", 
        value="4e4b442cf70b4264999d54e5c3887afd",
        help="Masukkan ID model custom Anda"
    )

# Parameter
temperature = st.sidebar.slider("Temperature:", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens:", 50, 2000, 500, 50)

# Fungsi chat
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
st.header("💬 Chat")

# Tampilkan model yang digunakan
if model_type == "Model Custom":
    st.info(f"🎯 Menggunakan custom model: `{selected_model}`")
else:
    st.info(f"🤖 Menggunakan model: `{selected_model}`")

# Input pengguna
user_input = st.text_area("Tulis pesan:", height=100)

# Tombol kirim
if st.button("🚀 Kirim", type="primary"):
    if user_input and api_key and selected_model:
        with st.spinner("🤔 Sedang memproses..."):
            response = chat_with_qwen(user_input, api_key, selected_model, temperature, max_tokens)
        
        st.success("✅ Response:")
        st.write(response)
        
    else:
        st.warning("⚠️ Lengkapi semua field!")

# Footer
st.markdown("---")
st.caption("Support model standar dan custom fine-tuned")
