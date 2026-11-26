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
MODEL_PILIH = None
MODEL_LIST_DAPAT = []

if API_KEY:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        # TANYA GOOGLE SENDIRI MODEL APA YANG ADA UNTUK KUNCI NI
        try:
            for m in client.models.list():
                nama = m.name.replace("models/", "")
                MODEL_LIST_DAPAT.append(nama)
            # Cari yang ada perkataan flash dulu, sebab paling laju & free
            for n in MODEL_LIST_DAPAT:
                if "flash" in n.lower() and "2.5" in n:
                    MODEL_PILIH = n
                    break
            if not MODEL_PILIH:
                for n in MODEL_LIST_DAPAT:
                    if "flash" in n.lower():
                        MODEL_PILIH = n
                        break
            if not MODEL_PILIH and MODEL_LIST_DAPAT:
                MODEL_PILIH = MODEL_LIST_DAPAT[0]
        except Exception as e:
            gemini_error = "LIST MODEL GAGAL: " + str(e)
    except Exception as e:
        client = None
        gemini_error = str(e)

def tanya_gemini(prompt):
    global gemini_error
    if not MODEL_PILIH:
        return None
    try:
        res = client.models.generate_content(model=MODEL_PILIH, contents=prompt)
        return res.text.strip()
    except Exception as e:
        gemini_error = str(e)
        return None

def check_kuota():
    if not client:
        return "❌ API KEY TAKDE / ROSAK. Kena buat API Key baru kat aistudio.google.com/apikey"
    if not MODEL_PILIH:
        return "❌ GOOGLE TAK BAGI SEBARANG MODEL UNTUK KUNCI NI. Model yang ada: " + str(MODEL_LIST_DAPAT) + " | Error: " + gemini_error + " | Cuba buat API Key baru dalam project baru."
    try:
        res = client.models.generate_content(model=MODEL_PILIH, contents="hi")
        return f"✅ KUOTA MASIH ADA! Model yang HAYDEN pakai sekarang: {MODEL_PILIH}. Dah guna {st.session_state.get('guna_gemini', 0)} kali sesi ni."
    except Exception as e:
        teks = str(e)
        if "429" in teks or "quota" in teks.lower() or "exceeded" in teks.lower():
            return "🛑 KUOTA DAH HABIS! Tunggu esok pagi reset."
        if "404" in teks:
            return f"⚠️ 404 lagi walaupun auto-detect. Model cuba: {MODEL_PILIH}. Model yang Google bagi: {MODEL_LIST_DAPAT}"
        if "API_KEY_INVALID" in teks or "API key not valid" in teks:
            return "❌ API KEY SALAH / DAH MATI. Buat baru, paste kat Secrets, Reboot."
        return "❌ ERROR LAIN: " + teks

if "chat" not in st.session_state:
    st.session_state.chat = []
if "guna_gemini" not in st.session_state:
    st.session_state.guna_gemini = 0

with st.sidebar:
    st.write("📊 **KUOTA HAYDEN**")
    st.write(f"Model aktif: {MODEL_PILIH if MODEL_PILIH else 'TAK JUMPA'}")
    st.write(f"Dah guna Gemini: {st.session_state.guna_gemini} kali (sesi ni)")
    if st.button("Check Kuota Sekarang"):
        with st.spinner("Check..."):
            st.info(check_kuota())
    with st.expander("Senarai Model Google Bagi"):
        st.write(MODEL_LIST_DAPAT if MODEL_LIST_DAPAT else "Kosong - Google tak bagi langsung")

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
