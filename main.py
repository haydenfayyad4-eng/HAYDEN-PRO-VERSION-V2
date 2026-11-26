import streamlit as st
import os, base64
from pekerja import bos_hayden, simpan_belajar, JUMLAH_PEKERJA
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖", layout="centered")

st.markdown("""
<style>
.stAppDeployButton {display:none !important; visibility:hidden !important;}
header {visibility: hidden !important;}
.block-container {padding-top: 10px !important; padding-bottom: 140px !important; max-width: 700px !important;}
/* Butang emoji jadi bulat, besar, senang tekan kat phone */
div[data-testid="stButton"] > button {
    font-size: 22px !important;
    padding: 2px 2px !important;
    border-radius: 50% !important;
    background: transparent !important;
    border: none !important;
    min-height: 38px !important;
}
div[data-testid="stButton"] > button:hover {
    background: #2a3942 !important;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style="display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid #222;">
  <div style="width:42px; height:42px; border-radius:50%; background:#00a884; display:flex; align-items:center; justify-content:center; font-size:22px;">🤖</div>
  <div>
    <div style="font-weight:700; font-size:17px; color:white;">HAYDEN-PRO-VERSION V2 <span style="color:#53bdeb; font-size:12px;">✓</span></div>
    <div style="font-size:12px; color:#8696a0;">Online • Adam dari Seremban</div>
  </div>
</div>
""", unsafe_allow_html=True)

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
                MODEL_LIST_DAPAT.append(m.name.replace("models/", ""))
            UTAMA = ["gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.1-flash", "gemini-2.0-flash-lite"]
            for u in UTAMA:
                if u in MODEL_LIST_DAPAT:
                    MODEL_CUBA.append(u)
            for n in MODEL_LIST_DAPAT:
                if "flash" in n.lower() and n not in MODEL_CUBA and "image" not in n.lower() and "preview" not in n.lower():
                    MODEL_CUBA.append(n)
        except Exception as e:
            gemini_error = str(e)
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
    try:
        res = client.models.generate_content(model=MODEL_GAMBAR, contents=f"Buatkan gambar: {prompt_gambar}")
        for part in res.candidates[0].content.parts:
            if part.inline_data:
                return part.inline_data.data
        return None
    except Exception as e:
        st.session_state["gambar_error"] = str(e)
        return None

if "chat" not in st.session_state:
    st.session_state.chat = []
if "guna_gemini" not in st.session_state:
    st.session_state.guna_gemini = 0
if "model_jaya" not in st.session_state:
    st.session_state.model_jaya = "-"
if "gambar_error" not in st.session_state:
    st.session_state.gambar_error = ""
if "msg_box" not in st.session_state:
    st.session_state.msg_box = ""

with st.sidebar:
    st.write("📊 Kuota")
    st.write(f"Model: {st.session_state.model_jaya} | Guna: {st.session_state.guna_gemini}")
    if st.button("Check Kuota"):
        if tanya_gemini("hi"):
            st.success("✅ Kuota Masih Ada!")
        else:
            st.error("❌ " + gemini_error)
    st.write("Error:")
    st.code(gemini_error if gemini_error else "Tiada")

# --- PAPAR CHAT ---
for m in st.session_state.chat:
    if m["role"] == "user":
        st.markdown(f"<div style='display:flex; justify-content:flex-end; margin:6px 0;'><div style='background:#005c4b; color:white; padding:9px 12px; border-radius:12px 12px 0 12px; max-width:80%; font-size:15px;'>{m['text']}</div></div>", unsafe_allow_html=True)
        if m.get("image"):
            st.image(m["image"], width=250)
    else:
        if m.get("type") == "image":
            st.image(m["image"], caption=m.get("text",""))
        else:
            st.markdown(f"<div style='display:flex; justify-content:flex-start; margin:6px 0;'><div style='background:#202c33; color:white; padding:9px 12px; border-radius:12px 12px 12px 0; max-width:85%; font-size:15px;'>{m['text']}</div></div>", unsafe_allow_html=True)

st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

# ================= EMOJI BAR =================
# Tekan emoji, dia masuk dalam Message terus
st.markdown("<div style='font-size:13px; color:#8696a0; margin-bottom:2px;'>😀 Emoji Cepat - Tekan je:</div>", unsafe_allow_html=True)

EMOJI_CEPAT = ["😂","❤️","👍","🔥","😭","😅","🙏","😍","😡","🤣","😮","👏"]
cols = st.columns(len(EMOJI_CEPAT))
for i, em in enumerate(EMOJI_CEPAT):
    with cols[i]:
        if st.button(em, key=f"em_{i}"):
            st.session_state.msg_box = st.session_state.msg_box + em
            st.rerun()

# Emoji banyak lagi dalam ni, tekan untuk buka
with st.expander("😀 Semua Emoji - Muka | Haiwan | Makan | Bola | Lain-lain"):
    st.markdown("**😀 Muka**")
    c = st.columns(8)
    for i, em in enumerate(["😀","😁","😆","😊","😎","🤔","😴","🥳","😇","😈","🤯","🥺","😤","🤢","😱","💀"]):
        with c[i % 8]:
            if st.button(em, key=f"muka_{i}"):
                st.session_state.msg_box += em
                st.rerun()
    st.markdown("**🐱 Haiwan**")
    c = st.columns(8)
    for i, em in enumerate(["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵","🦄"]):
        with c[i % 8]:
            if st.button(em, key=f"haiwan_{i}"):
                st.session_state.msg_box += em
                st.rerun()
    st.markdown("**🍔 Makan**")
    c = st.columns(8)
    for i, em in enumerate(["🍔","🍕","🍟","🌭","🍿","🍩","🍦","🍰","🍫","☕","🧋","🍺","🍎","🍇","🍓","🌶️"]):
        with c[i % 8]:
            if st.button(em, key=f"makan_{i}"):
                st.session_state.msg_box += em
                st.rerun()
    st.markdown("**⚽ Bola & Negeri Sembilan**")
    c = st.columns(8)
    for i, em in enumerate(["⚽","🏆","🥇","🎯","🏸","🏀","🚴","🏊","🇲🇾","❤️","💛","🖤","🔥","💪","👑","🎉"]):
        with c[i % 8]:
            if st.button(em, key=f"bola_{i}"):
                st.session_state.msg_box += em
                st.rerun()
    st.markdown("**👋 Lain-lain**")
    c = st.columns(8)
    for i, em in enumerate(["👋","🤝","👌","✌️","🤞","🫡","🙌","👀","💯","✨","⭐","🌙","☀️","🌧️","🚗","🏠"]):
        with c[i % 8]:
            if st.button(em, key=f"lain_{i}"):
                st.session_state.msg_box += em
                st.rerun()
    if st.button("🗑️ Padam Message"):
        st.session_state.msg_box = ""
        st.rerun()

# ================= BAR BAWAH MACAM WHATSAPP =================
c1, c2, c3, c4 = st.columns([6, 1, 1, 1])
with c1:
    tanya = st.text_input("Message", placeholder="Message", label_visibility="collapsed", key="msg_box")
with c2:
    foto = st.file_uploader("📎", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="attach")
    st.markdown("<div style='text-align:center; font-size:11px; color:#8696a0; margin-top:-18px;'>📎</div>", unsafe_allow_html=True)
with c3:
    kamera = st.camera_input("📷", label_visibility="collapsed", key="cam")
    st.markdown("<div style='text-align:center; font-size:11px; color:#8696a0; margin-top:-18px;'>📷</div>", unsafe_allow_html=True)
with c4:
    suara = st.audio_input("🎤", label_visibility="collapsed", key="mic")
    st.markdown("<div style='text-align:center; font-size:11px; color:#00a884; margin-top:-18px;'>🎤</div>", unsafe_allow_html=True)

nak_gambar = st.text_input("🎨 Buat Gambar", placeholder="🎨 Taip nak gambar apa... cth: kucing main bola kat Seremban", label_visibility="collapsed", key="buat_gambar_box")
hantar = st.button("➤ Hantar", use_container_width=True)

teks_suara = ""
if suara:
    try:
        from google.genai import types
        res = client.models.generate_content(model=MODEL_CUBA[0], contents=["Tulis apa orang ni cakap dalam audio ni, dalam Bahasa Melayu. Tulis ayat dia je.", types.Part.from_bytes(data=suara.getvalue(), mime_type="audio/wav")])
        teks_suara = res.text.strip()
        st.info(f"🎤 Kau cakap: {teks_suara}")
    except Exception as e:
        st.error("Voice gagal: " + str(e))

if teks_suara and not tanya:
    tanya = teks_suara

if nak_gambar:
    with st.spinner("HAYDEN tengah lukis..."):
        data_gambar = buat_gambar(nak_gambar)
        if data_gambar:
            img_bytes = base64.b64decode(data_gambar)
            st.image(img_bytes, caption=nak_gambar)
            st.session_state.chat.append({"role": "assistant", "text": f"Dah siap gambar: {nak_gambar}"})
        else:
            st.error("Buat gambar gagal: " + st.session_state.gambar_error)

gambar_final = foto if foto else kamera
if (hantar and (tanya or gambar_final)) or gambar_final:
    soalan_final = tanya if tanya else "Apa yang kau nampak dalam gambar ni? Cerita santai Bahasa Melayu."
    if tanya:
        st.session_state.chat.append({"role": "user", "text": tanya})
    if gambar_final:
        st.session_state.chat.append({"role": "user", "text": "📷 Gambar", "image": gambar_final})
    with st.spinner("HAYDEN tengah fikir..."):
        jawapan = ""
        t_lower = (tanya or "").lower().strip()
        if t_lower in ["check kuota", "kuota"]:
            jawapan = "✅ Kuota masih ada" if tanya_gemini("hi") else "❌ " + gemini_error
        elif t_lower.startswith("ajar aku"):
            try:
                bahagian = tanya.split("|", 3)
                if bahagian[1].strip() == "ADAM-BOS":
                    simpan_belajar(bahagian[2].strip(), bahagian[3].strip())
                    jawapan = "Ok, dah simpan."
                else:
                    jawapan = "Eh, untuk Bos je."
            except:
                jawapan = "Format: ajar aku | ADAM-BOS | soalan | jawapan"
        else:
            jawapan = bos_hayden(soalan_final) if not gambar_final else "TAK_TAHU"
            if jawapan == "TAK_TAHU" and client:
                prompt = CARA_JAWAB + "\nInfo: " + HAYDEN_INFO + "\nSoalan: " + soalan_final
                gambar_part = None
                if gambar_final:
                    from google.genai import types
                    gambar_part = types.Part.from_bytes(data=gambar_final.getvalue(), mime_type=gambar_final.type if hasattr(gambar_final, 'type') else "image/jpeg")
                hasil = tanya_gemini(prompt, gambar_part)
                if hasil:
                    jawapan = hasil
                    st.session_state.guna_gemini += 1
                else:
                    jawapan = "GEMINI ERROR: " + gemini_error
            if jawapan == "TAK_TAHU":
                jawapan = "Aku tak tahu lagi yang ni."
        st.session_state.chat.append({"role": "assistant", "text": jawapan})
        st.session_state.msg_box = ""
        st.rerun()
