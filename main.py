import streamlit as st
import os, base64
from pekerja import bos_hayden, simpan_belajar, JUMLAH_PEKERJA
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="HAYDEN-PRO-VERSION V2", page_icon="🤖", layout="centered")

st.markdown("""
<style>
.stAppDeployButton {display:none !important; visibility:hidden !important;}
header {visibility: hidden !important;}
.block-container {padding-top: 10px !important; padding-bottom: 120px !important; max-width: 700px !important;}
input[type="text"] {
    background: #2a3942 !important;
    color: white !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

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
    except
