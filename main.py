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
st.caption(f"Bos: Adam dari Seremban | Pekerja: {JUMLAH_PEKERJA} orang")

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
MODEL_LIST = ["gemini-2.5-flash-lite", "gemini-2.0-flash-lite", "gemini-2.0-flash"]
if API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        client = None
        gemini_error = str(e)

def tanya_gemini(prompt):
    global gemini_error
    for nama_model in MODEL_LIST:
        try:
            res = client.models.generate_content(model=nama_model, contents=prompt)
            return res.text.strip()
        except Exception as e:
            gemini_error = str(e)
            continue
    return None

def check_kuota():
    # Test panggil Gemini dengan soalan paling pendek, paling jimat kuota
    if not client:
        return "❌ API KEY TAKDE / ROSAK. Kena buat API Key baru kat aistudio.google.com/apikey"
    try:
        res = client.models.generate_content(model="gemini-2.5-flash-lite", contents="hi")
        # Kalau sampai sini, maknanya kuota masih ada
        return "✅ KUOTA MASIH ADA! API Key kau elok. Boleh tanya macam biasa. Tadi kau dah guna " + str(st.session_state.get("guna_gemini", 0)) + " kali dalam sesi ni."
    except Exception as e:
        teks = str(e)
        if "429" in teks or "quota" in teks.lower() or "exceeded" in teks.lower():
            return "🛑 KUOTA DAH HABIS! Google kata dah limit. Tunggu esok pagi, dia reset balik sendiri. Jangan tanya lagi hari ni, nanti dia block lagi lama."
        if "404" in teks or "not found" in teks.lower():
            return "⚠️ 404 - MODEL TAK JUMPA. Bukan kuota habis, tapi nama model tu Google dah tukar. Kena update MODEL_LIST kat main.py."
        if "API_KEY_INVALID" in teks or "API key not valid" in teks:
            return "❌ API KEY SALAH / DAH MATI. Kena buat API Key baru, paste kat Secrets, Reboot."
        return "❌ ERROR LAIN: " + teks

if "chat" not in st.session_state:
    st.session_state.chat = []
if "guna_gemini" not in st.session_state:
    st.session_state.guna_gemini = 0

# SIDEBAR KUOTA
with st.sidebar:
    st.write("📊 **KUOTA HAYDEN**")
    st.write(f"Dah guna Gemini: {st.session_state.guna_gemini} kali (sesi ni)")
    if st.button("Check Kuota Sekarang"):
        with st.spinner("Check..."):
            st.info(check_kuota())

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
            if t_lower in ["check kuota", "kuota", "check quota", "baki kuota", "kuota habis ke"]:
                jawapan = check_kuota()
            elif t_lower.startswith("ajar aku"):
                try:
                    bahagian = tanya.split("|", 3)
                    kod_bos = bahagian[1].strip()
                    soalan_baru = bahagian[2].strip()
                    jawapan_baru = bahagian[3].strip()
                    if kod_bos == "ADAM-BOS":
                        simpan_belajar(soalan_baru, jawapan_baru)
                        jawapan = "Ok Bos, dah simpan."
                    else:
                        jawapan = "Eh, ajar aku ni untuk Bos Adam je."
                except:
                    jawapan = "Format Bos sahaja: ajar aku | ADAM-BOS | soalan | jawapan"
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
                        jawapan = "Aku tak tahu lagi yang ni, Bos."
            st.write(jawapan)
            st.session_state.chat.append({"role": "assistant", "text": jawapan})
