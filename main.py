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
st.caption(f"Adam dari Seremban | {JUMLAH_PEKERJA} pekerja dalam sistem")

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
MODEL_GAMBAR = "gemini-2.5-flash-image"

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

def tanya_gemini(prompt, gambar=None):
    global gemini_error
    for nama_model in MODEL_CUBA:
        try:
            if gambar:
                from google.genai import types
                res = client.models.generate_content(model=nama_model, contents=[prompt, gambar])
            else:
                res = client.models.generate_content(model=nama_model, contents=prompt)
            if res.text:
                st.session_state["model_jaya"] = nama_model
                return res.text.strip()
        except Exception as e:
            gemini_error = f"[{nama_model}] {str(e)}"
            continue
    return None

def buat_gambar(prompt_gambar):
    # Guna model gambar Gemini
    try:
        from google.genai import types
        res = client.models.generate_content(model=MODEL_GAMBAR, contents=f"Buatkan gambar: {prompt_gambar}")
        for part in res.candidates[0].content.parts:
            if part.inline_data:
                return part.inline_data.data
        return None
    except Exception as e:
        st.session_state["gambar_error"] = str(e)
        return None

def check_kuota():
    if not client:
        return "❌ API KEY TAKDE / ROSAK"
    hasil = tanya_gemini("hi")
    if hasil:
        return f"✅ KUOTA MASIH ADA! Model: {st.session_state.get('model_jaya', '?')}"
    return "❌ ERROR: " + gemini_error

if "chat" not in st.session_state:
    st.session_state.chat = []
if "guna_gemini" not in st.session_state:
    st.session_state.guna_gemini = 0
if "model_jaya" not in st.session_state:
    st.session_state.model_jaya = "-"
if "gambar_error" not in st.session_state:
    st.session_state.gambar_error = ""

# --- SIDEBAR ---
with st.sidebar:
    st.write("📊 **KUOTA HAYDEN**")
    st.write(f"Model: {st.session_state.model_jaya} | Guna: {st.session_state.guna_gemini}")
    if st.button("Check Kuota Sekarang"):
        st.info(check_kuota())
    st.write("**Error Terakhir:**")
    st.code(gemini_error if gemini_error else "Tiada", language="text")

# --- PAPAR CHAT LAMA ---
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        if m.get("type") == "image":
            st.image(m["image"], caption=m.get("text", ""))
        else:
            st.write(m["text"])

# --- 3 FITUR BARU: VOICE + PHOTO + BUAT GAMBAR ---
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    suara = st.audio_input("🎤 Voice")
with col2:
    foto = st.file_uploader("📷 Hantar Gambar", type=["jpg", "jpeg", "png", "webp"])
with col3:
    nak_gambar = st.text_input("🎨 Nak Buat Gambar? Taip sini", placeholder="cth: kucing main bola kat Seremban")

# Kalau user hantar voice, tukar jadi teks
teks_suara = ""
if suara:
    try:
        from google.genai import types
        # Gemini dengar audio terus
        res = client.models.generate_content(model=MODEL_CUBA[0], contents=["Tolong tulis apa yang orang ni cakap dalam audio ni, dalam Bahasa Melayu. Tulis ayat dia je.", types.Part.from_bytes(data=suara.getvalue(), mime_type="audio/wav")])
        teks_suara = res.text.strip()
        st.info(f"🎤 Kau cakap: {teks_suara}")
    except Exception as e:
        st.error("Voice gagal: " + str(e))

# Kalau user nak buat gambar
if nak_gambar:
    with st.spinner("HAYDEN tengah lukis..."):
        data_gambar = buat_gambar(nak_gambar)
        if data_gambar:
            import base64
            st.image(base64.b64decode(data_gambar), caption=nak_gambar)
            st.session_state.chat.append({"role": "assistant", "text": f"Dah siap gambar: {nak_gambar}", "type": "text"})
        else:
            st.error("Buat gambar gagal: " + st.session_state.gambar_error + " | Model gambar mungkin tak aktif untuk kunci free kau. Cuba buat API Key baru.")

tanya = st.chat_input("Tanya HAYDEN apa-apa...")
# Kalau ada voice, guna teks voice tu jadi soalan
if teks_suara and not tanya:
    tanya = teks_suara

if tanya or foto:
    soalan_final = tanya if tanya else "Apa yang kau nampak dalam gambar ni? Cerita dalam Bahasa Melayu santai."
    if tanya:
        st.session_state.chat.append({"role": "user", "text": tanya})
        with st.chat_message("user"):
            st.write(tanya)
    if foto:
        st.session_state.chat.append({"role": "user", "text": "Hantar gambar", "type": "image", "image": foto})
        with st.chat_message("user"):
            st.image(foto, caption="Gambar kau")
    with st.chat_message("assistant"):
        with st.spinner("HAYDEN tengah fikir..."):
            jawapan = ""
            t_lower = (tanya or "").lower().strip()
            if t_lower in ["check kuota", "kuota", "check quota"]:
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
                        jawapan = "Eh, ajar aku ni untuk Bos je."
                except:
                    jawapan = "Format: ajar aku | ADAM-BOS | soalan | jawapan"
            else:
                jawapan = bos_hayden(soalan_final) if not foto else "TAK_TAHU"
                if jawapan == "TAK_TAHU" and client:
                    prompt = CARA_JAWAB + "\nInfo: " + HAYDEN_INFO + "\nSoalan: " + soalan_final
                    # Kalau ada foto, bagi gambar kat Gemini sekali
                    gambar_part = None
                    if foto:
                        from google.genai import types
                        gambar_part = types.Part.from_bytes(data=foto.getvalue(), mime_type=foto.type)
                    hasil = tanya_gemini(prompt, gambar_part)
                    if hasil:
                        jawapan = hasil
                        st.session_state.guna_gemini += 1
                    else:
                        jawapan = "GEMINI ERROR: " + gemini_error
                if jawapan == "TAK_TAHU":
                    jawapan = "Aku tak tahu lagi yang ni."
            st.write(jawapan)
            st.session_state.chat.append({"role": "assistant", "text": jawapan})
