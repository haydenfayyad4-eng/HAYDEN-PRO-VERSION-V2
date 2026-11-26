import streamlit as st
import os
from pekerja import bos_hayden, simpan_belajar, JUMLAH_PEKERJA
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖")

st.markdown("""
<style>
.stAppDeployButton {display: none !important; visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 HAYDEN-PRO-VERSION V2")
st.caption("Online • Tanya HAYDEN apa-apa")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""
try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except:
    NEWS_API_KEY = ""

client = None
gemini_error = ""
MODEL_LIST_DAPAT = []
MODEL_CUBA = []

if API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        try:
            for m in client.models.list():
                nama = m.name.replace("models/", "")
                MODEL_LIST_DAPAT.append(nama)
            UTAMA = ["gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.1-flash", "gemini-2.0-flash-lite"]
            for u in UTAMA:
                if u in MODEL_LIST_DAPAT:
                    MODEL_CUBA.append(u)
            for n in MODEL_LIST_DAPAT:
                if "flash" in n.lower() and n not in MODEL_CUBA and "image" not in n.lower() and "preview" not in n.lower():
                    MODEL_CUBA.append(n)
        except Exception as e:
            gemini_error = "LIST GAGAL: " + str(e)
    except Exception as e:
        client = None
        gemini_error = str(e)

def tanya_gemini(prompt):
    global gemini_error
    for nama_model in MODEL_CUBA:
        try:
            res = client.models.generate_content(model=nama_model, contents=prompt)
            if res.text:
                st.session_state["model_jaya"] = nama_model
                return res.text.strip()
        except Exception as e:
            gemini_error = f"[{nama_model}] {str(e)}"
            continue
    return None

def check_kuota():
    if not client:
        return "❌ API KEY TAKDE / ROSAK"
    if not MODEL_CUBA:
        return "❌ TAKDE MODEL FLASH. Model Google bagi: " + str(MODEL_LIST_DAPAT)
    hasil = tanya_gemini("hi")
    if hasil:
        return f"✅ KUOTA MASIH ADA! Model yang berjaya: {st.session_state.get('model_jaya', '?')} | Dah guna {st.session_state.get('guna_gemini', 0)} kali"
    teks = gemini_error
    if "429" in teks or "quota" in teks.lower() or "exceeded" in teks.lower():
        return "🛑 KUOTA DAH HABIS! Tunggu esok. Error: " + teks
    return "❌ ERROR: " + teks

if "chat" not in st.session_state:
    st.session_state.chat = []
if "guna_gemini" not in st.session_state:
    st.session_state.guna_gemini = 0
if "model_jaya" not in st.session_state:
    st.session_state.model_jaya = "-"

with st.sidebar:
    st.write("📊 **KUOTA HAYDEN**")
    st.write(f"Model berjaya tadi: {st.session_state.model_jaya}")
    st.write(f"Dah guna Gemini: {st.session_state.guna_gemini} kali")
    if st.button("Check Kuota Sekarang"):
        with st.spinner("Check..."):
            st.info(check_kuota())
    st.write("**Error Terakhir:**")
    st.code(gemini_error if gemini_error else "Tiada error lagi", language="text")
    with st.expander("Senarai Model Cuba"):
        st.write(MODEL_CUBA)

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
            t_lower = tanya.lower().strip()
            if t_lower in ["check kuota", "kuota", "check quota", "baki kuota"]:
                jawapan = check_kuota()
            elif t_lower.startswith("ajar aku"):
                try:
                    bahagian = tanya.split("|", 3)
                    kod_bos = bahagian[1].strip()
                    soalan_baru = bahagian[2].strip()
                    jawapan_baru = bahagian[3].strip()
                    if kod_bos == "ADAM-BOS":
                        simpan_belajar(soalan_baru, jawapan_baru)
                        jawapan = "Ok, dah simpan."
                    else:
                        jawapan = "Eh, kod salah."
                except:
                    jawapan = "Format: ajar aku | ADAM-BOS | soalan | jawapan"
            else:
                jawapan = bos_hayden(tanya)
                if jawapan == "TAK_TAHU":
                    cari = cari_pengetahuan(tanya, NEWS_API_KEY)
                    if cari:
                        jawapan = cari
                if jawapan == "TAK_TAHU" and client:
                    prompt = CARA_JAWAB + "\nInfo: " + HAYDEN_INFO + "\nSoalan: " + tanya
                    hasil = tanya_gemini(prompt)
                    if hasil:
                        jawapan = hasil
                        st.session_state.guna_gemini += 1
                    else:
                        jawapan = "GEMINI ERROR: " + gemini_error
                if jawapan == "TAK_TAHU":
                    if not API_KEY:
                        jawapan = "GEMINI ERROR: API KEY KOSONG"
                    elif gemini_error:
                        jawapan = "GEMINI ERROR SETUP: " + gemini_error
                    else:
                        jawapan = "Aku tak tahu lagi yang ni."
            st.write(jawapan)
            st.session_state.chat.append({"role": "assistant", "text": jawapan})
