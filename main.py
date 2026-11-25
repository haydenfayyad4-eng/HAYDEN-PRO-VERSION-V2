import streamlit as st
import os
from pekerja import bos_hayden, simpan_belajar, load_belajar
from pengetahuan import cari_pengetahuan

# LAPIS 1.5: PENGETAHUAN (Wikipedia + Kamus + Berita + Hukum)
pengetahuan = cari_pengetahuan(tanya, NEWS_API_KEY)
if pengetahuan:
    jawapan = pengetahuan
elif jawapan == "TAK_TAHU" and model:
    # baru tanya Gemini...

NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "") if hasattr(st, "secrets") else ""

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖")
st.title("🤖 HAYDEN-PRO-VERSION V2")
st.caption("Bos: Adam dari Seremban | Cikgu: Gemini | Pekerja: 3000")

# --- API KEY ---
# Letak kat Streamlit Secrets: GEMINI_API_KEY = "AIza..."
API_KEY = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
API_KEY = API_KEY or os.getenv("GEMINI_API_KEY", "")

# --- GEMINI SETUP ---
model = None
if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception:
        model = None

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
            # LAPIS 1: PEKERJA + BELAJAR (laju, tak pakai quota)
            jawapan = bos_hayden(tanya)

            # LAPIS 2: GEMINI (kalau pekerja tak tahu)
            if jawapan == "TAK_TAHU" and model:
                try:
                    prompt = f"""{CARA_JAWAB}
Bos kau Adam dari Seremban.
Info tentang kau: {HAYDEN_INFO}
Soalan: {tanya}
Jawab santai macam kawan Malaysia, pendek, jangan kaku."""
                    res = model.generate_content(prompt)
                    jawapan = res.text.strip()
                except Exception:
                    jawapan = "TAK_TAHU"

            # LAPIS 3: KALAU BETUL TAK TAHU
            if jawapan == "TAK_TAHU":
                jawapan = "Aku tak tahu lagi yang ni, Bos. Ajar aku? Taip: ajar aku | soalan | jawapan"

            # LAPIS BELAJAR: kalau user ajar
            if tanya.lower().startswith("ajar aku"):
                try:
                    _, soalan, jawapan_baru = tanya.split("|", 2)
                    simpan_belajar(soalan.strip(), jawapan_baru.strip())
                    jawapan = f"Ok Bos, dah simpan. Nanti kalau orang tanya '{soalan.strip()}', aku jawab '{jawapan_baru.strip()}'"
                except:
                    jawapan = "Format salah Bos. Taip macam ni: ajar aku | apa itu kucing | kucing tu haiwan comel"

            st.write(jawapan)
            st.session_state.chat.append({"role": "assistant", "text": jawapan})
