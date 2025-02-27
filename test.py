import os
import streamlit as st

st.write("📂 Daftar file di direktori saat ini:")
st.write(os.listdir())  # Menampilkan semua file di root direktori
