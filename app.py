import streamlit as st
import openai

# Judul aplikasi
st.title("🤖 OpenAI Chatbot")

# Sidebar untuk API key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input("Masukkan OpenAI API Key:", type="password", value="sk-ce46c47e696542268e5f3745d56ef034")

# Setup OpenAI client
if api_key:
    client = openai.OpenAI(api_key=api_key)

# Area chat
st.header("Chat dengan GPT")

# Input pengguna
user_input = st.text_input("Tulis pesan Anda:")

if user_input and api_key:
    try:
        with st.spinner("GPT sedang berpikir..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # atau "gpt-4" jika ada akses
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
        bot_response = response.choices[0].message.content
        st.write("🤖 **GPT:**", bot_response)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
elif user_input and not api_key:
    st.error("Silakan masukkan OpenAI API Key terlebih dahulu!")

# Info
st.info("Chatbot menggunakan model GPT dari OpenAI")
