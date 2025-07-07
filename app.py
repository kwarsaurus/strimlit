import streamlit as st

# Judul aplikasi
st.title("🤖 Chatbot")

# Sidebar untuk API key
st.sidebar.title("Pengaturan")
api_key = st.sidebar.text_input("Masukkan API Key:", type="password", value="sk-ce46c47e696542268e5f3745d56ef034")

# Area chat
st.header("Chat dengan Bot")

# Input pengguna
user_input = st.text_input("Tulis pesan Anda:")

if user_input and api_key:
    # Respon sederhana (nanti bisa diganti dengan AI)
    st.write("🤖 Bot:", f"Anda berkata: '{user_input}'")
    st.write("API Key tersimpan:", api_key[:10] + "...")
elif user_input and not api_key:
    st.error("Silakan masukkan API Key terlebih dahulu!")

# Info
st.info("Ini adalah aplikasi chatbot sederhana menggunakan Streamlit")
