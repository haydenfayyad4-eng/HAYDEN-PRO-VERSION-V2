import streamlit as st
import os
from pekerja import bos_hayden, simpan_belajar
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖")
st.title("🤖 HAYDEN-PRO-VERSION V2")
st.caption("Bos: Adam dari Seremban | Cikgu: Gemini | Pekerja: 3000")

# --- API KEY - DAH BETUL, TAKKAN ERROR LAGI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""
try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except:
    NEWS_API_KEY = ""

# --- GEMINI SETUP ---
model = None
gemini_error = ""
if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        model = None
        gemini_error = str(e)

# --- CHAT HISTORY ---
if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.write(m["text"])

tanya = st.chat_input("Tanya HAYDEN apa-apa...")
if tanya:
    st.session_state.chat.append({"role": "user", "text": tanya})
    with st.chat_message("user"):
        st.write(tanya)

    with st.chat_message("assistant"):
        with st.spinner("HAYDEN tengah fikir..."):
            jawapan = ""

            # Kalau user nak ajar HAYDEN
            if tanya.lower().startswith("ajar aku"):
                try:
                    bahagian = tanya.split("|", 2)
                    soalan_baru = bahagian[1].strip()
                    jawapan_baru = bahagian[2].strip()
                    simpan_belajar(soalan_baru, jawapan_baru)
                    jawapan = "Ok Bos, dah simpan. Nanti kalau orang tanya '" + soalan_baru + "', aku jawab '" + jawapan_baru + "'"
                except:
                    jawapan = "Format salah Bos. Taip macam ni: ajar aku | apa itu kucing | kucing tu haiwan comel"

            else:
                # LAPIS 1: PEKERJA + BELAJAR + SECURITY
                jawapan = bos_hayden(tanya)

                # LAPIS 2: PENGETAHUAN - Wikipedia + Kamus + Berita + Hukum Syarak
