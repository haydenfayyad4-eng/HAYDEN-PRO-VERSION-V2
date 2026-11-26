import streamlit as st
import os
from pekerja import bos_hayden, simpan_belajar
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖")
st.title("🤖 HAYDEN-PRO-VERSION V2")
st.caption("Bos: Adam dari Seremban")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""
try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except:
    NEWS_API_KEY = ""

model = None
gemini_error = ""
MODEL_LIST = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai
    except Exception as e:
        model = None
        gemini_error = str(e)

def tanya_gemini(prompt):
    global gemini_error
    for nama_model in MODEL_LIST:
        try:
            m = model.GenerativeModel(nama_model)
            res = m.generate_content(prompt)
            return res.text.strip()
        except Exception as e:
            gemini_error = str(e)
            continue
    return None

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
                jawapan = bos_hayden(tanya)
                if jawapan == "TAK_TAHU":
                    cari = cari_pengetahuan(tanya, NEWS_API_KEY)
                    if cari:
                        jawapan = cari
                if jawapan == "TAK_TAHU" and model:
                    prompt = CARA_JAWAB + "\nInfo: " + HAYDEN_INFO + "\nSoalan: " + tanya
                    hasil = tanya_gemini(prompt)
                    if hasil:
                        jawapan = hasil
                    else:
                        jawapan = "GEMINI ERROR: " + gemini_error
                if jawapan == "TAK_TAHU":
                    if not API_KEY:
                        jawapan = "GEMINI ERROR: API KEY KOSONG - Secrets takde key"
                    elif gemini_error:
                        jawapan = "GEMINI ERROR SETUP: " + gemini_error
                    else:
                        jawapan = "Aku tak tahu lagi yang ni, Bos. Ajar aku? Taip: ajar aku | soalan | jawapan"
            st.write(jawapan)
            st.session_state.chat.append({"role": "assistant", "text": jawapan})
