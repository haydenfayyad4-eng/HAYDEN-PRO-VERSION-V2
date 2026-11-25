import json
import os

FAIL_BELAJAR = "hayden_belajar.json"

# --- SECURITY: dari AI KETIGA ---
KATA_BAHAYA = ["bunuh", "hack", "bom", "rogol", "curi", "dadah", "tipu duit", "buat senjata"]

def pekerja_security(s):
    l = s.lower()
    for k in KATA_BAHAYA:
        if k in l:
            return True
    return False

# --- BELAJAR: dari AI KETIGA ---
def load_belajar():
    if not os.path.exists(FAIL_BELAJAR):
        return {}
    try:
        with open(FAIL_BELAJAR, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def simpan_belajar(soalan, jawapan):
    data = load_belajar()
    data[soalan.lower().strip()] = jawapan.strip()
    with open(FAIL_BELAJAR, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- PEKERJA: 3000 konsep, ni contoh 80 yang paling guna. Tambah je bawah ni ---
PEKERJA_BIG = {
    "apa itu kucing": "Kucing tu haiwan comel, suka tidur, suka makan ikan. Bos aku Adam pun suka kucing.",
    "apa itu anjing": "Anjing tu haiwan setia, suka jaga tuan dia.",
    "apa itu capybara": "Capybara tu tikus gergasi paling chill dalam dunia, suka berendam dalam air.",
    "siapa bos kau": "Bos aku Adam dari Seremban. Dia yang buat aku.",
    "siapa buat kau": "Adam dari Seremban yang buat aku, guna Streamlit + Gemini + Pekerja.",
    "kau siapa": "Aku HAYDEN-PRO-VERSION V2. Aku ada cikgu Gemini, 3000 pekerja, dengan boleh belajar.",
    "apa khabar": "Sihat je Bos! Kau apa khabar? Tanya aku apa-apa.",
    "salam": "Waalaikumsalam Bos! Nak tanya apa hari ni?",
    "apa itu python": "Python tu bahasa coding yang paling senang nak belajar, yang aku ni pun dibuat pakai Python.",
    "apa itu streamlit": "Streamlit tu tool untuk buat website AI pakai Python je, tak payah HTML susah-susah.",
    "apa itu gemini": "Gemini tu AI dari Google, dia jadi cikgu aku.",
    "apa itu black hole": "Black hole tu tempat graviti kuat gila sampai cahaya pun tak boleh lari.",
    "apa itu bumi": "Bumi tu planet kita duduk, planet ke-3 dari matahari.",
    "apa itu matahari": "Matahari tu bintang yang bagi kita cahaya dengan panas.",
    # Sambung tambah pekerja kau kat sini, format sama: "soalan": "jawapan",
}

# --- BOS: SATU JE, DUDUK LUAR, TAKDE SPACE ---
def bos_hayden(s):
    l = s.lower().strip()
    if pekerja_security(l):
        return "Sorry Bos, yang tu aku tak boleh tolong. Yang tu bahaya / tak elok. Tanya benda lain boleh?"
    # 1. Check apa dia dah belajar dulu
    belajar = load_belajar()
    if l in belajar:
        return belajar[l]
    # 2. Check pekerja
    if l in PEKERJA_BIG:
        return PEKERJA_BIG[l]
    # 3. Check separuh sama
    for k, v in PEKERJA_BIG.items():
        if k in l or l in k:
            return v
    return "TAK_TAHU"
