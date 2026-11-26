import streamlit as st
import os
import socket
import urllib.parse
from datetime import datetime, timezone, timedelta
try:
    from zoneinfo import ZoneInfo
    ZON_MY = ZoneInfo("Asia/Kuala_Lumpur")
except:
    ZON_MY = timezone(timedelta(hours=8))
from pekerja import bos_hayden, simpan_belajar, JUMLAH_PEKERJA, waktu_malaysia
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖")

st.markdown("""
<style>
.stAppDeployButton {display: none !important; visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 HAYDEN-PRO-VERSION V2")
st.caption("Online • Tanya HAYDEN apa-apa • Boleh buat imej jugak")

def ada_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

OFFLINE = not ada_internet()

# Waktu sebenar Malaysia - ni yang kita hantar kat Gemini setiap kali
SEKARANG = datetime.now(ZON_MY)
WAKTU_TEKST = SEKARANG.strftime("%A, %d %B %Y, pukul %I:%M %p")
HARI_MELAYU = {"Monday":"Isnin","Tuesday":"Selasa","Wednesday":"Rabu","Thursday":"Khamis","Friday":"Jumaat","Saturday":"Sabtu","Sunday":"Ahad"}
BULAN_MELAYU = {"January":"Januari","February":"Februari","March":"Mac","April":"April","May":"Mei","June":"Jun","July":"Julai","August":"Ogos","September":"September","October":"Oktober","November":"November","December":"Disember"}
WAKTU_MY = f"Hari {HARI_MELAYU.get(SEKARANG.strftime('%A'), SEKARANG.strftime('%A'))}, {SEKARANG.day} {BULAN_MELAYU.get(SEKARANG.strftime('%B'), SEKARANG.strftime('%B'))} {SEKARANG.year}, pukul {SEKARANG.strftime('%I:%M %p')}"

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

if API_KEY and not OFFLINE:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        try:
            for m in client.models.list():
                nama = m.name.replace("models/", "")
                MODEL_LIST_DAPAT.append(nama)
            UTAMA = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.1-flash", "gemini-2.0-flash-lite"]
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
    if OFFLINE or not client:
        return None
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

def buat_imej(prompt_imej):
    prompt_bersih = urllib.parse.quote(prompt_imej)
    url = f"https://image.pollinations.ai/prompt/{prompt_bersih}?width=1024&height=1024&nologo=true"
    return url

def check_kuota():
    if OFFLINE:
        return "📴 OFFLINE SEKARANG. Kuota tak boleh check, kena ada internet."
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
    if OFFLINE:
        st.warning("📴 MODE OFFLINE - Jawab soalan yang dah belajar je")
    else:
        st.success("🌐 ONLINE")
    st.write(f"🕐 **{WAKTU_MY}**")
    st.write("📊 **KUOTA HAYDEN**")
    st.write(f"Model berjaya tadi: {st.session_state.model_jaya}")
    st.write(f"Dah guna Gemini: {st.session_state.guna_gemini} kali")
    if st.button("Check Kuota Sekarang"):
        with st.spinner("Check..."):
            st.info(check_kuota())
    if st.button("Padam Memory / Topik Baru"):
        st.session_state.chat = []
        st.rerun()
    st.write("**Error Terakhir:**")
    st.code(gemini_error if gemini_error else "Tiada error lagi", language="text")
    with st.expander("Senarai Model Cuba"):
        st.write(MODEL_CUBA)
    with st.expander("🎨 Cara Buat Imej"):
        st.write("Taip je:")
        st.code("buat imej kucing main bola kat pantai")
        st.code("lukis rumah kampung waktu senja")

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        if m.get("type") == "image":
            st.image(m["text"], caption=m.get("caption", ""))
        else:
            st.write(m["text"])

tanya = st.chat_input("Tanya HAYDEN apa-apa... / buat imej ...")
if tanya:
    st.session_state.chat.append({"role": "user", "text": tanya})
    with st.chat_message("user"):
        st.write(tanya)
    with st.chat_message("assistant"):
        with st.spinner("HAYDEN tengah fikir..."):
            jawapan = ""
            t_lower = tanya.lower().strip()
            kata_imej = ["buat imej", "buat gambar", "buatkan gambar", "buatkan imej", "lukis", "gambar", "generate image", "buat poster", "buat logo"]
            nak_imej = any(k in t_lower for k in kata_imej)
            if nak_imej:
                if OFFLINE:
                    jawapan = "Aku offline sekarang, tak boleh buat imej. Kena ada internet."
                    st.write(jawapan)
                    st.session_state.chat.append({"role": "assistant", "text": jawapan})
                else:
                    prompt_imej = tanya
                    for k in kata_imej:
                        prompt_imej = prompt_imej.lower().replace(k, "").strip()
                    if not prompt_imej:
                        prompt_imej = "kucing comel"
                    url_imej = buat_imej(prompt_imej)
                    st.write(f"OK, ni imej untuk: **{prompt_imej}**")
                    st.image(url_imej, caption=prompt_imej)
                    st.session_state.chat.append({"role": "assistant", "text": f"OK, ni imej untuk: {prompt_imej}"})
                    st.session_state.chat.append({"role": "assistant", "text": url_imej, "type": "image", "caption": prompt_imej})
            elif t_lower in ["check kuota", "kuota", "check quota", "baki kuota"]:
                jawapan = check_kuota()
                st.write(jawapan)
                st.session_state.chat.append({"role": "assistant", "text": jawapan})
            elif t_lower.startswith("ajar aku"):
                try:
                    bahagian = tanya.split("|", 3)
                    kod_bos = bahagian[1].strip()
                    soalan_baru = bahagian[2].strip()
                    jawapan_baru = bahagian[3].strip()
                    if kod_bos == "ADAM-BOS":
                        simpan_belajar(soalan_baru, jawapan_baru)
                        jawapan = "Ok, dah simpan. Lepas ni boleh jawab offline dah."
                    else:
                        jawapan = "Eh, kod salah."
                except:
                    jawapan = "Format: ajar aku | ADAM-BOS | soalan | jawapan"
                st.write(jawapan)
                st.session_state.chat.append({"role": "assistant", "text": jawapan})
            else:
                jawapan = bos_hayden(tanya)
                if jawapan == "TAK_TAHU" and OFFLINE:
                    jawapan = "Aku offline sekarang, soalan ni aku tak belajar lagi. Nanti bila ada internet, ajar aku soalan ni, lepas tu aku boleh jawab offline."
                if jawapan == "TAK_TAHU":
                    cari = cari_pengetahuan(tanya, NEWS_API_KEY)
                    if cari:
                        jawapan = cari
                if jawapan == "TAK_TAHU" and client and not OFFLINE:
                    history = st.session_state.chat[-7:-1]
                    teks_history = ""
                    for h in history:
                        if h.get("type") == "image":
                            continue
                        peranan = "User" if h["role"] == "user" else "HAYDEN"
                        teks_history += f"{peranan}: {h['text']}\n"
                    # Ni yang buat dia tahu waktu Malaysia sebenar
                    prompt = CARA_JAWAB + "\nInfo: " + HAYDEN_INFO + f"\nWAKTU SEBENAR SEKARANG DI MALAYSIA: {WAKTU_MY}. Guna waktu ni kalau user tanya pasal waktu, hari, tarikh, esok, semalam, bila. Jangan guna waktu lain.\n\nPERBUALAN SEBELUM NI (INGAT TOPIK NI):\n" + teks_history + "\nSoalan terbaru user: " + tanya
                    hasil = tanya_gemini(prompt)
                    if hasil:
                        jawapan = hasil
                        simpan_belajar(tanya, hasil)
                        st.session_state.guna_gemini += 1
                    else:
                        jawapan = "GEMINI ERROR: " + gemini_error
                if jawapan == "TAK_TAHU":
                    if OFFLINE:
                        jawapan = "Aku offline sekarang, soalan ni aku tak belajar lagi."
                    elif not API_KEY:
                        jawapan = "GEMINI ERROR: API KEY KOSONG"
                    elif gemini_error:
                        jawapan = "GEMINI ERROR SETUP: " + gemini_error
                    else:
                        jawapan = "Aku tak tahu lagi yang ni."
                st.write(jawapan)
                st.session_state.chat.append({"role": "assistant", "text": jawapan})
