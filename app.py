import streamlit as st
from pekerja import bos_hayden

st.set_page_config(page_title="HAYDEN", page_icon="🤖")
st.title("🤖 HAYDEN-PRO-VERSION")
st.caption("Bos: Adam | 9000 Pekerja")

if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.write(m["text"])

soalan = st.chat_input("Tanya Hayden...")
if soalan:
    st.session_state.chat.append({"role": "user", "text": soalan})
    jawapan = bos_hayden(soalan)
    st.session_state.chat.append({"role": "assistant", "text": jawapan})
    st.rerun()
