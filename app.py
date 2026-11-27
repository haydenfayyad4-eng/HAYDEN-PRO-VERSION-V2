# app.py - HAYDEN HQ - Full Version
import streamlit as st
import time
import random
from datetime import datetime

st.set_page_config(page_title="HAYDEN HQ", page_icon="🤖", layout="wide")

# --- LOGIN ---
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"sender": "BOT ASSISTANT", "role": "bot", "text": "Selamat datang ke HAYDEN HQ! Saya Bot Assistant. Saya akan jaga Hayden 24 jam. Kalau Hayden error, saya akan bagitau Boss & Acap kat sini.", "time": "Sekarang"},
        {"sender": "HAYDEN", "role": "hayden", "text": "Hai Boss! Hayden dah online. Apa-apa suruh je saya.", "time": "Sekarang"},
    ]
if "hayden_status" not in st.session_state:
    st.session_state.hayden_status = "✅ ONLINE - Sihat"

# --- SIDEBAR LOGIN ---
st.sidebar.title("👑 HAYDEN HQ")
st.sidebar.write(f"Status Hayden: {st.session_state.hayden_status}")

if not st.session_state.user:
    st.title("👑 HAYDEN HQ - Login")
    st.write("Pilih siapa kau:")
    nama = st.text_input("Nama kau:")
    peranan = st.selectbox("Kau siapa?", ["BOSS", "ACAP - Assistant Manusia", "BOT ASSISTANT", "HAYDEN"])
    password = st.text_input("Password Group (buat sama untuk semua):", type="password", value="hayden123")

    if st.button("MASUK GROUP"):
        if nama and password == "hayden123":
            st.session_state.user = {"nama": nama, "peranan": peranan}
            st.rerun()
        else:
            st.error("Nama kosong atau password salah! Password: hayden123")
    st.stop()

user = st.session_state.user
st.sidebar.success(f"Login sebagai: {user['nama']} ({user['peranan']})")
if st.sidebar.button("Log Out"):
    st.session_state.user = None
    st.rerun()

# --- MAIN CHAT ---
st.title("💬 HAYDEN HQ - Group Chat")
st.caption("Boss + Acap + Bot Assistant + Hayden - Semua sembang kat sini")

# Papar mesej
for m in st.session_state.messages:
    if m["role"] == "bot":
        st.info(f"🤖 **{m['sender']}** ({m['time']}):\n\n{m['text']}")
    elif m["role"] == "hayden":
        st.success(f"✨ **{m['sender']}** ({m['time']}):\n\n{m['text']}")
    elif m["role"] == "boss":
        st.warning(f"👑 **{m['sender']} - BOSS** ({m['time']}):\n\n{m['text']}")
    else:
        st.chat_message("user").write(f"🧑‍💻 **{m['sender']}** ({m['time']}):\n\n{m['text']}")

# --- HANTAR MESEJ ---
col1, col2 = st.columns([4, 1])
with col1:
    teks = st.text_input("Taip mesej kat sini...", key="input_teks", label_visibility="collapsed")
with col2:
    hantar = st.button("Hantar ➡️")

if hantar and teks:
    masa = datetime.now().strftime("%H:%M")
    # Tentukan role
    if "BOSS" in user["peranan"]:
        role = "boss"
    elif "ACAP" in user["peranan"]:
        role = "member"
    elif "BOT" in user["peranan"]:
        role = "bot"
    else:
        role = "hayden"

    st.session_state.messages.append({"sender": user["nama"], "role": role, "text": teks, "time": masa})

    # --- BOT ASSISTANT AUTO-DETECT ERROR ---
    kata_error = ["error", "rosak", "tak jalan", "bug", "down", "gagal", "crash", "tak boleh"]
    if any(k in teks.lower() for k in kata_error):
        st.session_state.hayden_status = "🔴 ERROR - Bot tengah suruh Hayden betulkan"
        st.session_state.messages.append({"sender": "BOT ASSISTANT", "role": "bot", "text": f"⚠️ ALERT! Boss, {user['nama']} cakap ada error! Hayden, tolong betulkan sekarang! Error: '{teks}'", "time": masa})
        # Hayden auto-fix
        time.sleep(1)
        st.session_state.messages.append({"sender": "HAYDEN", "role": "hayden", "text": "Okay Bot, Boss! Saya dah nampak error tu. Saya tengah betulkan... Dah siap! Cuba try balik sekarang. Kalau masih error bagitau saya lagi.", "time": masa})
        st.session_state.hayden_status = "✅ ONLINE - Dah Betulkan"
    
    # --- HAYDEN AUTO-REPLY KALAU BOSS SURUH CODING ---
    elif "coding" in teks.lower() or "buat" in teks.lower() or "tolong" in teks.lower():
        st.session_state.messages.append({"sender": "HAYDEN", "role": "hayden", "text": f"Okay Boss {user['nama']}, saya faham. Saya dah buatkan coding untuk '{teks}'. Acap, tolong checkkan sekali boleh? Kalau okay, Boss boleh approve.", "time": masa})
        st.session_state.messages.append({"sender": "BOT ASSISTANT", "role": "bot", "text": "Saya dah check coding Hayden tu, n
